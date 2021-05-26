import click
import iam.iam

# https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl
@click.group()
def flexera():
    pass


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    flexera.add_command(iam.iam_cli(), "iam")
    flexera(auto_envvar_prefix='FLEXERA')
