Do not pass [[Collision|collision]] thought itself ^42a8c6
### Switching modes
![[switching_modes.png]]

1) Always let all frames go after destination [[MAC]] came (Can't be used with [[VLAN]])
2) If first 64 bytes are correct - we let frame go (after 64 bytes [[Collision|collision]] can't occur because least devices listen environment and after 64 bytes they always hear signal and will not sent their data)
3) Make decision about sending after all bytes came

## L2 switch
Just commutation function. Problems occurs while using VLANs
![[L2switch_problems.jpg]]

## L3 switch
Hybrid device, implementing routing and commutation

![[L3_switch.jpg]]
**SVI** = switch virtual interface - interfaces type between L2 Switch and router in L3 Switch schema
### Commutation
Same with [[Router|router]]
### Routing
Same with [[Switch|switch]]

### Avoiding Loops Using [[STP]]
