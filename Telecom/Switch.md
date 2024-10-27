Do not pass [[Collision|collision]] thought itself ^42a8c6
### Switching modes
![[switching_modes.png]]

1) Always let all frames go after destination [[MAC]] came (Can't be used with [[VLAN]])
2) If first 64 bytes are correct - we let frame go (after 64 bytes [[Collision|collision]] can't occur because least devices listen environment and after 64 bytes they always hear signal and will not sent their data)
3) Make decision about sending after all bytes came



