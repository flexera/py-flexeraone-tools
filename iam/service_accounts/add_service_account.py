import json
import logging
import requests
import sys
import click
import pprint

@click.command(no_args_is_help=True)
@click.option('--refresh-token', '-r', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--name', '-n', prompt="Service Account Name", help="Service Account Name", required=True)
@click.option('--description', '-d', prompt="description", help="Description", required=True)
def add_iam_service_account(refresh_token, host, org_id, name, description):
    """
    Organization Add Tool for MSP's
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    org_data = {
        "name": name,
        "description": description
    }
    click.echo(org_data)
    create_service_account(host, access_token, org_id, org_data)

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def create_service_account(host, access_token, org_id, org_data):
    """
    create_org(host, access_token, msp_org_id, org_data)
    Creates the org and logs the response.
    """
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    service_account_url = "https://{}/iam/v1/orgs/{}/service-accounts".format(host, org_id)
    create_service_account_request = requests.post(service_account_url, json.dumps(org_data), **kwargs, stream=True)
    create_service_account_request.raise_for_status()
    logging.info("Response: {}\nHeaders: {}\n".format(create_service_account_request.status_code, create_service_account_request.headers))
    new_org_url = "https://{}{}".format(host, create_service_account_request.headers['location'])
    get_response = requests.get(new_org_url, **kwargs)
    get_response.raise_for_status()
    logging.info("Response: {}\nHeaders: {}\n".format(get_response.status_code, get_response.headers))
    pprint.pprint(get_response.json())


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    add_iam_service_account(auto_envvar_prefix='FLEXERA')
