import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS
from pathlib import Path
import utils
import shutil
import subprocess

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cpu")

def add_voice_to_custom_lord(custom_lord: str, author: str):
    # load our JSON
    messages = utils.load_messages_for_lord(utils.CUSTOM_LORDS_DIR, author, custom_lord)
    reference = Path(utils.REFERENCE_DIR, f"{custom_lord}.mp3")
    lord_output_dir = Path(utils.OUTPUT_DIR, custom_lord)
    shutil.rmtree(lord_output_dir, ignore_errors=True)
    lord_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Custom lord: {custom_lord}")

    for message in messages:
        print(f"Generating a message '{message.name}': '{message.text}'")
        
        # Generate audio (requires a reference clip for voice cloning)
        wav = model.generate(message.text, audio_prompt_path=reference)

        output_file = Path(lord_output_dir, f"{message.name}.wav")
        ta.save(output_file, wav, model.sr)
        print(f"Saved to '{output_file}'")

    print("Generating of messages done!")

    batch_content = [
        "@echo off",
        f'cd /d "{lord_output_dir}"',
        "if not exist volume mkdir volume",
        "for %%i in (*.wav) do (",
        rf'"C:\Program Files (x86)\sox-14-4-2\sox.exe" -v 3 "%%i" "{lord_output_dir}\volume\%%~ni.wav"',
        ")"
    ]
    batch = Path(lord_output_dir, "_wav.bat")
    batch.write_text("\n".join(batch_content))

    subprocess.check_call(f'"{batch}"', shell=True)

    print("Increasing the volume done!")

    #final_output_dir = Path(output_dir, "_temp", custom_lord)
    final_output_dir = Path(f"{utils.CUSTOM_LORDS_DIR}{author}", custom_lord)
    shutil.copytree(Path(lord_output_dir, "volume"), final_output_dir, dirs_exist_ok=True)

    print(f"{custom_lord} DONE")



