

class noVideoFound(Exception):
    def __init__(self,message="video requested was not found") :
        super(noVideoFound, self).__init__(message)
        
class invalidCommandSyntax (Exception):
    def __init__(self,message="the command was not formatted correctly please refer to manunal for help") :
        super(invalidCommandSyntax, self).__init__(message)
        

class API_Error(Exception):
    def __init__(self, message="apikey error ither qoutalimit was reach or unable to reach api server"):
        super(API_Error, self).__init__(message)

class insertPlaylist(Exception):
    def __inti__(self,message='inserting playlist is not allowed'):
        super(insertPlaylist, self).__init__(message)