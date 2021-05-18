import logging
import requests
import sys
import click
import pandas as pd
import jellyfish
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

@click.command(no_args_is_help=True)
@optgroup.group('Connection configuration',
                help='The configuration of some server connection')
@optgroup.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@optgroup.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@optgroup.option('--msp-org-id', '-m', prompt="MSP Org ID", required=True)
@optgroup.group('Org Options', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Org Options, either id or name')
@optgroup.option('--org-id', '-o', help='Org ID to Delete')
@optgroup.option('--org-name', '-n', help="Organization Name to find. Using the name will only print close orgs")
def del_iam_msp_org(**params):
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
    if params['org_id']:
        delete_org(params['host'], access_token, params['msp_org_id'], params['org_id'])
    else:
        orgs = list_orgs(params['host'], access_token, params['msp_org_id'], params['org_name'])
        click.echo(orgs)

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

def list_orgs(host, access_token, msp_org_id, org_name):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    managed_service_provider_customers_url = "https://{}/msp/v1/orgs/{}/customers".format(host, msp_org_id)
    get_response = requests.get(managed_service_provider_customers_url, **kwargs)
    get_response.raise_for_status()
    orgs = pd.DataFrame(get_response.json())
    orgs['res'] = [jellyfish.levenshtein_distance(x, y) for x, y in zip(orgs['name'], org_name)]
    orgs.where(orgs['res'] > (len(org_name) - 2), inplace=True)
    return orgs.dropna(thresh=2)

def delete_org(host, access_token, msp_org_id, org_id):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    managed_service_provider_customer_url = "https://{}/msp/v1/orgs/{}/customers/{}".format(host, msp_org_id, org_id)
    click.echo("deleting org: {}".format(managed_service_provider_customer_url))
    delete_request = requests.delete(managed_service_provider_customer_url, **kwargs)
    delete_request.raise_for_status()


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    del_iam_msp_org(auto_envvar_prefix='FLEXERA')
