import json


class CustomResponse:
    """自己定義したレスポンスタイプの親クラス
    """

    def __init__(self, status: str):
        self.status = status

    def create_json(self):
        return json.dumps(vars(self))


class RedirectResponse(CustomResponse):
    """リダイレクトを要求するレスポンス
    """

    def __init__(self, url: str):
        super().__init__("redirect")
        self.url = url
