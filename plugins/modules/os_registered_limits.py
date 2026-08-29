from ansible.module_utils.basic import AnsibleModule
import openstack

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
}

OPTIONS = {
    "service": {
        "type": "str",
        "required": True,
    },
    "region": {
        "type": "str",
        "required": False,
    },
    "limits": {
        "type": "dict",
        "required": False,
    },
    "openstack_connect_args": {
        "type": "dict",
        "required": False,
    },
}

DOCUMENTATION = """
---
module: os_registered_limits
short_description: Manage OpenStack registered limits
version_added: "2.9"
description: |
    Configure Registered Limits for OpenStack services. Uses environment variables
    for OpenStack credentials.

    Note that each registered limit is configured with a separate non-atomic API call.

author:
    - Aggelos Kolaitis (@neoaggelos)
"""

EXAMPLES = """
---
- hosts: localhost
  tasks:
    - os_registered_limits:
        service: nova
        region: RegionOne
        limits:
          servers: 2
          class:VCPU: 2
          class:MEMORY_MB: 2048

---
- hosts: localhost
  tasks:
    - os_registered_limits:
        service: nova
        region: RegionOne
        limits:
          servers: 2
          class:VCPU: 2
          class:MEMORY_MB: 2048
          class:CUSTOM_PCI_10DE_15B3: 1

---
- hosts: localhost
  tasks:
    - os_registered_limits:
        service: nova
        limits:
          servers: absent
"""

RETURN = """
changed:
    type: bool
    description: Whether the limits were created and/or changed
limits:
    type: dict
    description: Updated service registered limits
"""


def run_module():
    module = AnsibleModule(argument_spec=OPTIONS, supports_check_mode=False)

    service_name = module.params["service"]
    region_name = module.params.get("region")
    create_limits = module.params.get("limits", {})
    openstack_connect_args = module.params.get("openstack_connect_args", {})

    c = openstack.connect(**openstack_connect_args)

    service_id = c.get_service(service_name).id
    region_id = None
    if region_name is not None:
        region_id = c.identity.get_region(region_name).id

    update_limits, delete_limits = {}, []
    for have in list(c.identity.registered_limits()):
        if have.service_id != service_id or have.region_id != region_id:
            continue

        try:
            want = create_limits.pop(have.resource_name)
        except KeyError:
            continue

        if want == "absent":
            delete_limits.append(have.id)
        elif have.default_limit != want:
            update_limits[have.id] = want

    create_limits = {k: v for k, v in create_limits.items() if v != "absent"}
    for key, value in create_limits.items():
        c.identity.create_registered_limit(
            resource_name=key, service_id=service_id, region_id=region_id, default_limit=value
        )
    for id, value in update_limits.items():
        c.identity.update_registered_limit(registered_limit=id, default_limit=value)
    for id in delete_limits:
        c.identity.delete_registered_limit(registered_limit=id, ignore_missing=True)

    module.exit_json(
        changed=bool(create_limits or update_limits or delete_limits),
        limits={
            l.resource_name: l.default_limit
            for l in c.identity.registered_limits()
            if l.service_id == service_id and l.region_id == region_id
        },
    )


if __name__ == "__main__":
    run_module()
