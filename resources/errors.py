# https://dev.to/paurakhsharma/flask-rest-api-part-4-exception-handling-5c6a
class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class ValidationError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "ValidationError": {
        "message": "ValidationError",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    }
}
