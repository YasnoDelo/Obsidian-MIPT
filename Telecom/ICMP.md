**Internet Control Message Protocol** ^368160

In [[IPv6]] is necessary. In [[IPv4]] is not.

It has to [[Management plane|manage network]]. Gives information about sent packets and about devices status.   ^0137eb

### Messages:

| Cause                                                               | Message                                   |
| ------------------------------------------------------------------- | ----------------------------------------- |
| TTL = 0                                                             | TTL exceeded                              |
| [[IPv4#^082ef4\|DF]] = 1 (packet can't be fragment), packet too big | Packet too big                            |
| Firewall or permission denied                                       | Communication administratively prohibited |

^ab6721

### Structure
Type+Code+Checksum

## In IPv6
Works with [[NDP]]

RS - Router Solicitation
RA - Router Advertisement

NS - Neighbour Solicitation
RA - Neighbour Advertisement

Redirect