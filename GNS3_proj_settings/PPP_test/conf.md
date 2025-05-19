R1
```
conf t

username  R2 password pass

int s3/2
ip add 1.1.1.1 255.255.255.0
no sh
enc ppp

ppp authe chap
ppp chap hostname R1
ppp chap password pass


```
R2
```

conf t

int s3/1
ip add 1.1.1.2 255.255.255.0
enc ppp
no sh

ppp chap hostname R2
ppp chap password pass

int s3/3
enc ppp
no sh
ip add 2.2.2.2 255.255.255.0

ppp pap sent R2 pass pass


  
```

R3

```
conf t

username R2 password pass
int s3/2
enc ppp
no sh
ip add 2.2.2.3 255.255.255.252
ppp authe pap

//шазосоединение на L2
int s3/2
ppp chap hostname R3
ppp chap password pass
```

R5-R6
```
int s4/0
ip add 1.1.1.1 255.255.255.0
no sh
enc ppp
```

```
int s4/0
ip add 2.1.1.1 255.255.255.0
no sh
enc ppp
```
