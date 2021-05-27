from main import flexera_cli
import click
from .msp.msp import msp_cli

@flexera_cli.group("iam")
@click.pass_obj
def iam_cli():
    pass


iam_cli.add_command(msp_cli(), "msp")
