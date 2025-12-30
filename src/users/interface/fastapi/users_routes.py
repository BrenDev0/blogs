from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from src.users.application.use_cases import create
from src.users.domain.schemas import CreateUserRequest, UserPublic
from src.security.domain.services.web_token import WebTokenService
from src.users.dependencies.use_cases import get_create_user_use_case
from src.security.dependencies.services import get_web_token_service
from src.app.interface.fastapi.middleware.verification import verification
security = HTTPBearer()
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(security)]
)

@router.post(
    path="/verified/create", 
    status_code=201, 
    response_model=UserPublic
)
def verified_create(
    req: Request,
    data: CreateUserRequest,
    _: None = Depends(verification),
    use_case: create.CreateUser = Depends(get_create_user_use_case),
    web_token_service: WebTokenService = Depends(get_web_token_service)
):
    verification_code = req.state.verification_code
    if int(data.code) != int(verification_code):
        raise HTTPException(status_code=401, detail="Unauthorized") 
    
    try:
        return use_case.execute(
            req_data=data
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to proccess request at this time")
    