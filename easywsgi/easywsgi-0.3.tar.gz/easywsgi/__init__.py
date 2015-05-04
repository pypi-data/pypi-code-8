#!/usr/bin/python
from paste.exceptions.errormiddleware import ErrorMiddleware
import traceback


class App():
    #TODO expand environ into class fields
    def __init__(self,environ,start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = "200 OK"
        self.content_type = "text/plain"
        self.gen = self.main()
        self.started = False
        
    def set_status(self,status):
        self.status = status

    def set_content_type(self,ctype):
        self.content_type = ctype

    def __next__(self): #walks to the next yield
        try:
            ret = next(self.gen)  
            ret = ret if type(ret) is bytearray else str.encode(str(ret)) #ensure bytestream
        except StopIteration: #if our function ends, so do we
            raise StopIteration()
        except Exception as e: #prety echo exceptions (instead off error 500_
            return str.encode(traceback.format_exc())

        if self.started: #cant echo if not started
            return ret
        else:
            self.start()
            return b'Output before start'
        
    def __iter__(self): #makes this an itterable
        return self


    def start(self): #equivalent of start_response
        if self.content_type == None:
            raise ValueError("Content type not set")
        headers = [('Content-Type',self.content_type)]
        self.start_response(self.status,headers)
        self.started = True
        
    def main(self): #place holder example
        self.start() #needs to be called
        yield "Please overwrite the main function" #example output


#very nasty trick
#decorator that returns a function, that returns a itterable class
def mainFunction(func):

    def res(environ, start_response): #this will be the application function
        class Page(App): #we need to extend out app and overwrite main
            main = func #user the decorated function for this
        return Page(environ, start_response) #now create an object from this class
    import __main__

    return res






