import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    MOGODB_SETTINGS = {'db' : 'UTA_Enrollment'}