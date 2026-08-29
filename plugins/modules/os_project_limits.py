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
    "project": {
        "type": "str",
        "required": True,
    },
    "region": {
        "type": "str",
        "required": False,
    },
    "domain": {
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
module: os_project_limits
short_description: Manage OpenStack limits for projects
version_added: "2.9"
description: |
    Configure project limits for OpenStack services. Uses environment variables
    for OpenStack credentials.

    Note that:
    - Any limits must already be defined as registered limits (see os_registered_limits)
    - Each limit is configured with a separate non-atomic API call.

author:
    - Aggelos Kolaitis (@neoaggelos)
"""

EXAMPLES = """
---
- hosts: localhost
  tasks:
    - os_project_limits:
        service: nova
        region: RegionOne
        project: ProjectOne
        domain: ProjectDomain
        limits:
          servers: 2
          class:VCPU: 2
          class:MEMORY_MB: 2048

---
- hosts: localhost
  tasks:
    - os_project_limits:
        service: nova
        region: RegionOne
        project: ProjectOne
        domain: ProjectDomain
        limits:
          servers: 2
          class:VCPU: 2
          class:MEMORY_MB: 2048
          class:CUSTOM_PCI_10DE_15B3: 1

---
- hosts: localhost
  tasks:
    - os_project_limits:
        service: nova
        region: RegionOne
        project: ProjectOne
        domain: ProjectDomain
        limits:
          servers: absent
"""

RETURN = """
changed:
    type: bool
    description: Whether the limits were created and/or changed
limits:
    type: dict
    description: Updated project limits
"""


def run_module():
    module = AnsibleModule(argument_spec=OPTIONS, supports_check_mode=False)

    service_name = module.params["service"]
    project_name = module.params["project"]
    domain_name = module.params.get("domain")
    region_name = module.params.get("region")
    create_limits = module.params.get("limits", {})
    openstack_connect_args = module.params.get("openstack_connect_args", {})

    c = openstack.connect(**openstack_connect_args)

    try:
        service_id = c.get_service(service_name).id
    except AttributeError:
        module.fail_json(f"service {service_name} could not be found")

    try:
        domain_id = None
        if domain_name is not None:
            domain_id = c.get_domain(name_or_id=domain_name).id
    except AttributeError:
        module.fail_json(f"domain {domain_name} could not be found")

    try:
        project_id = c.get_project(project_name, domain_id=domain_id).id
    except AttributeError:
        module.fail_json(f"project {project_name} could not be found")

    region_id = None
    if region_name is not None:
        region_id = c.identity.get_region(region_name).id

    update_limits, delete_limits = {}, []
    for have in list(c.identity.limits(service_id=service_id, project_id=project_id)):
        if have.service_id != service_id or have.region_id != region_id:
            continue

        try:
            want = create_limits.pop(have.resource_name)
        except KeyError:
            continue

        if want == "absent":
            delete_limits.append(have.id)
        elif have.resource_limit != want:
            update_limits[have.id] = want

    create_limits = {k: v for k, v in create_limits.items() if v != "absent"}
    for key, value in create_limits.items():
        c.identity.create_limit(
            resource_name=key, project_id=project_id, service_id=service_id, region_id=region_id, resource_limit=value
        )
    for id, value in update_limits.items():
        c.identity.update_limit(limit=id, resource_limit=value)
    for id in delete_limits:
        c.identity.delete_limit(limit=id, ignore_missing=True)

    module.exit_json(
        changed=bool(create_limits or update_limits or delete_limits),
        limits={
            l.resource_name: l.resource_limit
            for l in c.identity.limits(service_id=service_id, project_id=project_id)
            if l.region_id == region_id
        },
    )


if __name__ == "__main__":
    run_module()
