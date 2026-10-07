import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS
from pathlib import Path
import utils
import time

reference_dir = Path(r"c:\Users\marty\OneDrive\StrongholdCrusader\ReferenceAudio")
reference = Path(reference_dir, "Captain.mp3")
output_dir = Path("output").absolute()
output_dir.mkdir(parents=True, exist_ok=True)

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cpu")

# load our JSON
messages = utils.load_messages_for_lord("Captain")
#messages = []
# append add_player and kick_player
messages.append(utils.CustomLordAudio("add_player", "All aboard the ship!"))
messages.append(utils.CustomLordAudio("kick_player", "Abandon the ship!"))

for message in messages:
    print(f"Generating a message '{message.name}': '{message.text}'")

    # Generate audio (requires a reference clip for voice cloning)
    wav = model.generate(message.text, audio_prompt_path=reference)

    output_file = Path(output_dir, f"{message.name}.wav")
    ta.save(output_file, wav, model.sr)
    print(f"Saved to '{output_file}'")
    time.sleep(2)

print("Waiting 2 seconds to properly finish everything")
time.sleep(2)
print("DONE")