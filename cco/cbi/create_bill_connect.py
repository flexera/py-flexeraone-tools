'''
Bill Connect Tool
---------------------------
Creates a bill connect and returns the response
Usage: python create_bill_connect.py <refresh_token> <shard> <org_id> <cbi_integration_id> <cbi_bill_identifier> <cbi_name> <cbi_params> true

Parameters:
<refresh token>:        obtained from Cloud Management:
                        - go to Settings, then API Credentials in the Account Settings;
                        - enable the token and pass its value to this script.
<shard>:                3 or 4 for cm auth, F1 for FlexeraOne
<org_id>:               the relevant organization id, e.g. "12345"
<cbi_integration_id>:   the integration id (linked to that integration mentioned just above), e.g. "cbi-oi-optima";
                        - Possible integration ids: “cbi-oi-optima” (Optima CSV default format),
                        - but also "cbi-oi-oracle", “cbi-oi-alibaba” and “cbi-oi-azure-china”
                        - (talk to your Flexera account manager for those last three);
<cbi_bill_identifier>:  a bill identifier of your choice, alphanumeric (or - or _)
                        - sequence uniquely identifying this bill connect of this integration type for your organization, e.g. "test-1";
<cbi_name>:             a name/description, a human-readable string to give more information, e.g. "My test Optima CSV integration, number One";
<cbi_params>:           a parameter object in json to override the default integration settings. Pass an empty one if you are not passing any such parameters,
                        e.g. '{}'.
<tls_verification>:     true/false
'''
import os
import json
import logging
import requests
import sys
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import click
import pprint

# Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
flexera_integrations = [
    'cbi-oi-optima',
    'cbi-oi-alibaba',
    'cbi-oi-azure-china',
    'cbi-oi-oracle'
]

@click.command(no_args_is_help=True)
@click.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--id', prompt="ID", help="ID", required=True)
@click.option('--name', prompt="CBI Name", help="CBI Name", required=True)
@click.option('--integration-id', prompt='integration_id', multiple=False, type=click.Choice(flexera_integrations))
@click.option('--optima-display-name', prompt='Optima Display Name', required=False)
@click.option('--optima-vendor-name', prompt='Optima Vendor Name', required=False)
def create_bill_connect(refresh_token, host, org_id, id, name, integration_id, optima_display_name, optima_vendor_name):
    """
    Bill Connect Create
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    # ===== Use Access Token as Bearer token from them on ===== #
    auth_headers = {"Api-Version": "1.0", "Authorization": "Bearer " + access_token}
    kwargs = {"headers": auth_headers, "allow_redirects": False}

    bill_connect_url = "https://onboarding.rightscale.com/api/onboarding/orgs/{}/bill_connects/cbi".format(org_id)
    cbi_params = {}
    if optima_display_name:
        cbi_params["optima_display_name"] = optima_display_name
    if optima_vendor_name:
        cbi_params["vendor_name"] = optima_vendor_name
    bill_connect = {
        "cbi_bill_identifier": id,
        "cbi_integration_id": integration_id,
        "cbi_name": name,
        "cbi_params": cbi_params
    }
    try:
        r = requests.post(bill_connect_url, json.dumps(bill_connect), **kwargs)
        if r.status_code == 403:
            print("\033[91m\nUser needs Enterprise Manager role!!!\n\033[0m")

        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error Response: {}".format(e.response.text))
        raise SystemExit(e)

    logging.info("Response: {}\n{}".format(r.status_code, json.dumps(r.json(), indent=4)))

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
