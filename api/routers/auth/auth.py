from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

import utils


@router.get("/auth/oauth2/discord/start", tags=["OAuth2"])
def discord_oauth2_start():
    return "OK"
