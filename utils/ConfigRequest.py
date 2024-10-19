import os
import httpx
import re
class Config:
    def __init__(self, config):
        self.proxies = config.get('proxies', None)
        self.total_requests = config.get('total_request', None)
        self.requests = config.get('requests', None)
        # create empty extract dict
        self.env = config.get('env', None)
        if self.total_requests is None:
            return
        if self.proxies is not None:
            self.proxies = {
                "http://": self.proxies['http'],
                "https://": self.proxies['https']  
            }
        if self.proxies is not None:
            self.client = httpx.Client(proxies=self.proxies, verify=False)
        else:
            self.client = httpx.Client()
    def getTotalRequests(self):
        return self.total_requests
    def addEnv(self, key, value):
        self.env[key] = value
    def getReq(self, idx):
        return Request(self.client, self.requests['request_'+idx], self.env)

class Request(Config):
    def __init__(self, client, request, env):
        self.client = client
        self.request = request
        self.env = env
    def matchReplace(self, data):
        retn = {

        }
        if type(data) == str:
            match = re.findall(r'{{.+}}', data)
            if match  == []:
                return data
            else:
                for i in match:
                    subkey = i[3:-2]
                    data = data.replace(f'{i}', self.env[subkey])
                return data
        for key, value in data.items():
            # get value replace in data
            if type(value) == str:
                listMatch = re.findall(r'{{.+}}', value)
                for i in listMatch:
                    subkey = i[3:-2]
                    value = value.replace(f'{i}', self.env[subkey])
                retn[key] = value
        return retn
    # extract data and add into Env
    def getExtract(self, jsondata, response):
        # step 1: iter over array data
        retn = {}
        for i in range(len(jsondata)):
            for key, value in jsondata[i].items():
                if value['getfrom'] == 'headers':
                    if value['type']  == 'raw':
                        retn[key] = response.headers[value['key']]
                    elif value['type'] == 'regex':
                        pattern = value['regex']['pattern']
                        match = re.findall(pattern, response.headers[value['key']])
                        # if not match -> set None
                        if len(match) == 0:
                            retn[key] = None
                        else:
                            start = int(value['regex']['start'])
                            end = None if (value['regex']['end'] == "None") else int(value['regex']['end'])
                            step = None if (value['regex']['step'] == "None") else int(value['regex']['step'])
                            if end is None and step is None: 
                                retn[key] = match[0][start:]
                            elif end is None :
                                retn[key] = match[0][start::step]
                            elif step is None:
                                retn[key] = match[0][start:end:]
                            else:
                                retn[key] = match[0][start:end:step]
                elif value['getfrom'] == 'body':
                    if value['type'] == 'regex':
                        pattern = value['regex'][pattern]
                        match = re.findall(pattern, response.text)
                        if len(match) == 0:
                            retn[key] = None
                        else:
                            start = int(value['regex']['start'])
                            end = None if (value['regex']['end'] == "None") else int(value['regex']['end'])
                            step = None if (value['regex']['step'] == "None") else int(value['regex']['step'])
                            if end is None and step is None: 
                                retn[key] = match[0][start:]
                            elif end is None:
                                retn[key] = match[0][start::step]
                            elif step is None:
                                retn[key] = match[0][start:end:]
                            else:
                                retn[key] = match[0][start:end:step]
                    elif value['getfrom'] == 'json':
                        retn[key] = response.json()[value['key']]
        # add data into Env
        for key, value in retn.items():
            super().addEnv(key, value)

    def sendRequest(self):
        method = self.request['method']
        url = self.request['url']
        headers = self.request.get('headers', None)
        
        # replace value in headers
        headers = self.matchReplace(headers)
        url = self.matchReplace(url)
        # send data
        if method == 'GET':
            response = self.client.get(url, headers=headers)
        elif method == 'POST':
            type = self.request['body']['type']
            data = self.matchReplace(self.request['body']['data'])
            if type == 'raw':
                response = self.client.post(url, headers=headers, data=data)
            elif type == 'json':
                response = self.post(url, headers=headers, json=data)
            # process extract data
            jsondata = self.request.get('extract', None)
            if jsondata is not None:
                self.getExtract(jsondata, response)
        elif method == 'PUT':
            response = self.client.put(url, headers=headers)
        elif method == 'DELETE':
            response = self.client.delete(url, headers=headers)
        else: os.exit(1)

        return response