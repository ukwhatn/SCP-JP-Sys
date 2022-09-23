from __future__ import annotations

from urllib.parse import urlencode

import httpx


class DiscordAuthorization:
    def __init__(self,
                 authorize_url: str, tokenize_url: str, revoke_url: str,
                 client_id: str, client_secret: str,
                 redirect_url: str):
        self.authorize_url = authorize_url
        self.tokenize_url = tokenize_url
        self.revoke_url = revoke_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

    def create_authorization_url(self, scope: list[str]):
        parameters = {
            "client_id":     self.client_id,
            "redirect_uri":  self.redirect_url,
            "response_type": "code",
            "scope":         " ".join(scope)
        }
        return self.authorize_url + "?" + urlencode(parameters)

    def get_access_token(self, code: str) -> bool | UserToken:
        data = {
            "client_id":     self.client_id,
            "client_secret": self.client_secret,
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  self.redirect_url,
        }
        response = httpx.post(self.tokenize_url, data=data)

        if response.status_code != 200:
            return False

        return UserToken(auth_object=self, **response.json())


class UserToken:
    def __init__(self, auth_object: DiscordAuthorization,
                 access_token: str, token_type: str, expires_in: int,
                 refresh_token: str, scope: str):
        self.auth_object = auth_object
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.scope = scope

    def __repr__(self):
        return f"UserToken(access_token={self.access_token}, token_type={self.token_type}, expires_in={self.expires_in}, refresh_token={self.refresh_token}, scope={self.scope})"

    def __str__(self):
        return self.__repr__()

    def create_dict(self):
        return {
            "access_token":  self.access_token,
            "token_type":    self.token_type,
            "expires_in":    self.expires_in,
            "refresh_token": self.refresh_token,
            "scope":         self.scope
        }

    def refresh(self):
        data = {
            "client_id":     self.auth_object.client_id,
            "client_secret": self.auth_object.client_secret,
            "grant_type":    "refresh_token",
            "refresh_token": self.refresh_token,
        }
        response = httpx.post(self.auth_object.tokenize_url, data=data)
        response.raise_for_status()
        response_json = response.json()

        self.access_token = response_json["access_token"]
        self.token_type = response_json["token_type"]
        self.expires_in = response_json["expires_in"]
        self.refresh_token = response_json["refresh_token"]
        self.scope = response_json["scope"]

    def get_client(self):
        return DiscordAPIClient(self)


class DiscordAPIClient:
    def __init__(self, token_object: UserToken):
        self.token_object = token_object
        self.base_uri = "https://discord.com/api/v10/"

    def _get_headers(self):
        return {
            "Authorization": f"{self.token_object.token_type} {self.token_object.access_token}"
        }

    def _get(self, url: str):
        response = httpx.get(
                url=self.base_uri + url,
                headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def _post(self, url: str, body: dict):
        response = httpx.post(
                url=self.base_uri + url,
                headers=self._get_headers(),
                json=body
        )
        response.raise_for_status()
        return response.json()

    def get_users_me(self):
        response = self._get("users/@me")
        return response
