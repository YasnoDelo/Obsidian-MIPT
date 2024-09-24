Has it's own table of network structure. Divide network onto 2 sides. Do not pass collision through itself.  

### Example Table:

| MAC address | Interface | Time |
| ----------- | --------- | ---- |
| xxx         | Left      | 2.5  |
| yyy         | Right     | 3.6  |
| zzz         | Left      | 1000 |
| zzz         | Right     | 3.5  |
zzz is not valid knot in left interface - we can delete it!

"Time" make sense: we can understand in which interface is device connected now

### Terms
1) **Learning** - process of table fulling (by senders addresses)
2) **Forwarding** - process of finding addresses (by destination addresses)

If switch don't know device(unknown unicast), it makes broadcast 
