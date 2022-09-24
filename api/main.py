from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# routers
from routers.auth import auth

app = FastAPI()


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/docs")


app.include_router(auth.router)
