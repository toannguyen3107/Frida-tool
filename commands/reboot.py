from utils.adb_utils import run_adb_command
def add_parser(subparsers):
    parser = subparsers.add_parser("reboot", help="Reboot the device")
    parser.set_defaults(func=reboot_device)

def reboot_device(args):
    run_adb_command("reboot")
