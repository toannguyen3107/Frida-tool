# Cli_tool

##  usage
> `python cli_tool.py -h`

```shell
cli_tool

    ==================================================================================

▄▄▄█████▓ ▒█████  ▄▄▄      ███▄    █     ███▄    █   ▄████  █    ██▓██   ██▓▓█████ ███▄    █
▓  ██▒ ▓▒▒██▒  ██▒████▄    ██ ▀█   █     ██ ▀█   █  ██▒ ▀█▒ ██  ▓██▒▒██  ██▒▓█   ▀ ██ ▀█   █
▒ ▓██░ ▒░▒██░  ██▒██  ▀█▄ ▓██  ▀█ ██▒   ▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▒██░ ▒██ ██░▒███  ▓██  ▀█ ██▒
░ ▓██▓ ░ ▒██   ██░██▄▄▄▄██▓██▒  ▐▌██▒   ▓██▒  ▐▌██▒░▓█  ██▓▓▓█  ░██░ ░ ▐██▓░▒▓█  ▄▓██▒  ▐▌██▒
  ▒██▒ ░ ░ ████▓▒░▓█   ▓██▒██░   ▓██░   ▒██░   ▓██░░▒▓███▀▒▒▒█████▓  ░ ██▒▓░░▒████▒██░   ▓██░
  ▒ ░░   ░ ▒░▒░▒░ ▒▒   ▓▒█░ ▒░   ▒ ▒    ░ ▒░   ▒ ▒  ░▒   ▒ ░▒▓▒ ▒ ▒   ██▒▒▒ ░░ ▒░ ░ ▒░   ▒ ▒
    ░      ░ ▒ ▒░  ▒   ▒▒ ░ ░░   ░ ▒░   ░ ░░   ░ ▒░  ░   ░ ░░▒░ ░ ░ ▓██ ░▒░  ░ ░  ░ ░░   ░ ▒░
  ░      ░ ░ ░ ▒   ░   ▒     ░   ░ ░       ░   ░ ░ ░ ░   ░  ░░░ ░ ░ ▒ ▒ ░░     ░     ░   ░ ░
             ░ ░       ░  ░        ░             ░       ░    ░     ░ ░        ░  ░        ░
                                                                    ░ ░
            Welcome to my hacking tool - v.1.0 - @Copyright by Toan Nguyen
    ==================================================================================



usage: cli_tool.py [-h] {devices,gen_req,install_cert,klfrida,packages,prr,proxy,reboot,flowReq,signapk} ...

CLI tool to run specific jobs.

positional arguments:
  {devices,gen_req,install_cert,klfrida,packages,prr,proxy,reboot,flowReq,signapk}
                        Available commands
    devices             List all connected devices
    gen_req             Generate flow project
    install_cert        Install a certificate with ip and port.
    klfrida             kill and list frida server
    packages            List all installed packages
    prr                 parser requests
    proxy               Manage proxy settings
    reboot              Reboot the device
    flowReq             send requests in sequence flow
    signapk             Sign an APK file

options:
  -h, --help            show this help message and exit
```
