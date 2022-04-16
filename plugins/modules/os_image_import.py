#!/usr/bin/env python3

import urllib.request

from ansible.module_utils.basic import AnsibleModule
import openstack

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
}

OPTIONS = {
    "name": {
        "type": "str",
        "required": True,
    },
    "url": {
        "type": "str",
        "required": True,
    },
    "visibility": {
        "type": "str",
        "required": False,
        "default": "public",
    },
    "disk_format": {
        "type": "str",
        "required": True,
    },
    "container_format": {
        "type": "str",
        "required": True,
    },
    "metadata": {
        "type": "dict",
        "required": False,
    },
}

DOCUMENTATION = """
---
module: os_image_import
short_description: Import image to OpenStack glance
version_added: "2.9"
description: |
    Import image from URL to OpenStack glance. Uses environment variables
    for OpenStack credentials.

author:
    - Aggelos Kolaitis (@neoaggelos)
"""

EXAMPLES = """
---
- hosts: localhost
  tasks:
    - os_image_import:
        name: cirros
        url: http://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img
        disk_format: qcow2
        container_format: bare
        visibility: public
        metadata:
          architecture: x86_64
          hypervisor_type: qemu
          os_distro: cirros
          os_version: '0.5.2'
---
- hosts: localhost
  tasks:
    - os_image_import:
        name: ubuntu-18.04
        url: https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img
        disk_format: qcow2
        container_format: bare
        visibility: public
        metadata:
          architecture: x86_64
          hypervisor_type: qemu
          os_distro: ubuntu
          os_version: '18.04'
"""

RETURN = """
changed:
    type: bool
    description: Whether the image was changed
image_id:
    type: str
    description: Image ID
metadata:
    type: dict
    description: Created image metadata
"""


def run_module():
    module = AnsibleModule(argument_spec=OPTIONS, supports_check_mode=True)

    image_name = module.params["name"]
    image_url = module.params["url"]
    disk_format = module.params["disk_format"]
    container_format = module.params["container_format"]
    visibility = module.params["visibility"]
    metadata = module.params.get("metadata", {})
    changed = False

    c = openstack.connect()
    image = c.get_image(module.params["name"])

    if image is None:
        image = c.create_image(
            name=image_name,
            meta=metadata,
            disk_format=disk_format,
            container_format=container_format,
            visibility=visibility,
        )
        changed = True
    else:
        for key, value in metadata.items():
            if value != image.metadata.get(key):
                c.update_image_properties(image=image, meta=metadata)
                changed = True
                break

        if image.visibility != visibility:
            c.image.update_image(image=image, visibility=visibility)
            changed = True

    expected_image_size = urllib.request.urlopen(image_url).headers.get("content-length")
    if not expected_image_size or expected_image_size != str(image.size):
        c.image.import_image(image=image, method="web-download", uri=image_url)
        changed = True

    module.exit_json(
        image_id=image.id,
        image_metadata=image.metadata,
        changed=changed,
    )


if __name__ == "__main__":
    run_module()
