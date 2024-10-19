from utils.color_utils import ANSI
from utils.decorator import header
from utils.parser_request_utils import gen_proj

def add_parser(subparsers):
    subparsers = subparsers.add_parser("gen_req", help="Generate flow project")
    subparsers.add_argument('-o', '--name', help="Gen proj with proj's name")
    subparsers.add_argument('-in', '--input', help="Input json file")
    subparsers.set_defaults(func=gen_req)

@header
def gen_req(args):   
    if args.name and args.input:
            print(f"{ANSI.GREEN}[+]{ANSI.RESET} Generating project: {args.name}")
            gen_proj(args.name, args.input)
    else:
        print(f"{ANSI.RED}[!]{ANSI.RESET} Failed to Generate the proj.")
        print(f"{ANSI.RED}[!]{ANSI.RESET} Please check the error message above.")