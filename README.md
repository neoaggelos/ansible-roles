# Ansible Collection - neoaggelos.common

Documentation for the `neoaggelos.common` collection.

This is a list of re-usable infrastructure-related Ansible roles.

| Role                      | Description                                                | Support                       |
| ------------------------- | ---------------------------------------------------------- | ----------------------------- |
| `apt_cacher`              | Setup a caching apt proxy                                  | Ubuntu                        |
| `apt_cacher_ng`           | Setup a caching apt proxy                                  | Ubuntu                        |
| `corosync`                | Setup a VIP resource using a Corosync cluster              | Ubuntu 18.04                  |
| `cron`                    | Setup cronjobs for system users                            | Ubuntu, CentOS, Rocky, Debian |
| `disable_tracker`         | Disable GNOME Tracker                                      | Ubuntu                        |
| `docker`                  | Install Docker and (optionally) Docker Compose             | Ubuntu, CentOS, Rocky, Debian |
| `docker_compose`          | Install Docker Compose                                     | Ubuntu, CentOS, Rocky, Debian |
| `etc_hosts`               | Configure entries in /etc/hosts                            | Ubuntu, CentOS, Rocky, Debian |
| `hostname`                | Configure host name                                        | Ubuntu, CentOS, Rocky, Debian |
| `k3s`                     | Configure a K3s cluster                                    | Ubuntu, CentOS, Rocky, Debian |
| `keepalived`              | Setup a VIP using Keepalived                               | Ubuntu, CentOS, Rocky, Debian |
| `kernel_modules_disable`  | Disable and blacklist Kernel modules                       | Ubuntu, CentOS, Rocky, Debian |
| `lvm_volume`              | Configure LVM volume group and logical volumes             | Ubuntu, CentOS, Rocky, Debian |
| `microk8s`                | Configure a MicroK8s cluster                               | Ubuntu, CentOS, Rocky, Debian |
| `netdata`                 | Configure netdata (and optional Slack alerts)              | Ubuntu                        |
| `netplan`                 | Configure netplan                                          | Ubuntu, CentOS, Rocky, Debian |
| `nginx`                   | Configure NGINX server, static files and servers           | Ubuntu, CentOS, Rocky, Debian |
| `nfs`                     | Configure NFS server and clients                           | Ubuntu, CentOS, Rocky, Debian |
| `nmcli`                   | Configure a NetworkManager connection using nmcli          | Ubuntu                        |
| `node_exporter_text_file` | Configure text file exporters for Node Exporter            | Ubuntu, CentOS, Rocky, Debian |
| `openstack_cloud`         | Bootstrap configuration for an OpenStack cloud             | `OpenStack`                   |
| `rke`                     | Configure a RKE cluster                                    | Ubuntu, CentOS, Rocky, Debian |
| `rke2`                    | Configure a RKE2 cluster                                   | Ubuntu, CentOS, Rocky, Debian |
| `ssh_access`              | Configure SSH access across machines of the same inventory | Ubuntu, CentOS, Rocky, Debian |
| `systemd_timesyncd_ntp`   | Configure NTP server for systemd-timesyncd                 | Ubuntu, CentOS, Rocky, Debian |
| `upgrades`                | Configure cron unattended upgrade schedule                 | Ubuntu, CentOS, Rocky, Debian |
| `users`                   | Configure users and SSH access                             | Ubuntu, CentOS, Rocky, Debian |
| `utils`                   | Install commonly needed server administration tools        | Ubuntu, CentOS, Rocky, Debian |
| `xrdp`                    | Install xRDP with the XFCE4 desktop                        | Ubuntu                        |
| `vpn_server`              | Configure OpenVPN server                                   | Ubuntu, CentOS, Debian        |
| `vpn_client`              | Configure OpenVPN clients (used along with `vpn_server`)   | Ubuntu, CentOS, Debian        |
| `wireguard`               | Configure WireGuard VPN                                    | Ubuntu                        |

See `defaults.yml` for configuration for each role.
