import glob
from pathlib import Path

import click

from policytool import ConstraintTemplate

COLORS = ["red", "green", "yellow", "blue", "magenta", "cyan"]


@click.group()
def cli():
    """
    A set of utilities for working with Open Policy Agent based tools, including
    Gatekeeper and Conftest.
    """


@click.command()
@click.option("--lib", default="lib", show_default=True, type=click.Path(exists=True))
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def build(files, lib):
    """
    Build ConstraintTemplates for Gatekeeper from rego source code
    """
    for filename in files:
        name = Path(filename).stem
        color = COLORS[len(name) % len(COLORS)]
        head = click.style(f"[{name}]", fg=color)
        click.echo(f'{head} Generating a ConstraintTemplate from "{filename}"')
        with open(filename, "r") as rego:
            ct = ConstraintTemplate(name, rego.read())

        click.echo(f'{head} Searching "{lib}" for additional rego files')
        for library in glob.glob(f"{lib}/*.rego"):
            with open(library, "r") as handle:
                click.echo(f'{head} Adding library from "{library}"')
                ct.libs.append(handle.read())

        with open(f"{name}.yaml", "w") as template:
            click.echo(f'{head} Saving to "{name}.yaml"')
            template.write(ct.yaml)


cli.add_command(build)

if __name__ == "__main__":
    cli()
