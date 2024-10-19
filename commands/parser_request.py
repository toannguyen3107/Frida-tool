import json
import os
from utils.color_utils import ANSI
from utils.decorator import header
from utils.parser_request_utils import parser_file, gen_proj
def add_parser(subparsers):
    parser = subparsers.add_parser("prr", help="parser requests")
    parser.add_argument('-in', "--request_directory", required=True, help="Path to the request directory")
    parser.add_argument('-o', '--output', help="Output directory")
    parser.set_defaults(func=parser_request)
    
    

@header
def parser_request(args):
    """Parser request settings."""
    if not args.request_directory:
        print(f"{ANSI.YELLOW}[!]{ANSI.RESET}Please provide a request directory.")
        return
    OUTPUT = "output"
    if not args.output: pass
    else:
        OUTPUT = args.output
    folder = args.request_directory
    retn_json = {}
    files = os.listdir(folder)
    print(f"{ANSI.GREEN}[+]{ANSI.RESET} Files in directory '{folder}':")
    
    for file in files:
        print(f" - {file}")
        print(f"{ANSI.GREEN}[-]{ANSI.RESET} Parsing files...")
        try:
            key, data = parser_file(os.path.join(folder, file))
            retn_json[key] = data
        except Exception as e:
            print(f"{ANSI.RED}[!]{ANSI.RESET} Error when parsing {file}: {e}")

    try: 
        with open(f"{OUTPUT}.json", "w") as file:
            file.write(json.dumps(retn_json, indent=4))
    except Exception as e:
        print(f"{ANSI.RED}[!]{ANSI.RESET} Error: {e}")
    

