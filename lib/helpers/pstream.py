from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioImagePiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import MediumQualityVideo

from lib.tg_stream import call_py


async def pstream(chat_id, file, audio=None):
    if audio:
        await call_py.join_group_call(
            chat_id,
            AudioImagePiped(
                file,
                "./etc/banner.png",
                video_parameters=MediumQualityVideo(),
            ),
            stream_type=StreamType().pulse_stream,
        )
    else:
        await call_py.join_group_call(
            chat_id,
            AudioVideoPiped(
                file,
                video_parameters=MediumQualityVideo(),
            ),
            stream_type=StreamType().live_stream,
        )


async def pstream_audio(chat_id, file, thumb):
    await call_py.join_group_call(
        chat_id,
        AudioImagePiped(
            file,
            thumb,
            video_parameters=MediumQualityVideo(),
        ),
        stream_type=StreamType().live_stream,
    )
