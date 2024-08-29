from utils.adb_utils import run_adb_command
from utils.run_command import run_command
from utils.color_utils import ANSI
from utils.decorator import header
import subprocess
import os

def add_parser(subparsers):
    parser = subparsers.add_parser("install_cert", help=f"Install a certificate, default path is {ANSI.YELLOW}toancert.der{ANSI.RESET}")
    parser.add_argument("-p", "--path", default="toancert.der", help="Path to the certificate file")
    parser.set_defaults(func=install_certificate)
@header
def install_certificate(args):
    def check_openssl_installed():
        try:
            result = subprocess.run(['openssl', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{ANSI.GREEN}OpenSSL is installed: {result.stdout.strip()}{ANSI.RESET}")
                return True
            else:
                print(f"{ANSI.RED}OpenSSL is not installed or not found in PATH.{ANSI.RESET}")
                return False
        except FileNotFoundError:
            print(f"{ANSI.RED}OpenSSL is not installed or not found in PATH.{ANSI.RESET}")
            return False
        except Exception as e:
            print(f"{ANSI.RED}An error occurred while checking OpenSSL: {e}{ANSI.RESET}")
            return False
    check_openssl_installed = check_openssl_installed()
    if check_openssl_installed:
        if not os.path.isfile('9a5ba575.0'):
            if not os.path.isfile('cim-cacert.pem'):
                run_command(f"openssl x509 -inform DER -in toancert.der -out cim-cacert.pem")
                run_command(f"openssl x509 -inform PEM -subject_hash_old -in cim-cacert.pem")
                run_command("powershell -c mv cim-cacert.pem 9a5ba575.0")
            else: 
                run_command(f"openssl x509 -inform PEM -subject_hash_old -in cim-cacert.pem")
                run_command("powershell -c mv cim-cacert.pem 9a5ba575.0")
        
        # install via adb
        run_adb_command("push 9a5ba575.0 /data/local/tmp/")
        run_adb_command("shell su -c \"cp /data/local/tmp/9a5ba575.0 /data/misc/user/0/cacerts-added/\"")
        run_command("powershell.exe rm 9a5ba575.0")
        inp = input(f"{ANSI.YELLOW}Please reboot the device to apply the changes. Type Y or N: {ANSI.RESET}")
        if inp == "Y":
            run_adb_command("reboot")
            print(f"{ANSI.GREEN}Certificate installed successfully!{ANSI.RESET}")
        else: 
            print(f"{ANSI.YELLOW}Reboot and check!{ANSI.RESET}")
