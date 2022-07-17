import socket
import ssl # used for https connections, wraps the socket
import gzip # for encoded responses

def request(url):
    headers = [
        'Connection: close\r\n', 
        'User-Agent: my-browser\r\n',
        'Accept-Encoding: gzip\r\n'
    ]

    # OBS: when using data type, type in the CLI the URI within quotes
    if 'view-source' in url:
        scheme, url = url.split(':', 1)

    elif 'data' in url:
        scheme, url = url.split(':', 1)
        if not 'text/html,' in url:
            raise AssertionError('Type of data not supported')
        body = url.split('text/html,', 1)[1]
        return '', body + '\n' 

    else:
        # for some reason ternary operator does not work here (?)
        if '://' in url:
            scheme, url = url.split('://', 1)
        else: scheme, url = 'http', url

    assert scheme in ['http', 'https', 'data', 'view-source'], \
        'Unknown scheme {}'.format(scheme)

    if ('/' in url):
        host, path = url.split('/', 1)
        path = '/' + path
    else:
        host = url
        path = '/'
    
    port = 443 if scheme == 'https' else 80

    if ':' in host:
        host, port = host.split(':', 1)
        port = int(port)

    s = socket.socket(
        family = socket.AF_INET,
        type = socket.SOCK_STREAM,
        proto= socket.IPPROTO_TCP,
    )
    s.connect((host, port))

    if scheme == 'https':
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    s.send(('GET {} HTTP/1.1\r\n'.format(path) +
            ''.join(headers) +
            'Host: {}\r\n\r\n'.format(host)).encode('utf8'))

    response = s.makefile('rb', newline='\r\n')

    statusline = response.readline()
    version, status, explanation = statusline.decode('utf-8').split(" ", 2)

    if status != '200' and status not in ['301', '302', '307', '308']:
        return status, '',"{}: {}".format(status, explanation), ''

    headers = {}
    while True:
        line = response.readline().decode('utf-8')
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
        
    if status in ['301', '302', '307', '308']:
        # bad request happens if we get stuck into a redirect loop
        return request(headers['location'])
    
    # We check if the content is encoded with gzip and if the transfer-encoding is chunked
    if 'content-encoding' in headers.keys():
        if 'gzip' in headers['content-encoding']:
            # we use gzip by default, even if other options are given
            if 'transfer-encoding' in headers.keys():
                if 'chunked' in headers['transfer-encoding']:
                    body = b''
                    chunked_response = response.read().split(b'\r\n')
                    for chunk in chunked_response:
                        if chunk == b'0': #final chunk
                            break
                        if not chunk.isdigit(): #chunks related to content-length
                            body += chunk
                    body = gzip.decompress(body)
            else:
                body = gzip.decompress(response.read())
    else:
        body = response.read()

    s.close()

    return status, headers, body, scheme

def show(raw_html, scheme):
    if scheme != 'view-source':
        body = raw_html.decode('utf-8').split('<body>', 1)[1].split('</body>', 1)[0]
        in_angle = False
        for c in body:
            if c == "<":
                in_angle = True
            elif c == ">":
                in_angle = False
            elif not in_angle:
                print(c, end="")
    else:
        print(raw_html)

def load(url):
    # print(request(url))
    status, headers, body, scheme = request(url)
    if status != '200':
        return print(body)
    show(body, scheme)

if __name__ == "__main__":
    import sys
    load(sys.argv[1])