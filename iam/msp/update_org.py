import logging
import requests
import sys
import click
from click_option_group import optgroup
import json

@click.command(no_args_is_help=True)
@optgroup.group('Connection configuration',
                help='The configuration of some server connection')
@optgroup.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@optgroup.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@optgroup.option('--msp-org-id', '-m', prompt="MSP Org ID", required=True)
@optgroup.option('--org-id', '-o', prompt='Org ID to update', required=True)
@optgroup.option('--filename', '-f', prompt="JSON file with settings", required=True)
def update_iam_msp_org(**params):
    """
    \b
    Organization Add Tool for MSP's
    -------------------------------
    Creates an organization and logs the response
    Ex: python add_org.py --refresh-token <token> -n "<Org Name>" -f "<First Name>" -l "<Last Name>" -e "<email>" -m <msp org id> --capability fcm --capability fss
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    click.echo(params)
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(params['refresh_token'], params['host'])
    with open(params['filename']) as f:
        options = json.loads(f.read())
    update_org(params['host'], access_token, params['msp_org_id'], params['org_id'], options)

def generate_access_token(refresh_token, host):
    """
    auth(refresh_token, host)
    Authenticates againsts the FlexeraOne API and returns the access token
    """
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def update_org(host, access_token, msp_org_id, org_id, options):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    managed_service_provider_customer_url = "https://{}/msp/v1/orgs/{}/customers/{}".format(host, msp_org_id, org_id)
    click.echo("patching org: {}".format(managed_service_provider_customer_url))
    update_request = requests.patch(managed_service_provider_customer_url, json.dumps(options), **kwargs)
    update_request.raise_for_status()
    logging.info("Response: {}\nHeaders: {}\n".format(update_request.status_code, update_request.headers))


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    update_iam_msp_org(auto_envvar_prefix='FLEXERA')
