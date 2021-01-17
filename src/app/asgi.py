import uvicorn
from main import get_application

asgi_app = get_application()

if __name__ == "__main__":
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)
