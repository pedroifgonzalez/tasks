from fastapi import FastAPI

from src.modules.auth.router import router as auth_router
from src.modules.tasks.router import router as task_router
from src.modules.users.router import router as user_router

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
