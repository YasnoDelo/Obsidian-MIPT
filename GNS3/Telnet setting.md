На клиенте:
```
telnet + ip_num + port (можно без порта)
```
### 1 способ
```
line vty 0 1869
login local
```
In [[Global config mode]] (not in config-line)
```
username usr secret pwd
username cisco secret cisco     //-инициализация пользователя
enable secret cisco             //-разрешения входа в привелегированный режим
```
### 2 способ
На сервере:
```
line vty 0 1869
  password pass
  login
