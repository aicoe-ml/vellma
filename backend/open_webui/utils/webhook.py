import json
import logging

import requests
from open_webui.config import WEBUI_FAVICON_URL, WEBUI_NAME
from open_webui.env import SRC_LOG_LEVELS, VERSION

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["WEBHOOK"])


def post_webhook(url: str, message: str, event_data: dict) -> bool:
    try:
        payload = {}

        # Slack and Google Chat Webhooks
        if "https://hooks.slack.com" in url or "https://chat.googleapis.com" in url:
            payload["text"] = message
        # Discord Webhooks
        elif "https://discord.com/api/webhooks" in url:
            payload["content"] = message
        # Microsoft Teams Webhooks
        elif "azure.com" in url:
            action = event_data.get("action", "undefined")
            facts = [
                {"name": name, "value": value}
                for name, value in json.loads(event_data.get("user", {})).items()
            ]

            # we only want the user's id, name, email and role
            facts = [
                fact
                for fact in facts
                if fact["name"] in ["id", "name", "email", "role"]
            ]
            payload = {
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": {
                            "type": "AdaptiveCard",
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                            "version": "1.2",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "size": "Medium",
                                    "weight": "Bolder",
                                    "text": message,
                                    "wrap": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "spacing": "None",
                                    "text": f"{WEBUI_NAME} ({VERSION}) - {action}",
                                    "isSubtle": True,
                                    "wrap": True,
                                },
                                {
                                    "type": "Image",
                                    "url": WEBUI_FAVICON_URL,
                                    "size": "Small",
                                    "style": "RoundedCorners",
                                },
                                {
                                    "type": "FactSet",
                                    "facts": [
                                        {"title": fact["name"], "value": fact["value"]}
                                        for fact in facts
                                    ],
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.OpenUrl",
                                            "title": "Let's go!",
                                            "url": "http://vellma.dk/admin",
                                            "iconUrl": "icon:AddCircle",
                                        },
                                    ],
                                },
                            ],
                        },
                    }
                ]
            }
        # Default Payload
        else:
            payload = {**event_data}

        log.debug(f"payload: {payload}")
        r = requests.post(url, json=payload)
        r.raise_for_status()
        log.debug(f"r.text: {r.text}")
        return True
    except Exception as e:
        log.exception(e)
        return False
