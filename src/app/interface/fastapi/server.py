from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.users.interface.fastapi import users_routes


def create_fastapi_app():
    app = FastAPI()

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "Blogs ok"}
    
    
    app.include_router(users_routes.router)

    return app
    
    