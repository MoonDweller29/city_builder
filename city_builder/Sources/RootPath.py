import os

class RootPath:
    __instance = None
    __initialized = None
    __rootPath = None

    def __new__(cls):
        if not RootPath.__instance:
            RootPath.__instance = super(RootPath, cls).__new__(cls)
        return RootPath.__instance

    def __init__(self):
        if not self.__initialized:
            self.__rootPath = os.path.dirname(__file__) + "/../"
            self.__initialized = True

    def get_path(self):
        return self.__rootPath
    
    def create_path(self, path):
        return os.path.join(self.__rootPath, path)