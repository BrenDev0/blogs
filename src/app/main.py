from dotenv import load_dotenv
load_dotenv()
import os
import logging
import uvicorn
from src.app.interface.fastapi.server import create_fastapi_app

def main():
    level = os.getenv("LOGGER_LEVEL", logging.INFO)
  
    logging.basicConfig(
        level=int(level),
        format="%(levelname)s - %(name)s - %(message)s"
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")

    app = create_fastapi_app()
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()