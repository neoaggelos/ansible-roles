# Ansible Collection - neoaggelos.common

Documentation for the `neoaggelos.common` collection.

This is a list of re-usable infrastructure-related Ansible roles.

| Role                      | Description                                                | Support                |
| ------------------------- | ---------------------------------------------------------- | ---------------------- |
| `corosync`                | Setup a VIP resource using a Corosync cluster              | Ubuntu 18.04           |
| `disable_tracker`         | Disable GNOME Tracker                                      | Ubuntu                 |
| `docker`                  | Install Docker and (optionally) Docker Compose             | Ubuntu, CentOS, Debian |
| `etc_hosts`               | Configure entries in /etc/hosts                            | Ubuntu, CentOS, Debian |
| `hostname`                | Configure host name                                        | Ubuntu, CentOS, Debian |
| `k3s`                     | Configure a K3s cluster                                    | Ubuntu, CentOS, Debian |
| `keepalived`              | Setup a VIP using Keepalived                               | Ubuntu, CentOS, Debian |
| `kernel_modules_disable`  | Disable and blacklist Kernel modules                       | Ubuntu, CentOS, Debian |
| `lvm_volume`              | Configure LVM volume group and logical volumes             | Ubuntu, CentOS, Debian |
| `microk8s`                | Configure a MicroK8s cluster                               | Ubuntu, CentOS, Debian |
| `netdata`                 | Configure netdata (and optional Slack alerts)              | Ubuntu                 |
| `nfs`                     | Configure NFS server and clients                           | Ubuntu, CentOS, Debian |
| `nmcli`                   | Configure a NetworkManager connection using nmcli          | Ubuntu                 |
| `node_exporter_text_file` | Configure text file exporters for Node Exporter            | Ubuntu, CentOS, Debian |
| `openstack_cloud`         | Bootstrap configuration for an OpenStack cloud             | `OpenStack`            |
| `rke`                     | Configure a RKE cluster                                    | Ubuntu, CentOS, Debian |
| `rke2`                    | Configure a RKE2 cluster                                   | Ubuntu, CentOS, Debian |
| `ssh_access`              | Configure SSH access across machines of the same inventory | Ubuntu, CentOS, Debian |
| `upgrades`                | Configure cron unattended upgrade schedule                 | Ubuntu, CentOS, Debian |
| `users`                   | Configure users and SSH access                             | Ubuntu, CentOS, Debian |
| `utils`                   | Install commonly needed server administration tools        | Ubuntu, CentOS, Debian |
| `xrdp`                    | Install xRDP with the XFCE4 desktop                        | Ubuntu                 |
| `vpn_server`              | Configure OpenVPN server                                   | Ubuntu, CentOS, Debian |
| `vpn_client`              | Configure OpenVPN clients (used along with `vpn_server`)   | Ubuntu, CentOS, Debian |

See `defaults.yml` for configuration for each role.
