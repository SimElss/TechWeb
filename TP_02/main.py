import uvicorn
from colorama import init


if __name__ == "__main__":
    init()
    #Get app variable from app file in app folder (app.app)
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000)