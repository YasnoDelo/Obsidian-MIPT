### Reasons
1) People need more IP addresses
2) Slow routing

Length = 128 bit

#Example 
$$2001:2002:2003:2004:2005:2006:2007:2008$$$$2001:2002:0000:0000:0000:2006:0000:2008=2001:2002:0:0:0:2006:0:2008$$
$$2001:2002:0:0:0:2006:0:2008= 2001::2006:0:2008$$
==::== decrease length of IP. It means several $0000$. Can be used once in one IP


| address   | meaning         |
| --------- | --------------- |
| `::/0`    | default gateway |
| `::1/128` | loopback        |
|           |                 |

### Types of IP
![[types_of_ipv6.jpg]]


| Type         | Addresse                   | Description                                                                                                                                                       |
| ------------ | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unicast:     |                            |                                                                                                                                                                   |
| Global       | `2000::/3`                 | as white addresses in [[IPv4]]                                                                                                                                    |
| Link local   | `FE80::/10`                | as grey in [[IPv4]], doesn't [[Routing\|routing]], do not cross over [[Router\|Routers]]. Network needs it for [[Control plane\|control plane's protocols]] using |
| Unique local | `FC00::/7`                 | as grey addresses in [[IPv4]], but can be [[Routing\|routing]]                                                                                                    |
|              |                            |                                                                                                                                                                   |
| Multicast:   |                            |                                                                                                                                                                   |
| Assigned     |                            |                                                                                                                                                                   |
| Solicited    | `FF2:0:0:0:0:1:FF00::/104` |                                                                                                                                                                   |

### Address distribution
![[IPv6_distribution.jpg]]

==Standard subnet prefix = /64==

### Some advantages
1) Address assignment
2) Built-in support for address renumbering
3) Built-in support for mobility
4) Provider independent and dependent public address space
5) Aggregation
6) No need for [[NAT]]/[[PAT]]
7) IPSec
8) Header Improvement
9) No broadcasts
10) Transition tools

### Header 
![[IPv6_header-en.svg.png]]

### Methods of define IP address on port
1) [[DHCP]] (stateful)
2) [[DHCP]] (stateless)  - stateless autoconfig ([[DHCP|DHCP server]] sends specific [[ICMP]]-requests with prefix /64, least 64 bits calculate from [[MAC]] by [[EUI-64]])
3) Static autoconfig (first 64 bits set by admin)
4) Static
5) SLAAC (half of prefix from [[NDP]], second half - from [[EUI-64]])


