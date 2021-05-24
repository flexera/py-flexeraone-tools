# Table of Contents

* [add\_org](#add_org)
  * [add\_iam\_msp\_org](#add_org.add_iam_msp_org)
  * [generate\_access\_token](#add_org.generate_access_token)
  * [generate\_org\_data](#add_org.generate_org_data)
  * [create\_org](#add_org.create_org)
* [del\_org](#del_org)
  * [del\_iam\_msp\_org](#del_org.del_iam_msp_org)
* [list\_orgs](#list_orgs)
  * [list\_iam\_msp\_orgs](#list_orgs.list_iam_msp_orgs)
* [update\_org](#update_org)
  * [update\_iam\_msp\_org](#update_org.update_iam_msp_org)

<a name="add_org"></a>
# add\_org

<a name="add_org.add_iam_msp_org"></a>
#### add\_iam\_msp\_org

```python
@click.command(no_args_is_help=True)
@click.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@click.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@click.option('--org-name', '-n', prompt="Organization Name", help="Organization Name", required=True)
@click.option('--first-name', '-f', prompt="Owner First Name", help="Owner First Name", required=True)
@click.option('--last-name', '-l', prompt="Owner Last Name", help="Owner Last Name", required=True)
@click.option('--email', '-e', prompt="Owner Email", help="Owner Email", required=True)
@click.option('--msp-org-id', '-m', prompt="MSP Org ID", help="MSP Org ID", required=True)
@click.option('--capabilities', '-o', prompt="Capability to Enable", required=True, multiple=True, type=click.Choice(flexera_capabilities))
add_iam_msp_org(refresh_token, host, org_name, first_name, last_name, email, msp_org_id, capabilities)
```

\b
Organization Add Tool for MSP's

<a name="add_org.generate_access_token"></a>
#### generate\_access\_token

```python
generate_access_token(refresh_token, host)
```

auth(refresh_token, host)
Authenticates againsts the FlexeraOne API and returns the access token

<a name="add_org.generate_org_data"></a>
#### generate\_org\_data

```python
generate_org_data(org_name, first_name, last_name, email, capabilities)
```

generate_org_data(org_name, first_name, last_name, email, capabilities)
Generates org create data from inputs and returns org data object.

<a name="add_org.create_org"></a>
#### create\_org

```python
create_org(host, access_token, msp_org_id, org_data)
```

create_org(host, access_token, msp_org_id, org_data)
Creates the org and logs the response.

<a name="del_org"></a>
# del\_org

<a name="del_org.del_iam_msp_org"></a>
#### del\_iam\_msp\_org

```python
@click.command(no_args_is_help=True)
@optgroup.group('Connection configuration',
                help='The configuration of some server connection')
@optgroup.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@optgroup.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@optgroup.option('--msp-org-id', '-m', prompt="MSP Org ID", help="MSP Org ID", required=True)
@optgroup.option('--org-id', '-o', prompt="Org ID to Delete", help="Org ID to Delete", required=True)
del_iam_msp_org(**params)
```

\b
Organization Delete Tool for MSP's

<a name="list_orgs"></a>
# list\_orgs

<a name="list_orgs.list_iam_msp_orgs"></a>
#### list\_iam\_msp\_orgs

```python
@click.command(no_args_is_help=True)
@optgroup.group('Connection configuration',
                help='The configuration of some server connection')
@optgroup.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@optgroup.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@optgroup.option('--msp-org-id', '-m', prompt="MSP Org ID", help="MSP Org ID", required=True)
@optgroup.option('--filename', '-f', help="Filename to save results to.")
@optgroup.group('Org Options', cls=MutuallyExclusiveOptionGroup,
                help='Org Options, either id or name')
@optgroup.option('--org-id', '-o', help='Org ID to Get')
@optgroup.option('--org-name', '-n', help="Organization Name to find. Using the name will only print close orgs")
list_iam_msp_orgs(**params)
```

\b
Lists Organizations and allows search by name

<a name="update_org"></a>
# update\_org

<a name="update_org.update_iam_msp_org"></a>
#### update\_iam\_msp\_org

```python
@click.command(no_args_is_help=True)
@optgroup.group('Connection configuration',
                help='The configuration of some server connection')
@optgroup.option('--refresh-token', prompt="Refresh Token", help='Refresh Token from FlexeraOne', required=True)
@optgroup.option('--host', '-h', prompt="IAM API Endpoint", default="api.flexeratest.com", show_default=True)
@optgroup.option('--msp-org-id', '-m', prompt="MSP Org ID", help="MSP Org ID", required=True)
@optgroup.option('--org-id', '-o', prompt='Org ID to update', help='Org ID to update', required=True)
@optgroup.option('--filename', '-f', prompt="JSON file with settings", help="JSON file with settings", required=True)
update_iam_msp_org(**params)
```

\b
MSP Organization update tool.

