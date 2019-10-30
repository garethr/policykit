import shutil
from unittest.mock import Mock

import delegator  # type: ignore
import pytest  # type: ignore

from .conftest import Conftest
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

    def test_test_method_with_policy(self, mocker, conftest):
        cli = Conftest("policy/dir")
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.test("some/file")
        delegator.run.assert_called_once_with(
            "conftest test --output json --policy policy/dir some/file"
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

    def test_verify_method_with_policy(self, mocker, conftest):
        cli = Conftest("policy/dir")
        mocker.patch("delegator.run", return_value=Mock(out="[]"))
        cli.verify()
        delegator.run.assert_called_once_with(
            "conftest verify --output json --policy policy/dir"
        )
