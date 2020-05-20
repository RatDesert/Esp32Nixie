import time
import os

WEEKDAYS = ('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun')
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')

class Response:
    Server = 'Server: microhttp/0.1(ESPWROOM32)\r\n'
    Connection = 'Connection: Closed\r\n'

    # Content_Language = 'Content-Language: en-US\n'


    def __init__(self, status, content_type='', data=None, file_path=None):
        self.Start_line = 'HTTP/1.1 ' + status + '\r\n'
        self.Content_Encoding = ''
        self._set_date()
        
        # if (data and file_path) or (not data and not file_path):
        #     raise NoResponseBody

        if content_type:
            self.Content_Type = 'Content-Type: {}; charset=utf-8\r\n'.format(content_type)
 
            self.data = data
            self.file_path = file_path
            self._set_content_lenght()


    def __getattr__(self, attr):
        if attr in ('Content_Type', 'Content_Length', 'data', 'file_path', 'Content_Encoding'):
            return ''
        else:
            raise AttributeError(attr)


    def __iter__(self):
        return self._send_response()


    def _set_date(self):
        year, month, mday, hour, minute, second, weekday, yearday = time.localtime()

        self.Date = '{0}: {1} {2} {3} {4}:{5}:{6} {7}\r\n'.format(WEEKDAYS[weekday], month, MONTHS[month + 1], year, hour, minute, second, 'UTC')
    
    def _set_content_lenght(self):

        if self.file_path:
            self.Content_Length = 'Content-Length: {}\r\n'.format(os.stat(self.file_path)[6])

        elif self.data:
            self.data = self.data.encode()
            self.Content_Length = 'Content-Length: {}\r\n'.format(len(self.data))

    def _send_response(self):
        #it can be done by yield but it seems uneffective
        #should pack all headers in one bytearray and yeild chunks (?bsize)
        #should rollback in case of slow transmition and set timeout
        #should pack it in gzip zlib...
        response_headers = (self.Start_line,
                            self.Date,
                            Response.Server,
                            self.Content_Length,
                            self.Content_Type,
                            Response.Connection,
                            '\r\n\r\n')
        
        response_headers = ''.join(response_headers)
        print(response_headers)
        yield response_headers.encode()

        #assume that data is not too long
        if self.data:
            yield self.data
        
        if self.file_path:

            with open(self.file_path) as f:
                for line in f:
                    yield line.encode()
