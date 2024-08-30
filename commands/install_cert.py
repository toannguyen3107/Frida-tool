from utils.adb_utils import run_adb_command
from utils.run_command import run_command
from utils.color_utils import ANSI
from utils.decorator import header
import subprocess
import os
import requests

def add_parser(subparsers):
    parser = subparsers.add_parser("install_cert", help=f"Install a certificate, default path is {ANSI.YELLOW}toancert.der{ANSI.RESET}")
    parser.add_argument("-p", "--path", default="toancert.der", help="Path to the certificate file")
    parser.set_defaults(func=install_certificate)
    parser.add_argument("-H", "--host", type=str, help="Host address for certificate download")
    parser.add_argument("-P", "--port", type=int, help="Port number for certificate download")


@header
def install_certificate(args):
    # Check if "install_cert" folder exists, create if not found
    install_cert_folder = "install_cert"
    if not os.path.exists(install_cert_folder):
        os.makedirs(install_cert_folder)
        print(f"{ANSI.GREEN}Created '{install_cert_folder}' folder{ANSI.RESET}")
    else:
        print(f"{ANSI.YELLOW}'{install_cert_folder}' folder already exists{ANSI.RESET}")

    # function download certificate
    def download_certificate(host, port):
        try:
            url = f"http://{host}:{port}/cert"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(f"{install_cert_folder}/toancert.der", "wb") as cert_file:
                    cert_file.write(response.content)
                print(f"{ANSI.GREEN}Certificate downloaded successfully as toancert.der{ANSI.RESET}")
                return True
            else:
                print(f"{ANSI.RED}Failed to download certificate. Status code: {response.status_code}{ANSI.RESET}")
                return False
        except requests.RequestException as e:
            print(f"{ANSI.RED}Error downloading certificate: {e}{ANSI.RESET}")
            return False
    # function check openssl is installed
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
    
    # check host and port 
    if args.host and args.port:
        print(f"{ANSI.YELLOW}[+] Download cert from {args.host}:{args.port}{ANSI.RESET}")
        check_download_cert = download_certificate(args.host, args.port)
        if check_download_cert == False:
            print(f"{ANSI.RED}Have problem when download cert! check host and port!{ANSI.RESET}")
    else: 
        print(f"{ANSI.YELLOW}[+] Find cert in folder {install_cert_folder}{ANSI.RESET}")
    # Check if toancert.der exists in the install_cert folder
    if not os.path.isfile(f'{install_cert_folder}/toancert.der'):
        print(f"{ANSI.RED}Error: toancert.der not found in {install_cert_folder} folder{ANSI.RESET}")
        os.exit(1)
    else:
        print(f"{ANSI.GREEN}toancert.der found in {install_cert_folder} folder{ANSI.RESET}")
        
    # check openssl installed
    check_openssl_installed = check_openssl_installed()
    if check_openssl_installed:
        if not os.path.isfile(f'{install_cert_folder}/9a5ba575.0'):
            if not os.path.isfile(f'{install_cert_folder}/cim-cacert.pem'):
                run_command(f"openssl x509 -inform DER -in toancert.der -out {install_cert_folder}/cim-cacert.pem")
                run_command(f"openssl x509 -inform PEM -subject_hash_old -in {install_cert_folder}/cim-cacert.pem")
                run_command(f"powershell -c mv {install_cert_folder}/cim-cacert.pem {install_cert_folder}/9a5ba575.0")
            else: 
                run_command(f"openssl x509 -inform PEM -subject_hash_old -in {install_cert_folder}/cim-cacert.pem")
                run_command(f"powershell -c mv {install_cert_folder}/cim-cacert.pem {install_cert_folder}/9a5ba575.0")
        
        # install via adb
        run_adb_command(f"push {install_cert_folder}/9a5ba575.0 /data/local/tmp/")
        run_adb_command(f"shell su -c \"cp /data/local/tmp/9a5ba575.0 /data/misc/user/0/cacerts-added/\"")
        run_command(f"powershell.exe rm {install_cert_folder}/9a5ba575.0")
        inp = input(f"{ANSI.YELLOW}Please reboot the device to apply the changes. Type Y or N: {ANSI.RESET}")
        if inp == "Y":
            run_adb_command("reboot")
            print(f"{ANSI.GREEN}Certificate installed successfully!{ANSI.RESET}")
        else: 
            print(f"{ANSI.YELLOW}Reboot and check!{ANSI.RESET}")
