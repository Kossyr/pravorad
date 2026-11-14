import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.absolute()
RESOURCES_DIR = Path(PROJECT_DIR, "resources")
OUTPUT_DIR = Path(PROJECT_DIR, "output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CUSTOM_LORDS_DIR = Path(r"c:\Users\marty\OneDrive\StrongholdCrusader\CustomMedia")
REFERENCE_DIR = Path(r"c:\Users\marty\OneDrive\StrongholdCrusader\ReferenceAudio")
SOX_EXE = Path(r"C:\Program Files (x86)\sox-14-4-2\sox.exe")

# paralinquistic paths
# [clear throat], [sigh], [shush], [cough], [groan], [sniff], [gasp], [chuckle], [laugh]

JSON_TO_WAV_DICTIONARY = {
    "TAUNT1": "taunt1",
    "TAUNT2": "taunt2",
    "TAUNT3": "taunt3",
    "TAUNT4": "taunt4",
    "ANGRY_SIEGE_LOST": "angry_siege_lost",
    "ANGRY_CASTLE_DAMAGED": "angry_castle_damaged",
    "DEFEAT": "defeat",
    "NERV_PRE_SIEGE": "nerv_pre_siege",
    "NERV_WEAK": "nerv_weak",
    "VICTORY_GOOD": "victory_good",
    "VICTORY_HARASS": "victory_harass",
    "KILL_PLAYER": "kill_player",
    "KILL_NPC": "kill_npc",
    "REQUEST_GOODS": "request_goods",
    "THANK_GOODS": "thank_goods",
    "DIE_ALLY": "die_ally",
    "CONGRATS_ON_KILL": "congrats_on_kill",
    "BOAST_OF_KILL": "boast_of_kill",
    "ALLY_NEED_HELP": "ally_need_help",
    "ABOUT2SIEGE": "about2siege",
    "CANT_ATTACK": "cant_attack",
    "WONT_ATTACK": "wont_attack",
    "CANT_HELP": "cant_help",
    "WONT_HELP": "wont_help",
    "NOT_SENDING_GOODS": "not_sending_goods",
    "SENT_GOODS": "sent_goods",
    "TEAM_WINNING": "team_winning",
    "TEAM_LOSING": "team_losing",
    "WILL_SEND_TROOPS": "will_send_troops",
    "WILL_ATTACK_ENEMY": "will_attack_enemy",
}


class CustomLordAudio:
    name: str
    text: str

    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text


def load_messages_for_lord(
    author: str,
    custom_lord: str,
) -> list[CustomLordAudio]:
    lord_file = Path(f"{CUSTOM_LORDS_DIR}{author}", custom_lord, "text.txt")
    with open(lord_file) as f_in:
        lines = f_in.readlines()

    audio_list = []

    for line in lines:
        line = line.strip()

        if line.startswith("NICKNAME"):
            continue

        if "=" in line:
            line_split = line.split("=")
            key = line_split[0].strip()
            value = line_split[1].strip()
            if '"' in value:
                value = value.replace('"', "")
            text = value
            name = JSON_TO_WAV_DICTIONARY[key]
            audio_list.append(CustomLordAudio(name, text))

    # open the json as well for kick_player and add_player
    lord_file = Path(RESOURCES_DIR, f"{author}.json")
    with open(lord_file, "r") as f_in:
        data = json.load(f_in)

    audio_list.append(CustomLordAudio("add_player", data[custom_lord]["add_player"]))
    audio_list.append(CustomLordAudio("kick_player", data[custom_lord]["kick_player"]))

    return audio_list


def get_lords(author: str) -> list[str]:
    lord_file = Path(RESOURCES_DIR, f"{author}.json")
    with open(lord_file, "r") as f_in:
        data: dict[str, dict[str, str]] = json.load(f_in)
    return list(data.keys())
