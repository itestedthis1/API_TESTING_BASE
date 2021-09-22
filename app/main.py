from fastapi import Depends, FastAPI


from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import works, jobs, customers, client

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(jobs.router)
app.include_router(works.router)
app.include_router(customers.router)
app.include_router(client.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
