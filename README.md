
# Django firewall

This firewall is for linux using iptablewhich is installed as CLI firewall on every GNU/Linux system.  We created this web application to allow people whom are not familiar with linux terminal ans it will make firewall configuaration easy and  directly from the browser  to be set properly an quickly and easily. This is a project for us at our university and it still simple but we are  trying to do our best to mprove version of this firewallon the future.

## Installation

check if iptables is installed

```bash
  sudo iptables -L -n -v
```
    
if it is not installed, install this on the terminal:
## Debian/Ubuntu

```bash
sudo apt-get install iptables

```

## Arch based

```bash
sudo pacman -S install iptables

```
## Fedora

```bash
sudo dnf install iptables

```
## installer les dependences

```bash
pip install -r requirements.txt

```


## Authors

- [@Nomentsoa](https://www.github.com/Nouments)
