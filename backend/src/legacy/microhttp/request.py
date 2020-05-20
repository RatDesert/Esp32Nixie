import re
import time
from .exceptions import HttpExceptions

MAX_SIZE = 1024

#not memory safe
class Request:

    RGX_CONTENT_LEN = re.compile(b'(Content-Length: (\d+))')
    
    def __init__(self, handlers, chunk=b''):
        self.handlers = handlers

        self.__http = chunk
        self._chunk_count = 0

        
    def __getattr__(self, attr):
        if attr == '__http':
            return getattr(self, 'data')

        
    def __bool__(self):
        return self._is_request_full()

            
    def _parse_start_line(self):
        start_line, rest_http = self.__http.split(b'\r\n', 1)
        start_line = start_line.decode("utf-8")
        self.__http = rest_http
        method, url, http_version = start_line.split(' ')
        return method, url, http_version


    def add_chunk(self, chunk):
        #check memory here
        self._chunk_count += 1
        self.__http = b''.join((self.__http, chunk))
        
        if self._chunk_count == 1:
             self._check_first_chunk()

        
    def _check_first_chunk(self):
        method, url, http_version = self._parse_start_line()
        self._check_url(method, url, http_version)


    def _check_url(self, method, url, http_version):
        try:
            handler_method, _ = self.handlers[url]

            if handler_method != method:
                raise HttpExceptions.MethodNotAllowed

            self.method, self.url, self.http_version  = method, url, http_version

        except KeyError:
            raise HttpExceptions.NotFound
        

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
                raise HttpExceptions.LengthRequired

            if content_len > MAX_SIZE:
                raise HttpExceptions.PayloadTooLarge
        
            if len(self.data) < self.content_len:
                return False

            else:
                self.data = self.data.decode('utf-8')
                return True
        else:
            return False