import json


class CustomResponse:
    """自己定義したレスポンスタイプの親クラス
    """

    def __init__(self, status: str):
        self.status = status

    def create_json(self):
        return json.dumps(vars(self))


class InvalidArgumentResponse(CustomResponse):
    """引数が不正な場合のレスポンス
    """

    def __init__(self, status: str = "invalid_argument"):
        super().__init__(status)


class AuthFailedResponse(CustomResponse):
    """認証失敗レスポンス
    """

    def __init__(self, status: str = "auth_failed"):
        super().__init__(status=status)


class RedirectResponse(CustomResponse):
    """リダイレクトを要求するレスポンス
    """

    def __init__(self, url: str, status: str = "redirect"):
        super().__init__(status)
        self.url = url
