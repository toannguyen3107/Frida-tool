import json
import os
from utils.color_utils import ANSI
import shutil
def parser_file(file_path):
    """Parse the request file."""
    with open(file_path, "r") as file:
        # preprocess idx for file:
        idx = file.name.split('\\')[-1].split('_')[0]
        file_data = file.read()
    # Split the file data into lines
    lines = file_data.split('\n')
    
    # Extract the request line (method, URL, HTTP version)
    request_line = lines[0].split()
    method = request_line[0]
    url = request_line[1]

    
    # Initialize headers dictionary
    headers = {}
    body = ""
    
    # Extract headers
    for line in lines[1:]:
        if line == "":
            # Empty line indicates the end of headers and start of body
            break
        header_key, header_value = line.split(":", 1)
        headers[header_key.strip()] = header_value.strip()
    
    # Extract body if present
    body_index = lines.index("") + 1
    if body_index < len(lines):
        body = "\n".join(lines[body_index:])
    if body == "":
        pass
    elif body[0] == '{':
        try:
            body = json.loads(body) if body else ""
        except json.JSONDecodeError:
            print(f'{ANSI.RED}->{ANSI.RESET} have error in json.loads -> parsing body {ANSI.RED}{file_path}{ANSI.RESET}')
    else:
        bodyArr = body.split('&')
        retnbody = {}
        for i in bodyArr:
            key, value = i.split('=')
            retnbody[key] = value
        body = retnbody    
    # Extract host from headers
    host = headers.get("Host", "")
    if host == "":
        host = headers.get("host", "")
    # extract key
    key = f"{idx}_{method}_{url.split('/')[-1]}"
    # Create the JSON object
    request_json = {
        "method": method,
        "host": host,
        "url": f"https://{host}{url}",
        "headers": headers,
        "body": body
    }
    
    return key, request_json
def gen_program(name_proj, input_json):
    """generate the program request"""
    flow_request_body = ""
    try:
            
        with open(input_json, 'r') as file_json:
            config = json.load(file_json)
        print(config)
        collection = {}
        max_idx = 0

        for key, _ in config.items():
            idx = int(key.split('_')[0])
            collection[idx] = {
                'name': key
            }
            max_idx = max(max_idx, idx)
        def gen_flow_request_body(idx, name):
            return f"""
    \"\"\" {'=' * 10 } {idx} - {name}  {'=' * 10 }\"\"\"
    req = collection[{idx}]['req']
    # define header
    pass
    # define body
    pass
    # send request data or json
    response = req.senddata()

    print_color(collection[{idx}]['name'], response.json())

    # extract response
    pass
    \"\"\" {'=' * 20 } END - {idx} {'=' * 20 }\"\"\"
"""
        for i in range(max_idx + 1):
            if i in collection:
                flow_request_body += gen_flow_request_body(i, collection[i]['name']) 
            
    except Exception as e:
            print(f"{ANSI.RED}[!]{ANSI.RESET} Error when processing file: {e}")    


    content = f"""
def flow():
    {flow_request_body}
""" 
    try:
        with open('output_program.py', 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"{ANSI.RED}ERROR 3{ANSI.RESET}: error when write file: {e}")    
