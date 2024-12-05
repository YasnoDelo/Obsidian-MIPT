**Dynamic Host Configuration Protocol**

### The main task

^ea08f6

To give IP-address ^e5638b

### Algorithm
![[DHCP.jpg]]

| D   | Discover        |
| --- | --------------- |
| O   | Offer           |
| R   | Request         |
| A   | Acknowledgement |
1) As in the picture (server understand is address empty sending [[ICMP]]-ping, but another client might use this address and [[Firewall]], which blocks [[ICMP]]-requests)
2) Client after taking IP-address checks - is it empty, sending [[ARP]]-request, which can't be blocked. If Address blocked, there is special message to [[DHCP]]-server (decline) 

| message | meaning               |
| ------- | --------------------- |
| DECLINE | refusal of IP address |
| NAK     |                       |
| RELEASE |                       |

### If we want to give one client one IP address always
There is option 82 in Discover message added by [[Switch]] (it has to be configured)

The switch is configured via the port config

This option tells the DHCP server that the device should be given a specific IP address

## For IPv6
### Stateful
As in [[IPv4]]
### Stateless
Without control from [[DHCP]]-server

