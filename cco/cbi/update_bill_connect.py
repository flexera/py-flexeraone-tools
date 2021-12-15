import json
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
@click.option('--id', prompt="ID", help="ID", required=True)
@click.option('--name', prompt="CBI Name", help="CBI Name", required=True)
@click.option('--optima-display-name', required=False)
@click.option('--optima-vendor-name', required=False)
def create_bill_connect(refresh_token, host, org_id, id, name, optima_display_name, optima_vendor_name):
    """
    Bill Connect Create
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    # ===== Use Access Token as Bearer token from them on ===== #
    auth_headers = {"Api-Version": "1.0", "Authorization": "Bearer " + access_token}
    kwargs = {"headers": auth_headers, "allow_redirects": False}

    bill_connect_url = "https://api.optima.flexeraeng.com/api/onboarding/orgs/{}/bill_connects/cbi/{}".format(org_id, id)
    cbi_params = {}
    if optima_display_name:
        cbi_params["optima_display_name"] = optima_display_name
    if optima_vendor_name:
        cbi_params["vendor_name"] = optima_vendor_name
    bill_connect = {
        "cbi_name": name,
        "cbi_params": cbi_params
    }
    try:
        r = requests.patch(bill_connect_url, json.dumps(bill_connect), **kwargs)
        if r.status_code == 403:
            print("\033[91m\nUser needs Enterprise Manager role!!!\n\033[0m")

        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error Response: {}".format(e.response.text))
        raise SystemExit(e)

    logging.info("Response: {}\n{}".format(r.status_code, r.text))

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
    create_bill_connect(auto_envvar_prefix='FLEXERA')
