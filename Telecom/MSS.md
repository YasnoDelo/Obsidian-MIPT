Technology in [[TCP]] (one of [[TCP|TCP options]])

[[Router]] is able to change [[MTU]] value

1) Connection initiation:
	The client sends a SYN packet to the server to initiate a [[TCP]] connection.
2) Include the [[MSS]] option:
	The client includes the [[TCP]] [[MSS]] option in the SYN packet, indicating the maximum segment size it is willing to accept.
3) [[Router]] intervention:
	A router along the way can look at the [[TCP|TCP options]] and replace the value in the [[MSS]] field with one it supports
	If the [[Router|router]] does not do this, the Server will



