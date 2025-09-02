from fastapi import FastAPI

from src.modules.tasks.router import router as task_router
from src.modules.users.router import router as user_router

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
