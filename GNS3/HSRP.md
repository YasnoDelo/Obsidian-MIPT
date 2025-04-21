`do sh standby br` - посмотреть информацию

R1
```
standby 1 ip 192.168.10.123
standby 1 preempt
standby 1 timers 3 10

/// 1 - номер группы
```

Можно использовать `standby 1 track 1 decrement 20`, где [[Track|track]] это некоторое отслеживаемое условие 


