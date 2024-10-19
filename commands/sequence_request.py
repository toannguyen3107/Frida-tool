import os
from utils.color_utils import ANSI
from utils.decorator import header
from utils.ConfigRequest import Config

def add_parser(subparsers):
    parser = subparsers.add_parser("flowReq", help="send requests in sequence flow")
    parser.add_argument("-cf", "--config", required=True, help="Path to the config file <name>.yml")
    parser.set_defaults(func=config_sequence_request)


@header
def config_sequence_request(args):
    """Configure sequence_request settings."""

    import yaml
    if not args.config:
        print(f"{ANSI.YELLOW}[!]{ANSI.RESET}Please provide a config file.")
        return
    configLoad = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    config = Config(configLoad)

    total_requests = config.getTotalRequests()
    print(f"{ANSI.YELLOW}Total requests: {total_requests}{ANSI.RESET}")
    
    if total_requests is None:
        print(f"{ANSI.RED}Total requests not found in the config file{ANSI.RESET}")
        return
    
    for i in range(total_requests):
        req = config.getReq(str(i))
        response = req.sendRequest()
        print(response.headers['content-type'])