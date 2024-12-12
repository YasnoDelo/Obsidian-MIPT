It is disturbance of encapsulation order.

## IPIP
Encapsulation of [[IPv4]] in [[IPv4]]

## IPIPv6
Encapsulation of [[IPv6]] in [[IPv4]]

## GRE
Additional layer between initial IP header and encapsulated one
![[GRE.jpg]]

### Tunnel setting
![[tunnel_exmp.jpg]]
1) A->R1 IP packet to B
2) R1 understands, that packet should be encapsulated. R1 encapsulates it
3) R1 -> R2 IP packet to B
4) R2 understands, that packet should be decapsulated. R2 decapsulates it
5) R2 -> B packet to B

### L2 tunnels
![[Ether_enc.jpg]]

Example in database topology:
![[Data_servers.jpg]]
