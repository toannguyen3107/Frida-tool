from utils.adb_utils import run_adb_command
from utils.decorator import header
def add_parser(subparsers):
    parser = subparsers.add_parser("packages", help="List all installed packages")
    parser.set_defaults(func=list_installed_packages)
@header
def list_installed_packages(args):
    run_adb_command("shell pm list packages")
