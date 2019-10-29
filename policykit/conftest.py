import json
import shutil
from dataclasses import dataclass
from typing import Optional

import attr
import delegator  # type: ignor

from .errors import ConftestNotFoundError, ConftestRunError
from .models import ConftestResult, ConftestRun


def _check_for_conftest(func):
    def check(*args, **kwargs):
        if not shutil.which("conftest") is not None:
            raise ConftestNotFoundError
        return func(*args, **kwargs)

    return check


@attr.s(auto_attribs=True)
class Conftest(object):
    policy: Optional[str] = None

    def run(self, args):
        command = delegator.run(f"conftest {args}")
        try:
            results = ConftestResult.schema().loads(command.out, many=True)
        except json.decoder.JSONDecodeError as e:
            error_message = command.err.split("msg=")[-1].strip('"')
            raise ConftestRunError(error_message) from e
        return ConftestRun(code=command.return_code, results=results)

    @_check_for_conftest
    def test(
        self, files: str, namespace: Optional[str] = None, input: Optional[str] = None
    ):
        args = "test --output json"
        if self.policy:
            args = f"{args} --policy {self.policy}"
        if namespace:
            args = f"{args} --namespace {namespace}"
        if input:
            args = f"{args} --input {input}"
        return self.run(f"{args} {files}")

    @_check_for_conftest
    def verify(self):
        args = "verify --output json"
        if self.policy:
            args = f"{args} --policy {self.policy}"
        return self.run(args)
