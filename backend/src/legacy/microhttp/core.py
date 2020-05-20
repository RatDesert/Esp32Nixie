import socket
import gc
import select
import time
from .request import Request

class WebApp:

    def __init__(self, port=80):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.server.bind(addr)
        self.server.listen(3)


        self.READ_ONLY = select.POLLIN | select.POLLHUP | select.POLLERR
        self.READ_WRITE = self.READ_ONLY | select.POLLOUT
        self.poller = select.poll()
        self.poller.register(self.server, self.READ_ONLY)

        self.handlers = {}
        self._request_state = {}

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
                    #critical if buffer is full
                    #next method should save data and try again later
                    try:
                        data = next(self._request_state[id(s)][1])
                        s.send(data)
                    except Exception as e:
                        print('\033[93m', e, '\033[0m')
                        del self._request_state[id(s)]
                        self.poller.unregister(s)
                        s.close()


                elif flag & select.POLLERR:
                    self._close_connection(s)
        

    def _accept_conn(self, server_socket):
        client_socket, client_address = server_socket.accept()
        client_socket.setblocking(0)
        self.poller.register(client_socket, self.READ_ONLY)
        #[request, user defined view]
        self._request_state[id(client_socket)] = [Request(self.handlers), None]


    def _recv_chunk(self, client_socket):
        chunk = client_socket.recv(1024)
        print('\033[94m' ,chunk, '\033[0m')

        if chunk:
            self._prepare_request(client_socket, chunk)
        else:
            self._close_connection(client_socket)
            

    def _prepare_request(self, client_socket, chunk):
            request = self._request_state[id(client_socket)][0]

            try:
                request.add_chunk(chunk)
                if bool(request):
                    view = self.handlers[request.url][1]
                    self._request_state[id(client_socket)].insert(1, view(request))
                    self.poller.modify(client_socket, self.READ_WRITE)
                else:
                    print('Request is not full || must set timeout here')

            except Exception as e:
                error_code = e.__str__().encode()
                print(error_code)
                client_socket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
                self._close_connection(client_socket)
                print('\033[93m', e, '\033[0m')


    def _close_connection(self, client_socket):
        self.poller.unregister(client_socket)
        del self._request_state[id(client_socket)]
        client_socket.close()
        gc.collect()