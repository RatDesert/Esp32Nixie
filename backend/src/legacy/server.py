import socket
import gc
import select
import time
import re
import uio

MAX_SIZE = 1000
class WebApp:
    def __init__(self, port=80):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

        self.server.bind(addr)
        self.server.listen(3)

        # self.message = open('/static/index.html', 'r').read().encode()

        self.READ_ONLY = select.POLLIN | select.POLLHUP | select.POLLERR
        self.READ_WRITE = self.READ_ONLY | select.POLLOUT

        self.poller = select.poll()
        self.poller.register(self.server, self.READ_ONLY)

        self.handlers = {}
        self.client_request = {}

    def run(self):

        while True:
            events = self.poller.poll(5)

            for s, flag in events:

                if flag & select.POLLIN:

                    if s is self.server:
                        self._accept_conn(s)

                    else:
                        self._recv_chunk(s)
                        
                elif flag & select.POLLHUP:
                    self._close_connection(s)

                elif flag & select.POLLOUT:
                    try:
                        data = self.client_request[id(s)][1].__next__()
                        s.send(data)
                    except Exception as e:
                        print('\033[93m', e, '\033[0m')
                        del self.client_request[id(s)]
                        self.poller.unregister(s)
                        s.close()

                elif flag & select.POLLERR:
                    self._close_connection(s)
        

    def _accept_conn(self, server_socket):

        client_socket, client_address = server_socket.accept()
        client_socket.setblocking(0)
        self.poller.register(client_socket, self.READ_ONLY)
        #[request, user defined view]
        self.client_request[id(client_socket)] = [Request(self.handlers), None]

    def _recv_chunk(self, client_socket):
        chunk = client_socket.recv(1024)

        print('\033[94m' ,chunk, '\033[0m')
        if chunk:
            self._prepare_request(client_socket, chunk)
        else:
            self._close_connection(client_socket)
            

    def _prepare_request(self, client_socket, chunk):
            request = self.client_request[id(client_socket)][0]
            try:
                request.add_chunk(chunk)
                if bool(request):
                    view = self.handlers[request.url][1]

                    print('\033[92m200 OK: {}\033[0m'.format(request.url))

                    #init generator state for user respond
                    self.client_request[id(client_socket)].insert(1, view(request))
                    self.poller.modify(client_socket, self.READ_WRITE)
                else:
                    print('Request is not full || must set timeout here')

            except Exception as e:
                error_code = e.__str__().encode()
                client_socket.send(b'HTTP/1.1 {}'.format(error_code))

                self._close_connection(client_socket)
                print('\033[93m', e, '\033[0m')

    def _close_connection(self, client_socket):
        self.poller.unregister(client_socket)
        del self.client_request[id(client_socket)]
        client_socket.close()
        gc.collect()

"""Must:
   add chunks together in case of delay
   know about user defined handlers(url, merhod)
   send ready if request if fullfield | tries to parse all with timer and state
   Behavior:
   lazy parsing headers"""

        
class HttpException:
    
    class NotFound(Exception):
        def __init__(self, url):
            self.url = url

        def __str__(self): 
            return('404 Not Found: {}'. format(self.url))

    class MethodNotAllowed(Exception):
        def __str__(self): 
            return('405 Method Not Allowed')
        
    class RequestTimeout(Exception):
        def __str__(self): 
            return('408 Request Timeout')
        
    class LengthRequired(Exception):
        def __str__(self): 
            return('411 Length Required')
        
    class PayloadTooLarge(Exception):
        def __str__(self): 
            return('413 Payload Too Large')
        
class Request:
    RGX_CONTENT_LEN = re.compile(b'(Content-Length: (\d+))')
    
    def __init__(self, handlers, chunk=b''):
        self.__http = chunk
        self.handlers = handlers
        self.method, self.url, self.http_version = None, None, None
        
        self._chunk_count = 0
        
    """Lazy get request fields"""
    def __getattr__(self, attr):
        if attr == '__http':
            return getattr(self, 'data')
        
    def __bool__(self):
        return self._is_request_full()

    
    """Yields lines from http request"""
#     def _get_body(self):

            
    """Parsing http start line
       Must parse at first chunk if not than 400"""
    def _parse_start_line(self):
        start_line, rest_http = self.__http.split(b'\r\n', 1)
        start_line = start_line.decode("utf-8")
        self.__http = rest_http
        
        method, url, http_version = start_line.split(' ')
        return method, url, http_version
    
    
    def _check_mapped_uri(self):
        try:
            method, _ = self.handlers[self.url]
            if method != self.method:
                raise HttpException.MethodNotAllowed
                
        except KeyError:
            raise HttpException.NotFound(self.url)

    def add_chunk(self, chunk):
        self._chunk_count += 1
        self.__http = b''.join((self.__http, chunk))
        
        if self._chunk_count == 1:
             self._check_first_chunk()
        
    def _check_first_chunk(self):

        self.method, self.url, self.http_version = self._parse_start_line()
        self._check_mapped_uri()
        
    def _is_request_full(self):
        if self.method == 'GET' and b'\r\n\r\n' in self.__http:
            self.headers = self.__http.strip(b'\r\n\r\n')
            del self.__http
            return True
        
        elif self.method == 'POST' and b'\r\n\r\n' in self.__http:
            re_content_len = Request.RGX_CONTENT_LEN.search(self.__http)
            content_len = int(re_content_len.group(2))
            
            self.content_len = content_len
            self.headers, self.data = self.__http.split(b'\r\n\r\n')

            del self.__http
            if not content_len:
                raise HttpException.LengthRequired
            
            if content_len > MAX_SIZE:
                raise HttpException.PayloadTooLarge
        
            
            if len(self.data) < self.content_len:
                return False
            else:
                self.data = self.data.decode('utf-8')
                return True
            
        else:
            return False





