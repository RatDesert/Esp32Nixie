class HttpExceptions:
    
    class NotFound(Exception):
        def __str__(self): 
            return('404 Not Found')

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