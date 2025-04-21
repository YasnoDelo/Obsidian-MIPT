Type of [[Firewall]].

- Software on Cisco IOS
- Interfaces assigned to zones
- Security politic are applied between zones

Like [[Access Control List]], but interfaces are replaced by zones

It's flexible, granular and efficient configuration.

### Security zones
- Area/region of the same relative security in the network. 
- Interface can be assigned to only one zone
- All interfaces in one zone are protected by the same level of security
- Zone can contain $\geq$  1 interface
#### Types of zones
1) Inside zone - zone of high confidence, all devices here are our own. ^7ba8f6
2) Outside zone - zone leading to unprofitable sources. ^9eb742
3) DMZ - demilitarised zone - something between first two ones. Here are servers. ^55dfaf
4) Self zone - special type of zone of the router (is by default), in which only the router itself is located (its Control Plane). Traffic, aimed at any IP address of the router itself, or generated from it, enters or, accordingly, leaves Self-Zone. ^5c48ce

#### Zone rule
- By default traffic is cancelled (not in [[Zone based firewall#^5c48ce|self zone]]).
- Inside one zone traffic is allowed.
- In [[Zone based firewall#^5c48ce|self zone]] by default all traffic is allowed. That is, it does not matter where a message is coming from in the [[Zone based firewall#^5c48ce|self zone]] or where a message is going from the [[Zone based firewall#^5c48ce|self zone]].
- The policy is applied to two zones taking into account the direction of.

#### Algorithm
1) Define zones (Example: [[Zone based firewall#^7ba8f6|IN]], [[Zone based firewall#^9eb742|OUT]], [[Zone based firewall#^55dfaf|DMZ]])
2) Define zone pairs ([[Zone based firewall#^7ba8f6|IN]]-[[Zone based firewall#^55dfaf|DMZ]], [[Zone based firewall#^7ba8f6|IN]]-[[Zone based firewall#^9eb742|OUT]], [[Zone based firewall#^9eb742|OUT]]-[[Zone based firewall#^55dfaf|DMZ]])
3) Define traffic types (class maps)
4) Define policies to different traffic types (policy-map)
5) Apply policy-map to zone pairs
6) Apply interfaces to zones