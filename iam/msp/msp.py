import click
from .add_org import add_iam_msp_org
from .del_org import del_iam_msp_org
from .list_orgs import list_iam_msp_orgs
from .update_org import update_iam_msp_org

@click.group()
def msp_cli():
    pass


msp_cli.add_command(add_iam_msp_org(), "add")
msp_cli.add_command(del_iam_msp_org(), "delete")
msp_cli.add_command(list_iam_msp_orgs(), "list")
msp_cli.add_command(update_iam_msp_org(), "update")
