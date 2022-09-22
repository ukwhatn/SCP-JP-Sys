import os
import sys

from fastapi import APIRouter

router = APIRouter()

if __name__ == '__main__':
    from ...utils.oauth2 import discord_oauth2
    from ..responses import RedirectResponse
else:
    sys.path.append("/app")
    import utils.oauth2.discord_oauth2 as discord_oauth2
    from routers.responses import RedirectResponse

# Import authentication utilities

discord_oauth2 = discord_oauth2.DiscordAuthorization(
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
    client = userTokenObject.get_client()
    return client.get_users_me()
