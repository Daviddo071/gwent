from flask import Flask, Request
from typing import Type, Tuple, Any
from pydantic import BaseModel

def create_error(error_type: str, error_message: str) -> dict:
    return {"ErrorType": error_type, "ErrorMessage": error_message}


def deserialize_request_payload(app: Flask,
                                current_request: Request,
                                model_class: Type[BaseModel]) -> Tuple[bool, Any, int]:
    """
    Validates a request.
    Returns an object of the class type passed in if validation is successful.
    Returns a dictionary with error info if validation is unsuccessful.
    :param app: Flask app - used for logging
    :param current_request: Request being validated
    :param model_class: Model to validate the request to
    :return: Tuple of (success, data, http_status_code)
    """
    data = current_request.get_json(silent=True)
    if not data:
        app.logger.info(f"Malformed input provided.")
        return False, create_error("ValidationError", "Malformed input provided"), 400

    try:
        validated = model_class(**data)
        app.logger.info(f"Successfully validated {validated}")
        return True, validated.model_dump(), 200
    except Exception as e:
        app.logger.info(f"Failed to validate: {e}")
        return False, create_error("ValidationError", f"Failed to validate {e}"), 400


def deserialize_dictionary(app: Flask,
                           current_request: dict,
                           model_class: Type[BaseModel]) -> Tuple[bool, dict, int]:
    """
    Validates a request.
    Returns an object of the class type passed in if validation is successful.
    Returns a dictionary with error info if validation is unsuccessful.
    :param app: Flask app - used for logging
    :param current_request: Request payload being validated
    :param model_class: Model to validate the request to
    :return: Tuple of (success, data, http_status_code)
    """
    try:
        validated = model_class(**current_request)
        app.logger.info(f"Successfully validated {validated}")
        return True, validated.model_dump(), 200
    except Exception as e:
        app.logger.info(f"Failed to validate: {e}")
        return False, create_error("ValidationError", f"Failed to validate {e}"), 400
