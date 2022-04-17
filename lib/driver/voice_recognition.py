import asyncio
import json
import math
import os
import shutil
import subprocess
import time
import wave

import requests
from fpdf import FPDF
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from tqdm import tqdm
from vosk import KaldiRecognizer, Model
from yt_dlp import YoutubeDL

from lib.config import LANGUAGE_CODE, MODEL_URL, TRANSCRIPT_FORMAT
from lib.helpers.display_progress import (
    download_progress_hook,
    progress_for_pyrogram,
    read_stderr,
)


@Client.on_message(
    filters.private & (filters.video | filters.document | filters.audio | filters.voice)
)
async def transcribe_from_file(bot, m):
    if m.document and not m.document.mime_type.startswith("video/"):
        return
    media = m.video or m.document or m.audio or m.voice
    editable_msg = await m.reply("`Downloading..`", parse_mode="md")
    c_time = time.time()
    file_dl_path = await bot.download_media(
        message=m,
        progress=progress_for_pyrogram,
        progress_args=("Downloading file..", editable_msg, c_time),
    )
    await gen_transcript_and_send(m, editable_msg, file_dl_path, is_yt=False)


@Client.on_message(filters.private & filters.text & filters.regex(pattern=".*http.*"))
async def transcribe_from_yt_url(bot, m):
    editable_msg = await m.reply("Downloading audio..")
    yt_url = m.text
    await download_yt_audio(yt_url, editable_msg)
    await gen_transcript_and_send(
        m, editable_msg, "youtube_dl_input_mono.wav", is_yt=True
    )


def download_and_unpack_models(model_url):
    print("Start Downloading the Language Model...")
    r = requests.get(model_url, allow_redirects=True)

    total_size_in_bytes = int(r.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    file_name = model_url.split("/models/")[1]
    with open(file_name, "wb") as file:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    else:
        print("Downloaded Successfully. Now unpacking the model..")
        shutil.unpack_archive(file_name)
        model_target_dir = f"model-{LANGUAGE_CODE}"
        if os.path.exists(model_target_dir):
            os.remove(model_target_dir)
        os.rename(file_name.rsplit(".", 1)[0], model_target_dir)
        print("unpacking Done.")

    os.remove(file_name)


if not os.path.exists(f"model-{LANGUAGE_CODE}"):
    download_and_unpack_models(MODEL_URL)


async def download_yt_audio(youtube_url, msg):
    ydl_opts = {
        "outtmpl": "youtube_dl_input" + ".%(ext)s",
        "format": "bestaudio/best",
        "restrictfilenames": True,
        "noplaylist": True,
        "progress_hooks": [lambda d: download_progress_hook(d, msg, Bot)],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "128",
            },
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    start = time.time()
    convert2mono = [
        "ffmpeg",
        "-loglevel",
        "quiet",
        "-i",
        "youtube_dl_input.wav",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        "youtube_dl_input_mono.wav",
    ]

    process = await asyncio.create_subprocess_exec(
        *convert2mono,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    await asyncio.wait(
        [
            read_stderr(start, msg, process),
            process.wait(),
        ]
    )

    if process.returncode != 0:
        await msg.edit("An Error occurred")
        exit(0)
    os.remove("youtube_dl_input.wav")


async def gen_transcript_and_send(msg, editable_msg, input_file, is_yt=True):
    model_path = f"model-{LANGUAGE_CODE}"
    # Check if model path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(os.path.basename(model_path) + " not found")

    if is_yt:
        wf = wave.open(input_file, "rb")
        sample_rate = wf.getframerate()
        file_size = os.path.getsize(input_file)
    else:
        sample_rate = 16000
        file_size = len(sample_file_as_wave(input_file, sample_rate).stdout.read())
        # Reinit process stdout to the beginning because seek is not possible with stdio
        wf = sample_file_as_wave(input_file, sample_rate)

    # Initialize model
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)

    # to store our results
    transcription = []
    processed_data_size = 0

    while True:
        if is_yt:
            data = wf.readframes(10000)  # use buffer of 10000
        else:
            data = wf.stdout.read(10000)
        processed_data_size += len(data)
        # Showing the progress
        percentage = processed_data_size * 100 / file_size
        progress = (
            "`Transcribing in Process...`\n[{0}{1}]\nPercentage : {2}%\n\n".format(
                "".join(["●" for i in range(math.floor(percentage / 5))]),
                "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
        )
        try:
            await editable_msg.edit(progress, parse_mode="md")
        except:
            pass
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Convert json output to dict
            result_dict = json.loads(rec.Result())
            # Extract text values and append them to transcription list
            transcription.append(result_dict.get("text", ""))

    # Get final bits of audio and flush the pipeline
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))
    transcription_text = ". ".join(transcription)

    output_transcript_file = (
        f'{input_file.rsplit(".", 1)[0]}.{TRANSCRIPT_FORMAT.lower()}'
    )

    if TRANSCRIPT_FORMAT == "PDF":
        pdf = FPDF()
        pdf.add_page()
        margin_bottom_mm = 10
        pdf.set_auto_page_break(True, margin=margin_bottom_mm)
        pdf.set_font("Times", size=12)

        words = transcription_text.split()
        grouped_words = [" ".join(words[i : i + 13]) for i in range(0, len(words), 13)]
        for x in grouped_words:
            pdf.cell(50, 10, txt=x, ln=1, align="L")
        pdf.output(output_transcript_file)

    elif TRANSCRIPT_FORMAT == "TXT":
        with open(output_transcript_file, "w+") as file:
            file.write(transcription_text)

    try:
        await msg.reply_document(output_transcript_file)
    except FloodWait as e:
        await asyncio.sleep(e.x)

    await editable_msg.delete()
    os.remove(input_file)
    os.remove(output_transcript_file)


def sample_file_as_wave(input_file, sample_rate):
    return subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            input_file,
            "-ar",
            str(sample_rate),
            "-ac",
            "1",
            "-f",
            "s16le",
            "-",
        ],
        stdout=subprocess.PIPE,
    )
