import logging
import requests
import sys
import click
import pprint

@click.command(no_args_is_help=True)
@click.option('--refresh-token', '-r', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--account-id', '-a', prompt="Service Account Id", help="Service Account Id")
@click.option('--client-id', '-c', prompt="Client ID", help="Client Id")
def get_iam_service_account_client(refresh_token, host, org_id, account_id, client_id):
    """
    Organization Add Tool for MSP's
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    get_service_account_client(host, access_token, org_id, account_id, client_id)

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def get_service_account_client(host, access_token, org_id, account_id, client_id):
    """
    create_org(host, access_token, msp_org_id, org_data)
    Creates the org and logs the response.
    """
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    service_account_url = "https://{}/iam/v1/orgs/{}/service-accounts/{}/clients/{}".format(host, org_id, account_id, client_id)
    get_service_account_request = requests.get(service_account_url, **kwargs, stream=True)
    get_service_account_request.raise_for_status()
    pprint.pprint(get_service_account_request.json())


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    get_iam_service_account_client(auto_envvar_prefix='FLEXERA')
