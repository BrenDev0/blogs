import logging
from fastapi import Request, HTTPException, Depends
from src.security.domain.services.web_token import WebTokenService
from src.security.domain.exceptions import InvalidToken, ExpiredToken
from src.security.dependencies.services import get_web_token_service
logger = logging.getLogger(__name__)

def verification(
    req: Request,
    web_token_service: WebTokenService = Depends(get_web_token_service)
):
    auth_header = req.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unautrhorized. Missing required auth headers")
    
    token = auth_header.split(" ")[1]
    try: 
        payload = web_token_service.decode(
            token=token
        )

        verification_code = payload.get("verification_code")

        if verification_code is None:
            raise HTTPException(status_code=403, detail="Forbidden ")

        req.state.verification_code = verification_code
        

    except (ExpiredToken, InvalidToken) as e:
        logging.debug(str(e))
        raise HTTPException(status_code=401, detail=str(e))
    
    except Exception as e:
        logger.error(str(e))
        raise 
    

    

    
