# Policy Tool

A set of utilities and classes for working with [Open Policy Agent](https://www.openpolicyagent.org/) based tools, including [Gatekeeper](https://github.com/open-policy-agent/gatekeeper) and [Conftest](https://github.com/instrumenta/conftest).


## Installation

Policy Tool can be installed from PyPI using `pip` or similar tools:

```
pip install policytool
```


## CLI

The module provides a 

```console
$ policytool build *.rego
[SecurityControls] Generating a ConstraintTemplate from "SecurityControls.rego"
[SecurityControls] Searching "lib" for additional rego files
[SecurityControls] Adding library from "lib/kubernetes.rego"
[SecurityControls] Saving to "SecurityControls.yaml"
```

You can also use the tool via Docker:

```
docker run --rm -it -v $(pwd):/app  garethr/policytool build
```


## Python

This module currently contains one class, for working with `ConstraintTemplates` in Gatekeeper.

```python
from policytool import ConstraintTemplate

with open(path_to_rego_source_file, "r") as rego:
    ct = ConstraintTemplate(name, rego.read())
print(ct.yaml)
```


## Notes

A few caveats for anyone trying to use this module.

* [Loading libraries with `lib`](https://github.com/open-policy-agent/frameworks/commit/55fa33d1cca93f3b133e76a48d2e19adbdeb9de3) is only supported in Gatekeeper HEAD today but should be in the next release.
* This module does not support parameterized ConstraintTemplates
