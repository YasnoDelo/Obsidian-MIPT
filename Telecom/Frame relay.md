1) Outdated (just in the old networks)
2) NBMA (Non-Broadcast multiple access) (for example [[Ethernet]] is BMA)
3) All logic links are under provider's control

### Physical topology
![[FR.png]]

[[DCE]] - Data Communication Equipment - provider's stuff 
[[DTE]] - Data Terminal Equipment - clients' stuff
[[DCE]] and [[DTE]] are connected by serial access link

[[LMI]] - local management interface - protocol for communication between [[DCE]] and [[DTE]]
Can be [[DCE]] and [[DTE]] on L2 and L1 (and [[DCE]] on L1 can be [[DTE]] on L2)
### Logical topology
![[VC.jpg]]
[[VC]] - Virtual Circuit - logical neighbourhood. Can be Permanent (static, sets up by hands) or Software (dynamic, sets up by software) (like [[VPN]])

[[Access Control List]] is one on interface (for all [[VC]]) 

[[DLCI]] (Data Link Connection Identifier) - analogy of [[MAC]]. Connection identifier.