iptables
=========

Installs iptables, disable the other firewall services and initialize an easy way
to setup rules by specifying a list of directives.

Requirements
------------

None

Role Variables
--------------

```
iptables_v4_policy:
  input: ACCEPT
  output: ACCEPT
  forward: DROP
```
A dict of default filter policy.
```
iptables_security:
  accept_icmp_reply: true
  ignore_bogus_tcp: true
  prevent_port_scan: false
```
A dict of security policy.
```
iptables_allowed_client_ports
  - { port: 25, protocol: tcp }
  - { port: 53, protocol: tcp  }
  - { port: 80, protocol: tcp }
```
A list of TCP or UDP ports to open to outgoing traffic; if `iptables_v*_policy.output` was `ACCEPT`, this list would be unavailable.
```
iptables_allowed_server_ports:
  - { port: 22, protocol: tcp }
```
A list of TCP or UDP ports to open to incoming traffic; if `iptables_v*_policy.input` was `ACCEPT`, this list would be unavailable.

Dependencies
------------

None

Example Playbook
----------------
```
- hosts: all
  vars:
    iptables_strict_mode: false
    iptables_v4_policy:
      input: DROP
      output: DROP
      forward: DROP
    iptables_allowed_client_ports:
      - { port: 22, protocol: tcp }  # ssh-client
      - { port: 25, protocol: tcp }  # smtp
      - { port: 53, protocol: tcp  } # dns
      - { port: 53, protocol: udp }  
      - { port: 80, protocol: tcp }  # http
      - { port: 123, protocol: tcp } # ntp
      - { port: 123, protocol: udp }
      - { port: 443, protocol: tcp } # https
    iptables_allowed_server_ports:
      - { port: 22, protocol: tcp } # ssh-server

  roles:
    - role: ivoamorim.iptables
```

License
-------

BSD
