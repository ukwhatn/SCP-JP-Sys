import os
import sys

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
router = APIRouter()

sys.path.append("/app")

import utils.oauth2.discord

# Import authentication utilities

discord_oauth2 = utils.oauth2.discord.DiscordAuthorization(
        authorize_url=os.environ.get("DISCORD_OAUTH2_AUTHORIZE"),
        tokenize_url=os.environ.get("DISCORD_OAUTH2_TOKENIZE"),
        revoke_url=os.environ.get("DISCORD_OAUTH2_REVOKE"),
        client_id=os.environ.get("DISCORD_OAUTH2_CLIENT_ID"),
        client_secret=os.environ.get("DISCORD_OAUTH2_CLIENT_SECRET"),
        redirect_url=os.environ.get("DISCORD_OAUTH2_REDIRECT_URL")
)


@router.get("/auth/oauth2/discord/start", tags=["OAuth2"])
def discord_oauth2_start():
    return RedirectResponse(discord_oauth2.create_authorization_url(["identify", "email"]))


@router.get("/auth/oauth2/discord/callback", tags=["OAuth2"])
def discord_oauth2_callback(code: str):
    userTokenObject = discord_oauth2.get_access_token(code)


