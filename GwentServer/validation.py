from flask import Flask, Request


def create_error(errorType: str, errorMessage: str) -> dict:
    return {"ErrorType": errorType, "ErrorMessage": errorMessage}


def deserialize_request_payload(app: Flask,
                                current_request: Request,
                                required_fields: list[str],
                                should_filter:bool=True) -> tuple[bool, dict, int]:
    """
    Validates a request
    :param app: Flask app. Passed in for logging etc
    :param current_request: Request being validated
    :param required_fields: Fields required in the payload of the request
    :param should_filter: Should the output only include what is in the required fields
    :return: Tuple of (success, data, http_status_code)
    """
    data = current_request.get_json(silent=True)
    if not data:
        app.logger.info(f"Malformed input provided.")
        return False, create_error("ValidationError", "Malformed input provided"), 400

    data = dict(data)
    for field in required_fields:
        if field not in data:
            app.logger.warning(f"Missing attribute: {field}.")
            return False, create_error("ValidationError", f"Missing required field - {field}"), 400

    if should_filter:
        data = {field: data[field] for field in required_fields}

    app.logger.info(f"Payload validation success.")
    return True, data, 200
