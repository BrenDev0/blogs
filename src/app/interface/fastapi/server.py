from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.app.interface.strawberry.router import get_strawberry_graphql_router
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.security.domain.exceptions import HMACException


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

    @app.exception_handler(HMACException)
    async def hmac_exception_handler(request, exc: HMACException):
        return JSONResponse(
            status_code=401,
            content={"errors": [exc.detail]}
        )

    @app.get("/", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "ConvertIA ok"}
    

    graphql_router = get_strawberry_graphql_router()
    app.include_router(graphql_router, dependencies=[Depends(verify_hmac)])

    return app
    
    