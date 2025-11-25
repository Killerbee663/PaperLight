from google.cloud import translate_v2 as translate
from flask_babel import _
import logging
import os
import json


def get_translate_client():
    """Initialize the translate client with credentials from environment"""
    if os.environ.get("GOOGLE_CREDENTIALS"):
        # Production: credentials from environment variable
        creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
        return translate.Client.from_service_account_info(creds_dict)
    else:
        # Local: credentials from file
        return translate.Client()


def translate_text(text, source_language, dest_language):
    try:
        translate_client = get_translate_client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = translate_client.translate(
            text,
            source_language=(
                source_language if source_language != dest_language else None
            ),
            target_language=dest_language,
            format_="text",
        )

        return result["translatedText"]

    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return _("Error: the translation service failed.")
