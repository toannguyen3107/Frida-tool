
from utils.decorator import header
from utils.color_utils import ANSI
from utils.run_command import run_command
from utils.adb_utils import run_adb_command_retn, run_adb_command
import re
def add_parser(subparsers):
    parser = subparsers.add_parser("klfrida", help="kill and list frida server")
    parser.set_defaults(func=klfrida)
@header
def klfrida(args):
    checkfrida = run_adb_command_retn("shell su -c \"ps -A | grep frida\"")
    if checkfrida != "":
        match = re.search(r'\s+(\d+)\s+\d+\s+', checkfrida)
        if match: 
            pid = match.group(1)
            print(f'{ANSI.YELLOW}pid = {match.group(1)}{ANSI.RESET}')
            run_adb_command(f"shell su -c \"kill -9 {pid}\"")
            print(f'{ANSI.GREEN}Frida server stopped{ANSI.RESET}')
    else: print("\tfrida server is not running")
    versions = run_adb_command_retn("shell su -c \"ls /data/local/tmp/frida-server-*\"")
    if versions == "":
        print(f"{ANSI.RED}Frida server not found!{ANSI.RESET}")
        return
    else:
        lstver = versions.split('\n') 
        lstnum = [i  for i in range(len(lstver)) if lstver[i] != ""]
        for i in lstnum:
            print(f"\t{ANSI.YELLOW}[{i}]. {lstver[i]}{ANSI.RESET}")