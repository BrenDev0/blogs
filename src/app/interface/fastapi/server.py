from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.app.interface.strawberry.router import get_strawberry_graphql_router
from src.app.interface.fastapi.middleware import hmac
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
        return {"status": "Blogs ok"}
    
    @app.get("/test", tags=["Internal"])
    async def test_upload():
        import os
        # Get the absolute path to the root directory
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        html_path = os.path.join(root_dir, "test_upload.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
        
    @app.get("/test_post", tags=["Internal"])
    async def test_upload():
        import os
        # Get the absolute path to the root directory
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        html_path = os.path.join(root_dir, "test_post_create.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
        


    graphql_router = get_strawberry_graphql_router()
    app.include_router(graphql_router, dependencies=[Depends(hmac.verify_hmac)])

    return app
    
    