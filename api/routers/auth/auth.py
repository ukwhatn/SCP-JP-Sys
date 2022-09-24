import os
import sys

from fastapi import APIRouter, Query

router = APIRouter()

if __name__ == "__main__":
    # for development
    from ...utils.oauth2 import discord_oauth2
    from ...utils.db.session_control import SessionControler
    from ..responses import *
else:
    # in docker container
    sys.path.append("/app")
    # noinspection PyUnresolvedReferences
    from utils.oauth2 import discord_oauth2
    # noinspection PyUnresolvedReferences
    from utils.db.session_control import SessionControler
    # noinspection PyUnresolvedReferences
    from routers.responses import *

# initialize for discord oauth2
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
def discord_oauth2_callback(code: str = Query(None), error: str = Query(None), error_description: str = Query(None)):
    # validation
    if code is None and error is None and error_description is None:
        return InvalidArgumentResponse()

    # codeがパラメータになければエラーorキャンセルとして扱う
    if code is None:
        # todo: sessionに保存されたlatest visited pageにリダイレクトさせる
        return AuthFailedResponse()

    # tokenize試行
    userTokenObject = discord_oauth2.get_access_token(code)

    # tokenize失敗
    if userTokenObject is False:
        # todo: sessionに保存されたlatest visited pageにリダイレクトさせる
        # todo: 全ページに対してauth failed用パネルを実装する
        return AuthFailedResponse()

    client = userTokenObject.get_client()
    user = client.get_users_me()


@router.get("/auth/oauth2/discord/test", tags=["OAuth2"])
def test(id: str = Query(None)):
    return SessionControler().start_session(id)
