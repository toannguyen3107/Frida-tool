from utils.adb_utils import run_adb_command
from utils.decorator import header
def add_parser(subparsers):
    parser = subparsers.add_parser("devices", help="List all connected devices")
    parser.set_defaults(func=list_devices)

@header
def list_devices(args):
    run_adb_command("devices")
