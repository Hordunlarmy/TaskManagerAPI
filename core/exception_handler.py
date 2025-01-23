from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        messages = []
        for field, detail in response.data.items():
            if isinstance(detail, list):
                detail = detail[0]
                messages.append(str(detail))

        response.data = {"status": "error", "message": "; ".join(messages)}
    elif response is not None:
        response.data = {
            "status": "error",
            "message": response.data.get("detail", "An error occurred"),
        }
    else:
        response = Response(
            {"status": "error", "message": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
