from typing import List

import yaml


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


class ConstraintTemplate(object):
    def __init__(self, kind: str, rego: str, libs: List[str] = []):
        self.name = kind.lower()
        self.kind = kind
        self.list_kind = f"{kind}List"
        self.plural = self.name
        self.singular = self.name.rstrip("s")
        self.rego = rego
        self.libs = libs

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

    @property
    def yaml(self):
        yaml.add_representer(str, str_presenter)
        return yaml.dump(self._template)
