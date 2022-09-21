import json


class CustomResponse:
    """自己定義したレスポンスタイプの親クラス
    """

    def __init__(self, status: str):
        self.status = status

    def create_json(self):
        return json.dumps(vars(self))
