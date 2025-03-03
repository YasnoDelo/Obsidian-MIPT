![[VRRP.jpg]]
### Roles
1) Master - main [[Router|router]], who is sending packets
2) Backup - backup of master
3) IP address owner - have IP, is master regardless of priority

### Some info
Broadcast = 224.0.0.18
VID MAC = 00:00:5E:00:01:XX => 255 groups
Advtimer = 1 sec

### Priority

| Num   | Description           |
| ----- | --------------------- |
| 1-254 | usual                 |
| 0     | definitely not Master |
| 255   | obviously Master      |
| 100   | default               |
### Preempt
1) If [[Router|router]]  is not available while downtimer (3 sec) - classic reroling
2) If master available, but there is [[Router|router]] with preempt setting and higher priority.

### VRRP states
1) Initial (link up or election or another state)
2) Standby (know who is active. he isn't)
3) Active