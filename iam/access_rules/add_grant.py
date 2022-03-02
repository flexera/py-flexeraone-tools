import json
import logging
import requests
import sys
import click

@click.command(no_args_is_help=True)
@click.option('--refresh-token', '-r', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--service-account-id', prompt="Service Account Name", help="Service Account Name", required=True)
@click.option('--role-id', prompt="description", help="Description", required=True)
def add_iam_grant(refresh_token, host, org_id, service_account_id, role_id):
    """
    Organization Add Tool for MSP's
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    org_role_data = {
        "role": {
            "href": "/grs/orgs/{}/roles/{}".format(org_id, role_id)
        },
        "subject": {
            "href": "/iam/service-accounts/{}".format(service_account_id)
        }
    }
    click.echo(org_role_data)
    create_grant(access_token, org_id, org_role_data)

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def create_grant(access_token, org_id, org_data):
    """
    create_org(host, access_token, msp_org_id, org_data)
    Creates the org and logs the response.
    """
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json", "X-Api-Version": "2.0", "Accept": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    grant_url = "https://governance.rightscale.com/grs/orgs/{}/access_rules/grant".format(org_id)
    create_grant_request = requests.put(grant_url, json.dumps(org_data), **kwargs, stream=True)
    create_grant_request.raise_for_status()
    logging.info("Response: {}\nHeaders: {}\n".format(create_grant_request.status_code, create_grant_request.headers))


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    add_iam_grant(auto_envvar_prefix='FLEXERA')
