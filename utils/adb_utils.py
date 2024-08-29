import subprocess
import sys
from utils.color_utils import ANSI
from utils.decorator import splitstmtadb
@splitstmtadb
def run_adb_command(command):
    try:
        result = subprocess.run(['adb'] + command.split(), capture_output=True, text=True)
        print(f"{ANSI.CYAN}\t{result.stdout}{ANSI.RESET}")
        if result.stderr:
            print(f"{ANSI.RED}Error: {result.stderr}{ANSI.RESET}", file=sys.stderr)
    except FileNotFoundError:
        print(f"{ANSI.RED}ADB is not installed or not in your PATH.{ANSI.RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{ANSI.RED}An error occurred: {e}{ANSI.RESET}", file=sys.stderr)
        sys.exit(1)
@splitstmtadb
def run_adb_command_retn(command):
    try:
        result = subprocess.run(['adb'] + command.split(), capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        print(f"{ANSI.RED}ADB is not installed or not in your PATH.{ANSI.RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{ANSI.RED}An error occurred: {e}{ANSI.RESET}", file=sys.stderr)
        sys.exit(1)
        return None