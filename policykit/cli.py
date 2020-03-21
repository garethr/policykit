import glob
from pathlib import Path

import click

from policykit import ConstraintTemplate

COLORS = ["red", "green", "yellow", "blue", "magenta", "cyan"]


@click.group()
def cli():
    """
    A set of utilities for working with Open Policy Agent based tools, including
    Gatekeeper and Conftest.
    """


@click.command()
@click.option("--lib", default="lib", show_default=True, type=click.Path())
@click.option("-o", "--out", type=click.Path())
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def build(files, lib, out):
    """
    Build ConstraintTemplates for Gatekeeper from rego source code
    """

    for filename in files:
        filepath = Path(filename)
        if filepath.is_dir():
            paths = []
            for source in glob.glob(f"{filepath}/*.rego"):
                paths.append(Path(source))
        else:
            paths = [filepath]

        for path in paths:
            name = path.stem
            color = COLORS[len(name) % len(COLORS)]
            head = click.style(f"[{name}]", fg=color)
            click.echo(f'{head} Generating a ConstraintTemplate from "{path}"')
            with open(path, "r") as rego:
                ct = ConstraintTemplate(name, rego.read())

            for library in glob.glob(f"{lib}/*.rego"):
                with open(library, "r") as handle:
                    click.echo(f'{head} Adding global library from "{library}"')
                    ct.libs.append(handle.read())

            lib_path = path.parent.joinpath(lib)
            if Path(lib) != lib_path:
                for library in glob.glob(f"{lib_path}/*.rego"):
                    with open(library, "r") as handle:
                        click.echo(f'{head} Adding local library from "{library}"')
                        ct.libs.append(handle.read())

            if out:
                output_path = Path(out).joinpath(f"{name}.yaml")
            else:
                output_path = path.parent.joinpath(f"{name}.yaml")
            with open(output_path, "w") as template:
                click.echo(f'{head} Saving to "{output_path}"')
                template.write(ct.yaml())


cli.add_command(build)

if __name__ == "__main__":
    cli()
