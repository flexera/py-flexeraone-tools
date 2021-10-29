import logging
import requests
import sys
import click

# Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)

@click.command(no_args_is_help=True)
@click.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--dashboard-type', help="Is this a User or Org Dashboard", required=True, type=click.Choice(['org', 'user']))
@click.option('--user-id', required=False, help="User id if user option is set")
@click.option('--filename', required=True, help="Dashboard Filename")
def list_dashboards(refresh_token, host, org_id, dashboard_type, user_id, filename):
    """
    list_dashboards
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    # ===== Use Access Token as Bearer token from them on ===== #
    auth_headers = {"Api-Version": "1.0", "Authorization": "Bearer " + access_token}
    kwargs = {"headers": auth_headers, "allow_redirects": False}
    dashboard_create_url = "https://api.optima.flexeraeng.com/bill-analysis/orgs/{}".format(org_id)
    if dashboard_type == 'user':
        dashboard_create_url = dashboard_create_url + "/users/{}/dashboards".format(user_id)
    else:
        dashboard_create_url = dashboard_create_url + "/dashboards"

    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    create_response = requests.post(dashboard_create_url, data=open(filename, 'rb').read(), **kwargs)
    create_response.raise_for_status()
    return create_response.text

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    list_dashboards(auto_envvar_prefix='FLEXERA')
