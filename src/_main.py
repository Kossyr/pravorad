import sys

import utils
from text_to_speech import add_voice_to_custom_lord

TOMAS_LORDS = utils.get_lords("Tomas")
MARTIN_LORDS = utils.get_lords("Martin")


def _add_voice_to_custom_lord(custom_lord: str):
    author = ""
    if custom_lord in TOMAS_LORDS:
        author = "Tomas"
    elif custom_lord in MARTIN_LORDS:
        author = "Martin"
    else:
        print(f"NO AUTHOR FOUND FOR THIS CUSTOM LORD!!! {custom_lord}")
        sys.exit(1)
    add_voice_to_custom_lord(custom_lord, author)


_add_voice_to_custom_lord("Scorpion")
