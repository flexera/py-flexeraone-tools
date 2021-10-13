import json
import logging
import requests
import sys
import click
import pprint

@click.command(no_args_is_help=True)
@click.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-id', '-i', prompt="Organization ID", help="Organization ID", required=True)
@click.option('--id', prompt="ID", help="ID", required=True)
@click.option('--role-arn', prompt='Role Arn', required=True)
@click.option('--role-session-name', prompt='Role Session Name', required=True)
def create_credentials(refresh_token, host, org_id, id, role_arn, role_session_name):
    """
    Organization Add Tool for MSP's
    """
    # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
    access_token = generate_access_token(refresh_token, host)
    credential_data = {
        "name": id,
        "rolearn": role_arn,
        "rolesessionname": role_session_name,
        "tags": [
            {
                "key": "provider",
                "value": "aws"
            }
        ]
    }
    create_credential(host, access_token, org_id, id, credential_data)

def generate_access_token(refresh_token, host):
    domain = '.'.join(host.split('.')[-2:])
    token_url = "https://login.{}/oidc/token".format(domain)

    logging.info("OAuth2: Getting Access Token via Refresh Token for {} ...".format(token_url))
    token_post_request = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_post_request.raise_for_status()
    access_token = token_post_request.json()["access_token"]
    return access_token

def create_credential(host, access_token, org_id, id, credential_data):
    """
    create_org(host, access_token, msp_org_id, org_data)
    Creates the org and logs the response.
    """
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    kwargs = {"headers": headers, "allow_redirects": False}
    credential_service_url = "https://{}/cred/v1/orgs/{}/credentials/aws_sts/{}".format(host, org_id, id)
    try:
        create_cred_request = requests.put(credential_service_url, json.dumps(credential_data), **kwargs, stream=True)
        create_cred_request.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error Response: {}".format(e.response.text))
        raise SystemExit(e)
    logging.info("Code: {}\nHeaders: {}\n".format(create_cred_request.status_code, create_cred_request.headers))
    new_cred_url = "https://{}{}".format(host, create_cred_request.headers['location'])
    get_response = requests.get(new_cred_url, **kwargs)
    get_response.raise_for_status()
    logging.info("Response: {}\nHeaders: {}\n".format(get_response.status_code, get_response.headers))
    pprint.pprint(get_response.json())


if __name__ == '__main__':
    # click passes no args
    # pylint: disable=no-value-for-parameter
    create_credentials(auto_envvar_prefix='FLEXERA')
