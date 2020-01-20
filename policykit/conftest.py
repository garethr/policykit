import json
import shutil
from dataclasses import dataclass
from os import path
from shlex import quote
from typing import Optional

import attr
import delegator  # type: ignore

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

    def run(self, args, files="", json_input=""):
        if self.policy and not path.exists(self.policy):
            raise ConftestRunError("policy directory does not exist: %s", self.policy)

        if files and not json_input:
            args = f"{args} {files}"

        if json_input:
            args = f"{args} -"
            command = delegator.run(f"echo {quote(json.dumps(json_input))}").pipe(
                f"conftest {args}"
            )
        else:
            command = delegator.run(f"conftest {args}")

        try:
            results = []
            data = json.loads(command.out)
            for info in data:
                results.append(
                    ConftestResult.schema().loads(json.dumps(info), many=not json_input)
                )

        except json.decoder.JSONDecodeError as e:
            error_message = command.err.split("msg=")[-1].strip('"')
            raise ConftestRunError(error_message) from e

        return ConftestRun(code=command.return_code, results=results)

    @_check_for_conftest
    def test(
        self,
        files: Optional[str] = None,
        namespace: Optional[str] = None,
        input: Optional[str] = None,
        fail_on_warn: Optional[bool] = None,
        combine: Optional[bool] = None,
        json_input: Optional[str] = None,
    ):
        args = "test --output json"
        if self.policy:
            args = f"{args} --policy {self.policy}"
        if namespace:
            args = f"{args} --namespace {namespace}"
        if input:
            args = f"{args} --input {input}"
        if fail_on_warn:
            args = f"{args} --fail-on-warn"
        if combine:
            args = f"{args} --combine"

        return self.run(f"{args}", files=f"{files}", json_input=json_input)

    @_check_for_conftest
    def verify(self):
        args = "verify --output json"
        if self.policy:
            args = f"{args} --policy {self.policy}"
        return self.run(args)
