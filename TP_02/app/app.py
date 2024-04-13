from fastapi import FastAPI, status, Depends
from app.routes.routes import router
from app.routes.users import user_router
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.database import create_database


#Structure of the app
app = FastAPI()
#Routing files -> get pages and post infos
app.include_router(router)
app.include_router(user_router)
#Include css file(s) and images
app.mount("/static", StaticFiles(directory="static"), name="static")
#Locate templates (html pages) folder
templates = Jinja2Templates(directory="templates")

#Get any 404 error from app and catch it then redirect to tmp page -> tmp redirect then to error
#Why using tmp ? Impossible to import login_manager in app_file ? So we use tmp to see if user is connected or not 
#-> choose correct page to redirect after error page
@app.exception_handler(404)
def not_found(request, exc):
    error = status.HTTP_404_NOT_FOUND
    description = f"Erreur {error} : page non trouvée"
    #redirect to tmp
    return RedirectResponse(url=f"/error/{description}/tmp", status_code=302)

#Get any error relative to model integrity
@app.exception_handler(ValidationError)
def custom_validation_error_redirection(request : Request, exception: ValidationError):
    errors = exception.errors()
    error = status.HTTP_422_UNPROCESSABLE_ENTITY
    #Works in this case cause only 1 integrity error possible -> password | see field-validator in schemas/users.py
    description = f"Erreur {error} : {errors[0]['msg']}"
    #redirect to register page
    return RedirectResponse(
        url=f"/error/{description}/register", status_code=302
    )

@app.on_event("startup")
def on_application_started():
    create_database()