import json

import requests
from decouple import config

from src.shared.logger import Logger

AUTH_KEY = config("EMAIL_AUTH_KEY").strip('"')
URL = config("EMAIL_API_URL").strip('"')

logger = Logger("__email__").get_logger()


class Email:
    def __init__(self, templates, authorization_key, url):
        self.templates = templates
        self.authorization_key = authorization_key
        self.url = url

    def _send_email(
        self, template_key, recipient_email, recipient_name, merge_info
    ):
        url = self.url
        payload = {
            "mail_template_key": template_key,
            "from": {
                "address": "noreply@hordun.software",
                "name": "Toraah Task Manager",
            },
            "to": [
                {
                    "email_address": {
                        "address": recipient_email,
                        "name": recipient_name,
                    }
                }
            ],
            "merge_info": merge_info,
        }

        payload = json.dumps(payload)

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.authorization_key,
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            print(response.text)
            return True
        except Exception as e:
            print("Email exception:", str(e))
            return False

    def send_status_email(
        self, recipient_email, recipient_name, template_variables: dict
    ):
        return self._send_email(
            template_key=self.templates.user_verification,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            merge_info=template_variables,
        )


class Email_Templates:
    """
    Class to store the email templates
    """

    status = config("STATUS_TEMPLATE")


templates = Email_Templates()

sender = Email(
    templates=templates,
    authorization_key=AUTH_KEY,
    url=URL,
)
