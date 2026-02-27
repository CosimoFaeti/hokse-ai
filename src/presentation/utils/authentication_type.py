from enum import Enum

# class syntax
class AuthenticationType(Enum):
    PUBLIC = "public"
    TOKEN = "token"
    API_KEY = "api_key"