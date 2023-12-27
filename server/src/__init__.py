import openai
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import starlette.status as status
from pydantic import BaseModel
from contextlib import asynccontextmanager

from server.src.google import new_auth_url, authenticate, get_user_email
from server.src.safe_create_task import create_task
from server.src.user import User
from server.src.snip import Snip
from server.src.mongo import MONGO

openai.api_key = "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"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MONGO.load_users()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/bonsai.svg", FileResponse("build/bonsai.svg"))
app.mount("/favicon.ico", FileResponse("build/favicon.ico"))
app.mount("/static", StaticFiles(directory="build/static"), name="static")
app.mount("/images", StaticFiles(directory="build/images"), name="image")


@app.get("/")
async def index():
    return FileResponse("build/index.html")


@app.get("/profile")
async def profile(
    state: str | None = None, code: str | None = None, scope: str | None = None
):
    """
    Args:
        state:
            The client ID that we passed into flow when we created it?
        code:
            The refresh token.
        scope:
            The valid scopes.
    """
    try:
        cred = await authenticate(state, code)

        user = User.from_state(state, email=get_user_email(cred))
        user.cred = cred

        create_task(MONGO.save_user(user))

        return FileResponse("build/index.html")
    except Exception:
        return RedirectResponse("/")


@app.get("/login")
async def function():
    url = new_auth_url()
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


class UpdateUser(BaseModel):
    state: str
    phone_number: str | None
    language: str | None
    whitelist: str | None
    blacklist: str | None


@app.post("/api/update_user")
async def upate_user(data: UpdateUser):
    user = User.from_state(data.state)
    user.phone_number = data.phone_number
    user.whitelist = data.whitelist
    user.language = data.language
    user.blacklist = data.blacklist
    await MONGO.save_user(user)


@app.get("/api/snips/{state:str}")
async def get_snips(state: str):
    """
    Returns
    [{"email": str, "summary": str, "link": str}]
    """
    user = User.from_state(state)
    snips = list(map(Snip.to_json, await MONGO.fetch_snips(user)))
    return JSONResponse(snips)
