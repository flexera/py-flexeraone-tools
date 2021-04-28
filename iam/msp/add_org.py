import json
import logging
import requests
import sys
import time
import click
import sys
import urllib3
from urllib3.exceptions import InsecureRequestWarning


@click.command()
@click.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from CM or FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="https://api.flexeratest.com", show_default=True, required=False)
@click.option('--org-name', '-o', prompt="Organization Name", required=True)
@click.option('--first-name', '-f', prompt="Owner First Name", required=True)
@click.option('--last-name', '-l', prompt="Owner Last Name", required=True)
@click.option('--email','-e', prompt="Owner Email", required=True)
@click.option('--msp-org-id', '-m', prompt="MSP Org ID",required=True)

def cli(refresh_token,host,org_name,first_name,last_name,email,msp_org_id):
  # Tweak the destination (e.g. sys.stdout instead) and level (e.g. logging.DEBUG instead) to taste!
  logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', stream=sys.stderr, level=logging.INFO)
  access_token = auth(refresh_token,host)
  org_data = generate_org_data(org_name, first_name, last_name, email)
  create_response = create_org(host, access_token, msp_org_id, org_data)
  print(json.dumps(create_response))

def auth(refresh_token,host):
  if host == 'https://api.flexera.com':
    token_url = "https://login.flexera.com/oidc/token"
  else:
    token_url = "https://login.flexeratest.com/oidc/token"

  logging.info("OAuth2: Getting Access Token via Refresh Token...")
  r = requests.post(token_url, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
  r.raise_for_status()
  access_token = r.json()["access_token"]
  click.echo(access_token)
  return access_token

def generate_org_data(org_name, first_name, last_name, email):
  org_data = {
    name: org_name,
    owners: [ { "firstName": first_name, "lastName": last_name, "email": email } ],
    capabilities: [ { "Name": "optima" }, { "Name": "policy" }, {"Name": "fcm"}, {"Name": "fss"} ]
  }
  return org_data

def create_org(host, access_token, msp_org_id, org_data):
  headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
  kwargs = {"headers": headers, "allow_redirects": False}
  msp_url = "https://{}/msp/v1/orgs/{}/customers".format(host,msp_org_id)
  r = requests.post(msp_url, json.dumps(org_data), **kwargs)
  logging.info("Response: {}\n{}".format(r.status_code, json.dumps(r.json(), indent=4)))
  r.raise_for_status()
  return r.json()

if __name__ == '__main__':
  # click passes no args
  # pylint: disable=no-value-for-parameter
  cli()
