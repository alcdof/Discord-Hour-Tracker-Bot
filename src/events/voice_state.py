from src.services.time_tracker import start_tracking, stop_tracking

def register_voice_event(bot):

    @bot.event
    async def on_voice_state_update(member, before, after):

        if before.channel is None and after.channel is not None:
            start_tracking(member.id)

        if before.channel is not None and after.channel is None:
            stop_tracking(member.id)