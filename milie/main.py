from contextlib import asynccontextmanager
import importlib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from shared.logger import default_logger
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO 앱 시작시 필요한 로직 추가(eg. kafka consumer, DB 데이터 적재 등..)
    default_logger.info("APP Start")
    yield
    # TODO 앱 종료시 필요한 로직 추가
    default_logger.info("APP Exit")

app = FastAPI(lifespan=lifespan)

ROUTERS = settings.routers

# Router 동적 등록
for router in ROUTERS:
    try:
        module_path = f"api.{settings.api_version}.{router}"
        module = importlib.import_module(module_path)
        app.include_router(
            module.router,
            prefix=f"/api/{settings.api_version}"
        )
    except ModuleNotFoundError as e:
        default_logger.warning(f"{module_path} not found")

# Handler 등록
def make_error(code: int, message: str):
    return JSONResponse(
        status_code=code,
        content={"message": message}
    )

@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    return make_error(400, str(exc) or "Invalid Input Error")

@app.exception_handler(Exception)
async def unhandled_error_handler(_: Request, exc: Exception):
    default_logger.error("Unhandled error: %s", exc)
    return make_error(500, "Internal server error")