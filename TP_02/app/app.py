from fastapi import FastAPI, status
from app.routes.routes import router
from app.routes.users import user_router
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

app = FastAPI()
app.include_router(router)
app.include_router(user_router)
templates = Jinja2Templates(directory="templates")

@app.exception_handler(404)
def not_found(request, exc):
    error = status.HTTP_404_NOT_FOUND
    description = f"Erreur {error} : page non trouvée"
    return RedirectResponse(url=f"/error/{description}", status_code=302)

@app.exception_handler(ValidationError)
def custom_validation_error_redirection(request : Request, exception: ValidationError):
    errors = exception.errors()
    error = status.HTTP_422_UNPROCESSABLE_ENTITY
    description = f"Erreur {error} : {errors[0]['msg']}"
    return RedirectResponse(
        url=f"/error/{description}", status_code=302
    )
