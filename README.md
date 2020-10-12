# conkyberry
Web application developed with Python and ReactJS for monitoring Raspberry Pi 4 model B.


## Installation
```
sudo apt-get install vnstat net-tools
sudo nano /etc/vnstat.conf # select interface
sudo vnstat -i eth0 # create database for interface
sudo systemctl status vnstat.service # check if service is running
vnstat
```

If you see next message: Not enough data available yet.

By default, when you install vnstat, it auto starts a vnstatd daemon, 
which collects metrics every 30 seconds and "updates them" (for all local devices)
every 5 minutes. So in essence, after installing vnstat packet, you should start to see metrics 5 minutes later.

https://askubuntu.com/questions/500663/vnstat-not-updating
