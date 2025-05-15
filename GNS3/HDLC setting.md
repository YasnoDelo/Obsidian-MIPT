
| command                               | discriptoin                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `encapsulation hdlc`                  | Выставить нужную инкапсуляцию                                                                    |
| `show controllers` + serial<br>number | Lists whether a cable is connected to the interface, and if so, whether it is a DTE or DCE cable |
| `clock rate`                          | Установить на DCE скорость передачи (в GNS3 все считают, что они DCE)                            |
|                                       |                                                                                                  |
R1
```
conf t

int s3/4
enc hdlc - по умолчанию
ip add 192.168.0.1 255.255.255.0
no sh
```

R2
```
conf t

int s3/4
enc hdlc - по умолчанию
ip add 192.168.0.2 255.255.255.0
no sh
```