from multiprocessing.resource_tracker import getfd
from typing import Annotated, Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import Session
from ..login_manager import login_manager
from ..services.beers import update_cart_item_quantity, add_to_cart, get_orders_by_user, is_beer_in_cart, get_all_beers, drop_beer_panier, get_number_beers_of_user, delete_beer, modify_beer, paid_cart, save_beers, get_number_beers, get_beer_by_id, add_owner
from ..schemas.users import UserSchema
from ..schemas.beers import Beer
from fastapi import APIRouter, status, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Create APIRouter instance for beer-related routes
router = APIRouter()

# Setup Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Route for redirecting to login page on root access
@router.get("/")
def home():
    return RedirectResponse(url="/login", status_code=302)

# Temporary route to handle user session management
@router.get("/tmp")
def tmp(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    else:
        return RedirectResponse(url="/liste", status_code=302)

# Route to display error message
@router.get("/error/{description}/{url}")
def error(request: Request, description: str, url: str):
    return templates.TemplateResponse(
        "error.html", 
        context={'request': request, 'description': description, 'url': url}
    )

# Route to display list of beers
@router.get("/liste")
def list_beers(request: Request, user: UserSchema = Depends(login_manager.optional)):
    beers = get_all_beers()
    nb = get_number_beers()
    nbUser = get_number_beers_of_user(user.id)
    return templates.TemplateResponse(
        "beers.html",
        context={'request': request,'Nombre': nb, 'nb' : nbUser , 'current_user': user, 'beers': beers}
    )

# Route to delete a beer
@router.post("/delete/{id}")
def delete(id: str):
    print(id)
    response = delete_beer(id)
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error} : No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

#route to get the page to modify a beer
@router.get("/modify/{id}")
def modify(request: Request, id: str, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    
    beer = get_beer_by_id(id)
    return templates.TemplateResponse(
        "modify.html", 
        context={'request': request, 'beer': beer, "beer.id" : id}
    )
#route to modify a beer
@router.post("/modify/{id}")
def modify(id: str, name: Annotated[str, Form()], brewery: Annotated[str, Form()], price: Annotated[float, Form()], stock: Annotated[int, Form()], description: Annotated[Optional[str], Form()] = None
):
    # Définir le chemin de l'image
    image_path = f"./static/{name}.jpg"
    
    response = modify_beer(id, image_path, name, brewery, price, stock, description)
    
    if response is None:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    
    if response == 1:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    
    return RedirectResponse(url="/liste", status_code=302)


# Route to add a new beer
@router.get("/save")
def save(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    # check if user is admin -> only admin can modify beer
    return templates.TemplateResponse(
        "save_beers.html", 
        context={'request': request, 'current_user': user}
    )
#Route to add a new beer (POST request)
@router.post("/save")
def save(name: Annotated[str, Form()], brewery: Annotated[str, Form()], price: Annotated[float, Form()], stock: Annotated[int, Form()], description: Annotated[str, Form()]):
    # define the path de the image
    image_name = f"{name.strip().replace(' ', '_').lower()}.png"
    image_path = f"./static/{image_name}"
    
    # create a new dictionnary for the beer
    new_beer = {
        "id": str(uuid4()),
        "name": name.strip(),
        "brewery": brewery.strip(),
        "price": price,
        "stock": stock,
        "description": description.strip(),
        "image": image_path,
    }
    
    new_beer = Beer.model_validate(new_beer)
    saved_beers = save_beers(new_beer)

    if saved_beers is None:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/save", status_code=302)

    return RedirectResponse(url="/liste", status_code=302)    

# Route to buy the beer (POST request)
@router.post("/buy/{id}")
def buy(id: str, user = Depends(login_manager.optional)):
    #We verify that the user is connected
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    #We verify that the beer exists
    beer = get_beer_by_id(id)
    if beer is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
     # Check if the beer is already in the user's cart
    if is_beer_in_cart(beer.id, user.id):
        # Beer is already in the cart, display a message
        description = "Cette article est déjà dans votre panier"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)

    #add the user as owner of the beer
    add_owner(id, user.id)
    add_to_cart(id, user.id)
    return RedirectResponse(url="/liste", status_code=302)

# Route to delete a beer
@router.post("/deletepanier/{id}")
def delete(id: str, user = Depends(login_manager.optional)):
    #We verify that the user is connected
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    #We verify that the beer exists
    beer = get_beer_by_id(id)
    if beer is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    #add the user as owner of the beer
    drop_beer_panier(id, user.id)

    return RedirectResponse(url="/panier", status_code=302)

@router.post("/update_quantity/{beer_id}")
def update_quantity(beer_id: str, quantity: int = Form(...), user = Depends(login_manager.optional)):
    # Vérifier que l'utilisateur est connecté
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Vérifier que la bière existe
    beer = get_beer_by_id(beer_id)
    if beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")

    # Mettre à jour la quantité de la bière dans le panier
    success = update_cart_item_quantity(beer_id, user.id, quantity)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update quantity")

    return RedirectResponse(url="/panier", status_code=302)
# Route to pay the cart
@router.post('/paiement')
def payer_panier_route(request: Request, user: UserSchema = Depends(login_manager)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    
    if paid_cart(user.id):
        return RedirectResponse(url="/purchase", status_code=302)
    else:
        return RedirectResponse(url="/panier", status_code=302)
    
# Route to get to the order of the user
@router.get('/order')
def historique(request: Request, user: UserSchema = Depends(login_manager)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    
    orders = get_orders_by_user(user.id)
    nbUser = get_number_beers_of_user(user.id)
    
    return templates.TemplateResponse(
        "order.html", 
        context={'request': request, 'current_user': user, 'orders': orders, 'nb':nbUser}
    )
#route to go to the purchase html
@router.get("/purchase")
def list_beers(request: Request, user: UserSchema = Depends(login_manager.optional)):
    nbUser = get_number_beers_of_user(user.id)
    return templates.TemplateResponse(
        "purchase.html",
        context={'request': request, 'nb' : nbUser , 'current_user': user}
    )
# Route to get the detail of all of the order 
@router.get('/orderdetail/')
def historique(request: Request, user: UserSchema = Depends(login_manager)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    
    orders = get_orders_by_user(user.id)
    nbUser = get_number_beers_of_user(user.id)
    
    return templates.TemplateResponse(
        "order_detail.html", 
        context={'request': request, 'current_user': user, 'orders': orders, 'nb':nbUser}
    )
