E->A sends lots of segments with upper [[TCP#^5e9227|SYN flag]]

# Defence
### SYN Cookies
Instead of storing the state of each [[TCP|SYN]] request in memory, the server generates a cookie and sends it back to the client in a [[TCP|SYN-ACK]] packet. This code contains the information needed to **restore** the connection state.
Server works with re-requesting [[TCP|ACKs]] with correct cookie 