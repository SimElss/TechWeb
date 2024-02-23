from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI()
app.include_router(router)

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")