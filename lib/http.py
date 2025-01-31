# urllib wrappers for simple operation
#
# because 'requests' or 'urllib3' start up 3x times slower and eat many
# times more RAM, in addition to being 3rd party modules

import time
import json
import gzip
import urllib.request


def _decode_using_charset(headers, data):
    if 'Content-Type' in headers:
        content_type = headers['Content-Type'].split('; ')
        for param in content_type:
            if param.startswith('charset='):
                try:
                    return data.decode(param.removeprefix('charset='), errors='ignore')
                except LookupError:
                    pass
                break
    return data.decode('ascii', errors='ignore')


def _decompress_using_encoding(headers, fobj):
    if 'Content-Encoding' in headers:
        encoding = headers['Content-Encoding']
        if encoding in ['gzip', 'x-gzip']:
            with gzip.GzipFile(fileobj=fobj) as gzobj:
                return gzobj.read()
        else:
            raise RuntimeError(f"unsupported Content-Encoding: {encoding}")
    return fobj.read()


def wrap_urlopen(url, retries=5, retry_delay=60, **kwargs):
    for retry in range(retries+1):
        try:
            with urllib.request.urlopen(url, **kwargs) as response:
                headers = response.headers
                data = _decompress_using_encoding(headers, response)
                text = _decode_using_charset(headers, data)
                return text
        except urllib.error.URLError as e:
            if retry < retries:
                print('sleeping')
                time.sleep(retry_delay)
            else:
                err = e
    raise err from None


def request(url, method, data=None, headers=None, **kwargs):
    if headers is None:
        headers = {}
    if isinstance(data, str):
        data = data.encode()
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    return wrap_urlopen(request, **kwargs)


def get(url, **kwargs):
    return request(url, method='GET', **kwargs)


def delete(url, **kwargs):
    return request(url, method='DELETE', **kwargs)


def post(url, **kwargs):
    return request(url, method='POST', **kwargs)


def request_json(url, method, data=None, headers=None, **kwargs):
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    if isinstance(data, dict):
        data = json.dumps(data)
    response = request(url, method=method, data=data, headers=headers, **kwargs)
    return json.loads(response)


def get_json(url, **kwargs):
    return request_json(url, method='GET', **kwargs)


def delete_json(url, **kwargs):
    return request_json(url, method='DELETE', **kwargs)


def post_json(url, **kwargs):
    return request_json(url, method='POST', **kwargs)
