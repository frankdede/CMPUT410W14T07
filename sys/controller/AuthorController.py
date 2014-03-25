from AuthorHelpr import *
import Utility
import json
import sys
sys.path.append("sys/model")
from author import *

class AuthorController:
    def __init__(self,dbAdapter):
        self.authorController = AuthorController(dbAdapter)