from fastapi import FastAPI
from custom_route.custom_router import custom_router
import uvicorn, os

main_app = FastAPI()

main_app.include_router(custom_router)

if __name__ == "__main__":
    port = int(os.getenv("port"))
    uvicorn.run("main:main_app", host="0.0.0.0", port=port)
