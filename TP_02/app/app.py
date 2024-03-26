from fastapi import FastAPI, status
from app.routes.routes import router
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(router)

@app.exception_handler(404)
def not_found(request, exc):
    error = status.HTTP_404_NOT_FOUND
    description = f"Erreur {error} : pas non trouvée"
    return RedirectResponse(url=f"/error/{description}", status_code=302)
