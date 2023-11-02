import json
import requests

from pyavwx.models.exceptions import StationError, AuthError, BadStatus
from pyavwx.models.metar import Metar


class AvwxBadStatus(Exception):
    def __init__(self, request: requests.Response):
        self.status = request.status_code
        if request.status_code == 400:
            self.exception = StationError(**json.loads(request.text))

        elif request.status_code == 401:
            self.exception = AuthError(**(json.loads(request.text)))
            self.args = (self.status, self.exception, Metar(**self.exception.sample))

        else:
            self.exception = BadStatus(error="Unknown Error", code=self.status)

    def __str__(self):
        return f"[Status_Code:{self.status}] {self.exception.error}"
