import logging
import requests
import sys
import click
import pprint

@click.command(no_args_is_help=True)
@click.option('--refresh-token', '-r', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
def list_iam_roles(refresh_token, host, org_id):
    """
    Organization Add Tool for MSP's
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    list_roles(host, access_token, org_id)

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def list_roles(host, access_token, org_id):
    """
    create_org(host, access_token, msp_org_id, org_data)
    Creates the org and logs the response.
    """
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    roles_url = "https://{}/iam/v1/orgs/{}/roles".format(host, org_id)
    list_roles_request = requests.get(roles_url, **kwargs, stream=True)
    list_roles_request.raise_for_status()
    pprint.pprint(list_roles_request.json())


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    list_iam_roles(auto_envvar_prefix='FLEXERA')
