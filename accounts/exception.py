from rest_framework.exceptions import APIException




class Validation(APIException):
    status_code = 400 #or whatever you want
    default_code = '4026'
    #  Custom response below
    default_detail = {"status": False, "message": "", "data":[]}