def gen_proj(name_proj, input_json):
    """Generate the request proj."""
    try:
        shutil.rmtree(name_proj, ignore_errors=True)
        os.makedirs(name_proj, exist_ok=True)
        os.makedirs(f"{name_proj}/collections", exist_ok=True)
        if not os.path.exists(input_json):
            raise FileNotFoundError(f"{ANSI.RED}[!]{ANSI.RESET} Input JSON file not found: {input_json}")
        shutil.copyfile(input_json, f"{name_proj}/collections/{input_json}")
    except Exception as e:
        print(f"{ANSI.RED}[!]{ANSI.RESET} Error: {e}")
    # step 2 create class file
    try:
        class_concept = """
import httpx
from config import PROXIES_HTTPX, TIMEOUT_REQ
class Request:
    def __init__(self, method, url, headers, body):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.client = None
    def __str__(self):
        return f"Request(method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"
    def __repr__(self):
        return self.__str__()
    def setHeader(self, key, value):
        self.headers[key] = value
    def setBodyMaster(self, value):
        self.body = value
    def setBody(self, key, value):
        self.body[key] = value
    def setUrl(self, value):
        self.url = value
    def getHeader(self, key):
        return self.headers.get(key, None)
    def getBody(self, key):
        return self.body.get(key, None)
    def getHeaders(self):
        return self.headers
    def getBody(self):
        return self.body
    def getUrl(self):
        return self.url
    def getMethod(self):
        return self.method
    def removeHeader(self, key):
        self.headers.pop(key, None)
    def removeBody(self, key):
        self.body.pop(key, None)
    def senddata(self):
        self.client = httpx.Client(proxies=PROXIES_HTTPX, verify=False, timeout=TIMEOUT_REQ)
        if self.method == 'GET':
            return self.client.get(self.url, headers=self.headers)
        elif self.method == 'POST':
            return self.client.post(self.url, headers=self.headers, data=self.body)
        elif self.method == 'PUT':
            return self.client.put(self.url, headers=self.headers, data=self.body)
        elif self.method == 'DELETE':
            return self.client.delete(self.url, headers=self.headers)
        else:
            return self.client.get(self.url, headers=self.headers)
    def sendjson(self):
        self.client = httpx.Client(proxies=PROXIES_HTTPX, verify=False, timeout=TIMEOUT_REQ)
        if self.method == 'GET':
            return self.client.get(self.url, headers=self.headers)
        elif self.method == 'POST':
            return self.client.post(self.url, headers=self.headers, json=self.body)
        elif self.method == 'PUT':
            return self.client.put(self.url, headers=self.headers, json=self.body)
        elif self.method == 'DELETE':
            return self.client.delete(self.url, headers=self.headers)
        else:
            return self.client.get(self.url, headers=self.headers)
    def close(self):
        self.client.close()
"""
        config_concept = f"""
PROXIES_HTTPX = {{
    'http://': 'http://127.0.0.1:8081',
    'https://': 'http://127.0.0.1:8081'
}} 
JSON_NAME = 'collections/{input_json}'

TIMEOUT_REQ = None
""" 
        flow_request_body = """
"""
        try:
            
            with open(input_json, 'r') as file_json:
                config = json.load(file_json)
            print(config)
            collection = {}
            max_idx = 0

            for key, value in config.items():
                idx = int(key.split('_')[0])
                collection[idx] = {
                    'name': key
                }
                max_idx = max(max_idx, idx)
            def gen_flow_request_body(idx, name):
                return f"""
    \"\"\" {'=' * 10 } {idx} - {name}  {'=' * 10 }\"\"\"
    req = collection[{idx}]['req']
    # define header
    pass
    # define body
    pass
    # send request data or json
    response = req.senddata()

    print_color(collection[{idx}]['name'], response.json())

    # extract response
    pass
    \"\"\" {'=' * 20 } END - {idx} {'=' * 20 }\"\"\"
"""
            for i in range(max_idx + 1):
                if i in collection:
                    flow_request_body += gen_flow_request_body(i, collection[i]['name']) 
            
        except Exception as e:
                print(f"{ANSI.RED}[!]{ANSI.RESET} Error when processing file: {e}")
        request_concept = f"""
import json
from request_class import Request
from config import JSON_NAME
import os

fp  = os.path.join(os.path.dirname(__file__), JSON_NAME)
with open(fp, 'r') as file_json:
    config = json.load(file_json)

def print_color(name, data):
    print(f"\\033[32m[+]\\033[0m \\033[31m{{name}}\\033[0m: {{data}}")

def flow_request(collection):
    for idx in collection:
        # co = collection[idx]
        # co['req'].removeHeader('Content-Length')
        pass
    {flow_request_body}

def runFlow():
    collection = {{
    }}
    for key, _ in config.items():
        req = Request(config[key]['method'], config[key]['url'], config[key]['headers'], config[key]['body'])
        idx = int(key.split('_')[0])
        collection[idx] = {{
            'name': key,
            'req': req
        }}
    flow_request(collection)    
if __name__ == '__main__':
    runFlow()
"""

        
        # add body to request_concept
       

        with open(f"{name_proj}/main.py", "w") as file:
            file.write(request_concept)
        with open(f"{name_proj}/config.py", "w") as file:
            file.write(config_concept)
        with open(f"{name_proj}/request_class.py", "w") as file:
            file.write(class_concept)
    except Exception as e:
        print(f"{ANSI.RED}[!]{ANSI.RESET} Error 1: {e}")
