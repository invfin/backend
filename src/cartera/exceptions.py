from rest_framework.exceptions import APIException


class FileProcessingError(APIException):
    status_code = 500
    default_detail = "An error occurred while processing the file."
