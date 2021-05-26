import click
from .msp.msp import msp_cli

@click.group()
def iam_cli():
    pass


iam_cli.add_command(msp_cli(), "msp")
