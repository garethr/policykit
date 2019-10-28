# Policy Kit

A set of utilities and classes for working with [Open Policy Agent](https://www.openpolicyagent.org/) based tools, including [Gatekeeper](https://github.com/open-policy-agent/gatekeeper) and [Conftest](https://github.com/instrumenta/conftest).


## Installation

Policy Kit can be installed from PyPI using `pip` or similar tools:

```
pip install policykit
```


## CLI

The module provides a CLI tool called `pk` for using some of the functionality.

```console
$ pk build *.rego
[SecurityControls] Generating a ConstraintTemplate from "SecurityControls.rego"
[SecurityControls] Searching "lib" for additional rego files
[SecurityControls] Adding library from "lib/kubernetes.rego"
[SecurityControls] Saving to "SecurityControls.yaml"
```

You can also use the tool via Docker:

```
docker run --rm -it -v $(pwd):/app  garethr/policykit build
```


## Python

This module currently contains one class, for working with `ConstraintTemplates` in Gatekeeper.

```python
from policykit import ConstraintTemplate

with open(path_to_rego_source_file, "r") as rego:
    ct = ConstraintTemplate(name, rego.read())
print(ct.yaml())
```


## Action

Policy Kit can also be easily used in GitHub Actions, using the following Action. This example also demonstrates
committing the generated files back into the Git repository. Update the the values in `<>` as required.

```yaml
on: push
name: Gatekeeper
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Generate ConstraintTemplates for Gatekeeper
      uses: garethr/policykit/action@master
      with:
        args: <directory-of-rego-source-files>
    - name: Commit to repository
      env:
        GITHUB_TOKEN: ${{ secrets.github_token }}
        COMMIT_MSG: |
          Generated new ConstraintTemplates from Rego source
          skip-checks: true
      run: |
        # Hard-code user config
        git config user.email "<your-email-address>"
        git config user.name "<your-username>"
        git config --get-regexp "user\.(name|email)"
        # Update origin with token
        git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git
        # Checkout the branch so we can push back to it
        git checkout master
        git add .
        # Only commit and push if we have changes
        git diff --quiet && git diff --staged --quiet || (git commit -m "${COMMIT_MSG}"; git push origin master
```


## Notes

A few caveats for anyone trying to use this module.

* [Loading libraries with `lib`](https://github.com/open-policy-agent/frameworks/commit/55fa33d1cca93f3b133e76a48d2e19adbdeb9de3) is only supported in Gatekeeper HEAD today but should be in the next release.
* This module does not support parameterized ConstraintTemplates
