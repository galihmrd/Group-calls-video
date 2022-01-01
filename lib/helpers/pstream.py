from lib.tg_stream import group_call_factory


group_call = group_call_factory.get_group_call()

async def pstream(chat_id, file, audio=None):
    if audio:
        await group_call.join(chat_id)
        await group_call.start_video('./etc/banner.png', with_audio=False)
        await group_call.start_audio(file)
    else:
        await group_call.join(chat_id)
        await group_call.start_video(file)

async def pstream_audio(chat_id, file, thumb):
    await grouo_call.join(chat_id)
    await group_call.start_video(thumb, with_audio=False)
    await group_call.start_audio(file)
