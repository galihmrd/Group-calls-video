import subprocess

import ffmpeg


def get_audio(inputName, outName):
    stream = ffmpeg.input(inputName)
    audio = stream.audio
    stream = ffmpeg.output(audio, outName)
    ffmpeg.run(stream)


def time_stamp(inputName, outName):
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            f"{inputName}",
            "-c:v",
            "libx265",
            "-r",
            "24",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "fps=24,mpdecimate,drawtext=fontfile='./etc/font.ttf':fontcolor=yellow:fontsize=20:x=w-tw-10:y=10+50:text='%{pts\:gmtime\:0\:%H\\\\\:%M\\\\\:%S}'",
            f"{outName}",
        ]
    )
