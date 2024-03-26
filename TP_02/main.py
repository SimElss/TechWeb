import uvicorn
from colorama import init


if __name__ == "__main__":
    init()
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000)