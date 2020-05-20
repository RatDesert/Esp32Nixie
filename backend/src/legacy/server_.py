import socket
import gc
import select



class Server:
    def __init__(self, port=80):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        
        self.server.bind(addr)
        self.server.listen(3)

        self.response_queues = {}
        self.request_messages = {}
        # self.message = open('/static/index.html', 'r').read().encode()
        self.message = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'

        self.READ_ONLY = select.POLLIN | select.POLLHUP | select.POLLERR
        self.READ_WRITE = self.READ_ONLY | select.POLLOUT

        self.poller = select.poll()
        self.poller.register(self.server, self.READ_ONLY)

    def run(self):

        while True:
            events = self.poller.poll(100)

            for s, flag in events:

                if flag & select.POLLIN:

                    if s is self.server:
                        self._accept_conn(s)

                    else:
                        self._read_request(s)

                elif flag & select.POLLHUP:
                    self.poller.unregister(s)
                    s.close()
                    gc.collect()

                elif flag & select.POLLOUT:
                    # g = self.response_queues[id(s)]
                    # g.__next__()
                    try:
                        self.response_queues[id(s)].__next__()
                    except Exception as e:
                        print(e)
                    
                    # s.send(self.message)
                    # self.poller.unregister(s)
                    # s.close()
                    


                elif flag & select.POLLERR:
                    self.poller.unregister(s)
                    s.close()
                    gc.collect()
    

    def _accept_conn(self, server_socket):

        connection, client_address = server_socket.accept()
        connection.setblocking(0)
        self.poller.register(connection, self.READ_ONLY)

        self.request_messages[id(connection)] = []

    def _read_request(self, client_socket):
        data = client_socket.recv(1024)
        if data:
            request = self.request_messages[id(client_socket)]
            request.insert(len(request), data)

            print(id(client_socket) , request)
            #if complete message than register
            #if not than 400
            self.poller.modify(client_socket, self.READ_WRITE)

            self.response_queues[id(client_socket)] = self._send_response(client_socket)
            
            
        else:
            self.poller.unregister(client_socket)
            client_socket.close()
            del self.request_messages[id(client_socket)]
            gc.collect()

            #server should map url to existing methods
            #pre parse
            #check url
            #check method
            

            #parssing data into request obj

            #calling user handler with url mapped and passing request obj
    def _send_response(self, client_socket):
        client_socket.send(self.message)

        with open('/static/index.html') as f:
            for line in f:
                yield client_socket.send(line.encode())
                         


        self.poller.unregister(client_socket)
        client_socket.close()

            
