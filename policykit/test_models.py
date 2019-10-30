import pytest  # type: ignore

from policykit import ConstraintTemplate
from policykit.models import ConftestRun


class TestConftestRun(object):
    def test_failures(self):
        run = ConftestRun(code=1, results=[])
        assert not run.success

    def test_pass(self):
        run = ConftestRun(code=0, results=[])
        assert run.success


class TestConstraintTemplate(object):
    @pytest.fixture
    def rego(self):
        return """package sample
import data.lib.helpers
violation[{"msg": msg}] {
    helpers.name = "Invalid"
}
"""

    @pytest.fixture
    def lib(self):
        return """package lib.helpers
name = input.review.object.metadata.name
"""

    @pytest.fixture
    def name(self):
        return "SampleThings"

    @pytest.fixture
    def template(self, name, rego):
        return ConstraintTemplate(name, rego)

    def test_kind(self, name, template):
        assert template.kind == name

    def test_list_kind(self, template):
        assert template.list_kind == "SampleThingsList"

    def test_singular(self, template):
        assert template.singular == "samplething"

    def test_plural(self, template):
        assert template.plural == "samplethings"

    def test_default_libs(self, template):
        assert template.libs == []

    def test_yaml(self, template):
        assert (
            template.yaml()
            == """apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: samplethings
spec:
  crd:
    spec:
      names:
        kind: SampleThings
        listKind: SampleThingsList
        plural: samplethings
        singular: samplething
  targets:
  - rego: |
      package sample
      import data.lib.helpers
      violation[{"msg": msg}] {
          helpers.name = "Invalid"
      }
    target: admission.k8s.gatekeeper.sh
"""
        )

    def test_adding_library(self, lib, template):
        template.libs.append(lib)
        libraries = template._template["spec"]["targets"][0]["libs"]
        assert len(libraries) == 1
        assert libraries[0] == lib
