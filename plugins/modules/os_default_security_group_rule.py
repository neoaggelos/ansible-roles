from ansible.module_utils.basic import AnsibleModule
import openstack

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
}

OPTIONS = {
    "state": {
        "type": "str",
        "default": "present",
        "choices": ["present", "absent"],
    },
    "description": {
        "type": "str",
        "default": "",
    },
    "ether_type": {
        "type": "str",
        "default": "IPv4",
        "choices": ["IPv4", "IPv6"],
    },
    "direction": {
        "type": "str",
        "default": "ingress",
        "choices": ["ingress", "egress"],
    },
    "protocol": {},
    "port_range_min": {
        "type": "int",
    },
    "port_range_max": {
        "type": "int",
    },
    "remote_ip_prefix": {},
    "remote_address_group_id": {},
    "remote_group_id": {},
    "used_in_default_sg": {
        "type": "bool",
        "default": True,
    },
    "used_in_non_default_sg": {
        "type": "bool",
        "default": False,
    },
    "openstack_connect_args": {
        "type": "dict",
        "required": False,
    },
}

DOCUMENTATION = """
---
module: os_default_security_group_rule
short_description: Manage OpenStack default security group rules
version_added: "2.9"
description: |
    Configure default security group rules for OpenStack. These are inherited by any
    security group that is created. Uses environment variables for OpenStack credentials.

    Existing security group rules are matched based on equality of all fields except state,
    description, used_in_default_sg and used_in_non_default_sg.

author:
    - Aggelos Kolaitis (@neoaggelos)
"""

EXAMPLES = """
---
- hosts: localhost
  tasks:
  - os_default_security_group_rule:
      protocol: tcp
      port_range_min: 22
      port_range_max: 22
      remote_group_id: PARENT
      used_in_default_sg: true
      used_in_non_default_sg: true

---
- hosts: localhost
  tasks:
  - os_default_security_group_rule:
      protocol: tcp
      port_range_min: 22
      port_range_max: 22
      remote_group_id: PARENT
      state: absent


"""

RETURN = """
changed:
    type: bool
    description: Whether the default security group rules were changed
"""


def run_module():
    module = AnsibleModule(argument_spec=OPTIONS, supports_check_mode=False)

    state = module.params["state"]
    description = module.params.get("description")
    ether_type = module.params["ether_type"]
    direction = module.params["direction"]
    protocol = module.params.get("protocol")
    port_range_min = module.params.get("port_range_min")
    port_range_max = module.params.get("port_range_max")
    remote_ip_prefix = module.params.get("remote_ip_prefix")
    remote_address_group_id = module.params.get("remote_address_group_id")
    remote_group_id = module.params.get("remote_group_id")
    used_in_default_sg = module.params.get("used_in_default_sg")
    used_in_non_default_sg = module.params.get("used_in_non_default_sg")

    openstack_connect_args = module.params.get("openstack_connect_args") or {}

    c = openstack.connect(**openstack_connect_args)

    match = None
    for rule in list(c.network.default_security_group_rules()):
        if rule.ether_type != ether_type:
            continue
        if rule.direction != direction:
            continue
        if rule.protocol != protocol:
            continue
        if rule.port_range_min != port_range_min:
            continue
        if rule.port_range_max != port_range_max:
            continue
        if rule.remote_ip_prefix != remote_ip_prefix:
            continue
        if rule.remote_address_group_id != remote_address_group_id:
            continue
        if rule.remote_group_id != remote_group_id:
            continue

        match = rule
        break

    changed = False
    if state == "absent" and match is not None:
        c.network.delete_default_security_group_rule(default_security_group_rule=match.id, ignore_missing=True)
        changed = True
    elif state == "present":
        changed = True
        if match is not None:
            if description and match.description != description:
                c.delete_default_security_group_rule(match.id)
            elif used_in_default_sg is not None and match.used_in_default_sg != used_in_default_sg:
                c.delete_default_security_group_rule(match.id)
            elif used_in_non_default_sg is not None and match.used_in_non_default_sg != used_in_non_default_sg:
                c.delete_default_security_group_rule(match.id)
            else:
                changed = False

        if changed:
            c.network.create_default_security_group_rule(
                description=description or "managed by ansible",
                ether_type=ether_type,
                direction=direction,
                protocol=protocol,
                port_range_min=port_range_min,
                port_range_max=port_range_max,
                remote_ip_prefix=remote_ip_prefix,
                remote_address_group_id=remote_address_group_id,
                remote_group_id=remote_group_id,
                used_in_default_sg=used_in_default_sg,
                used_in_non_default_sg=used_in_non_default_sg,
            )

    return module.exit_json(changed=changed)


if __name__ == "__main__":
    run_module()
