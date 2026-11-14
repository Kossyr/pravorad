from pathlib import Path

import json
import utils

from text_to_speech import add_voice_to_custom_lord

tomas_lords = utils.get_lords("Tomas")
martin_lords = utils.get_lords("Martin")

add_voice_to_custom_lord("Bishop", "Tomas")