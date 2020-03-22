import shutil
from unittest.mock import Mock

import delegator  # type: ignore
import pytest  # type: ignore

from .conftest import Conftest, ConftestResult
from .errors import ConftestNotFoundError, ConftestRunError


class TestConftest(object):
    @pytest.fixture
    def conftest(self, mocker):
        mocker.patch("shutil.which", return_value="/usr/bin/conftest")

    @pytest.fixture
    def cli(self, conftest):
        return Conftest()

    def test_test_method(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file")
        delegator.run.assert_called_once_with("conftest test --output json some/file")

    def test_test_method_with_policy(self, mocker, conftest, tmpdir):
        d = tmpdir.mkdir("policy")
        d.mkdir("dir")
        cli = Conftest(tmpdir + "/policy/dir")
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file")
        delegator.run.assert_called_once_with(
            f"conftest test --output json --policy {tmpdir}/policy/dir some/file"
        )

    def test_test_method_with_namespace(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file", namespace="value")
        delegator.run.assert_called_once_with(
            "conftest test --output json --namespace value some/file"
        )

    def test_test_method_with_input(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file", input="ini")
        delegator.run.assert_called_once_with(
            "conftest test --output json --input ini some/file"
        )

    def test_test_method_with_fail_flag(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file", fail_on_warn=True)
        delegator.run.assert_called_once_with(
            "conftest test --output json --fail-on-warn some/file"
        )

    def test_test_method_with_flag_false(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file", fail_on_warn=False)
        delegator.run.assert_called_once_with("conftest test --output json some/file")

    def test_test_method_with_combine_flag(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file", combine=True)
        delegator.run.assert_called_once_with(
            "conftest test --output json --combine some/file"
        )

    def test_test_error(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="", err="mock error"))
        with pytest.raises(ConftestRunError, match="mock error"):
            cli.test("some/file")

    def test_test_missing_exe(self, mocker, conftest):
        mocker.patch("shutil.which", return_value=None)
        with pytest.raises(ConftestNotFoundError):
            cli = Conftest()
            cli.test("some/file")

    def test_verify_method(self, mocker, cli):
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.verify()
        delegator.run.assert_called_once_with("conftest verify --output json")

    def test_verify_method_with_policy(self, mocker, conftest, tmpdir):
        d = tmpdir.mkdir("policy")
        d.mkdir("dir")
        cli = Conftest(tmpdir + "/policy/dir")
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.verify()
        delegator.run.assert_called_once_with(
            f"conftest verify --output json --policy {tmpdir}/policy/dir"
        )


@pytest.mark.integration
def test_json_fail(tmpdir):
    d = tmpdir.mkdir("policy")
    fh = d.join("test.rego")
    fh.write(
        """package main

has_key(x, k) { _ = x[k] }

deny[msg] {
    input.foo == "bar"
    msg := "bar not allowed"
}
"""
    )
    import json

    test_conftest_result = Conftest(tmpdir + "/policy").test(json_input={"foo": "bar"})
    assert test_conftest_result.code == 1
    assert test_conftest_result.results == [
        ConftestResult(
            filename="",
            warnings=[],
            failures=[{"msg": "bar not allowed"}],
            successes=[],
        )
    ]


@pytest.mark.integration
def test_json_success(tmpdir):
    d = tmpdir.mkdir("policy")
    fh = d.join("test.rego")
    fh.write(
        """package main

has_key(x, k) { _ = x[k] }

deny[msg] {
    input.foo == "bar"
    msg := "bar not allowed"
}
"""
    )
    import json

    test_conftest_result = Conftest(tmpdir + "/policy").test(json_input={"foo": "boat"})
    assert test_conftest_result.code == 0
    assert test_conftest_result.results == [
        ConftestResult(
            filename="", warnings=[], failures=[], successes=[{"msg": "data.main.deny"}]
        )
    ]
