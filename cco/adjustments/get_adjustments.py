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
@click.option('--filename', help="Filename for export", required=False)
def get_adjustments(refresh_token, host, org_id, filename):
    """
    Adjustments Get
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    # ===== Use Access Token as Bearer token from them on ===== #
    auth_headers = {"Api-Version": "1.0", "Authorization": "Bearer " + access_token}
    kwargs = {"headers": auth_headers, "allow_redirects": False}

    bill_adjustments_url = "https://api.optima.flexeraeng.com/bill-analysis/orgs/{}/adjustments/".format(org_id)
    try:
        r = requests.get(bill_adjustments_url, **kwargs)
        if r.status_code == 403:
            print("\033[91m\nUser needs Enterprise Manager role!!!\n\033[0m")

        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error Response: {}".format(e.response.text))
        raise SystemExit(e)
    if filename:
        with open(filename, 'w', encoding='utf-8') as json_file:
            jsonString = json.dumps(r.json(), indent=2)
            json_file.write(jsonString)
            logging.info("Adjustments file created")
    else:
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
    get_adjustments()(auto_envvar_prefix='FLEXERA')
