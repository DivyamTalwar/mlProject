import sys
from src.logger import logging #To Import The Logging File From The Src Folder

#This function provides a detailed error message whenever an exception occurs
def error_message_detail(error,error_detail:sys):
    #in exc_tb all the informaton will be stored like on which file the error has occured on which line etc
    _,_,exc_tb=error_detail.exc_info() #exc.info() return 3 length tuple we are only interested in the last value
    file_name=exc_tb.tb_frame.f_code.co_filename #To get the filename in which error has occured
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message



class CustomException(Exception):
    
    '''When an exception occurs and the CustomException is raised, the constructor (__init__) is automatically executed. It calls 
    the error_message_detail function to get detailed information about the error (like the file name, line number, and message) 
    and stores it in the error_message variable.'''
    
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message) #Inheried From The base Class Exception So you have to initialize the constructor
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message #To Return The Detailed Information About The Error Occured 
    

