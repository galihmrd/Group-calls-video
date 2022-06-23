import os
from lib.tg_stream import group_call_factory
from lib.driver.misc import PAUSE, RESUME, STOP


group_call = group_call_factory.get_group_call()


async def pstream(chat_id, file, audio=None):
    if audio:
        await group_call.join(chat_id)
        await group_call.start_video('./etc/banner.png', with_audio=False)
        await group_call.start_audio(file)
    else:
        await group_call.join(chat_id)
        await group_call.start_video(file)
    STOP[chat_id] = group_call
    PAUSE[chat_id] = group_call
    RESUME[chat_id] = group_call

async def pstream_audio(chat_id, file, thumb):
    await group_call.join(chat_id)
    await group_call.start_video(thumb, with_audio=False)
    await group_call.start_audio(file)
    STOP[chat_id] = group_call
    PAUSE[chat_id] = group_call
    RESUME[chat_id] = group_call

@group_call.on_playout_ended
async def media_ended(gc, source, media_type):
    print(f'{media_type} ended: {source}')
    try:
        await group_call.stop()
        os.remove(source)
    except Exception:
        pass
