from typing import List

import attr
import yaml


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


@attr.s(auto_attribs=True)
class ConstraintTemplate(object):
    kind: str
    rego: str
    libs: List[str] = attr.Factory(list)

    @property
    def name(self):
        return self.kind.lower()

    @property
    def plural(self):
        return self.name

    @property
    def singular(self):
        return self.name.rstrip("s")

    @property
    def list_kind(self):
        return f"{self.kind}List"

    @property
    def _template(self):
        temp = {
            "apiVersion": "templates.gatekeeper.sh/v1beta1",
            "kind": "ConstraintTemplate",
            "metadata": {"name": self.name},
            "spec": {
                "crd": {
                    "spec": {
                        "names": {
                            "kind": self.kind,
                            "listKind": self.list_kind,
                            "plural": self.plural,
                            "singular": self.singular,
                        }
                    }
                },
                "targets": [
                    {"target": "admission.k8s.gatekeeper.sh", "rego": self.rego}
                ],
            },
        }
        if self.libs:
            temp["spec"]["targets"][0]["libs"] = self.libs
        return temp

    def yaml(self):
        yaml.add_representer(str, str_presenter)
        return yaml.dump(self._template)
