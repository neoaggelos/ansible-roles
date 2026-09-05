from ansible.module_utils.basic import AnsibleModule
import openstack

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
}

OPTIONS = {
    "router": {
        "type": "str",
        "required": True,
    },
    "subnet": {
        "type": "str",
        "required": True,
    },
    "state": {
        "type": "str",
        "default": "present",
        "choices": ["present", "absent"],
    },
    "openstack_connect_args": {
        "type": "dict",
        "required": False,
    },
}

DOCUMENTATION = """
---
module: os_router_subnet
short_description: Manage OpenStack router subnet attachments
version_added: "2.9"
description: |
    Configure router (by name or ID) attachments for a target subnet (by name or ID).
    Uses environment variables for OpenStack credentials.

author:
    - Aggelos Kolaitis (@neoaggelos)
"""

EXAMPLES = """
---
- hosts: localhost
  tasks:
    - os_router_subnet:
        router: shared-router
        subnet: my-subnet

---
- hosts: localhost
  tasks:
    - os_router_subnet:
        router: shared-router
        subnet: my-subnet
        state: absent

"""

RETURN = """
changed:
    type: bool
    description: Whether the router interfaces were changed
"""


def run_module():
    module = AnsibleModule(argument_spec=OPTIONS, supports_check_mode=False)

    router_name = module.params["router"]
    subnet_name = module.params["subnet"]
    state = module.params["state"]
    openstack_connect_args = module.params.get("openstack_connect_args") or {}

    c = openstack.connect(**openstack_connect_args)

    try:
        router_id = c.get_router(router_name).id
    except AttributeError:
        module.fail_json(f"router {router_name} could not be found")

    try:
        subnet = c.get_subnet(subnet_name)
    except AttributeError:
        module.fail_json(f"subnet {subnet_name} could not be found")

    router_ports = c.list_ports({"device_id": router_id, "network_id": subnet.network_id})
    router_subnet_ports = [p for p in router_ports if p.fixed_ips[0]["subnet_id"] == subnet.id]

    changed = False
    if state == "present" and not router_subnet_ports:
        c.add_router_interface(router_id, subnet_id=subnet.id)
        changed = True
    elif state == "absent" and router_subnet_ports:
        c.remove_router_interface(router_id, subnet_id=subnet.id)
        changed = True

    return module.exit_json(changed=changed)


if __name__ == "__main__":
    run_module()
