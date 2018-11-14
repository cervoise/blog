This post is about this VM:
* https://www.rebootuser.com/?p=1307
* https://www.vulnhub.com/entry/hacklab-vulnvpn,49/

This is not a write-up or a solution for the VM (availalbe here: https://www.rebootuser.com/?p=1474), just a doc about setting up the VPN through Kali:

Some error message I got:
```
E: Package 'openswan' has no installation candidate
whack: Pluto is not running (no "/run/pluto/pluto.ctl")
bash: /var/run/xl2tpd/l2tp-control: No such file or directory
```


```
# apt-get install libreswan xl2tpd ppp
# wget http://www.rebootuser.com/wp-content/uploadsipsec auto –up vpn/vulnvpn/client.7z
# p7zip -d client.7z 
# cd client
```
Edit the ipsec.secrets file with the PSK you cracked.

```
# cp ipsec.conf /etc/ipsec.conf
# cp ipsec.secrets /etc/ipsec.secrets
# cp ppp/options.l2tpd.client /etc/ppp/options.l2tpd.client
# cp xl2tpd/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf
# service ipsec restart
# ipsec auto -–up vpn
```

And then something must be done with xl2tpd but is not working. If you have any clue for make it works on a recent Kali I'll be happy to try it!
