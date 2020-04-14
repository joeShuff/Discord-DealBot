import discord

from db.db_controller import set_region, get_region

possible_regions = {
    "AU2": ":flag_au:",
    "BR2": ":flag_br:",
    "CA": ":flag_ca:",
    "CN": ":flag_cn:",
    "EU1": ":flag_eu: ",
    "EU2": ":flag_eu: ",
    "RU": ":flag_ru:",
    "TR": ":flag_tr:",
    "US": ":flag_us:",
    "UK": ":flag_gb:"
}


async def set_region_for_channel(bot, message):
    from commands.CommandManager import prefix
    chosen_region = message.content.replace("<pref>region".replace("<pref>", prefix), "").strip().split(" ")[0]

    if len(chosen_region) == 0:
        chosen_region = get_region(message.channel.id)
        region_flag = possible_regions[chosen_region.upper()]

        channel_name = ""
        if isinstance(message.channel, discord.DMChannel):
            channel_name = str(message.channel.recipient)
        else:
            channel_name = str(message.channel.name)

        current_region_embed = discord.Embed(
            color=0x046EB2,
            title="Current Region",
            description="<flag> Your current region for `<chan>` is <reg> <flag>"
                .replace("<flag>", str(region_flag))
                .replace("<chan>", channel_name)
                .replace("<reg>", str(chosen_region).upper())
        )

        await message.channel.send(embed=current_region_embed)
    else:
        if chosen_region.upper() in possible_regions:
            set_region(message.channel.id, chosen_region)
            region_flag = possible_regions[chosen_region.upper()]

            channel_name = ""
            if isinstance(message.channel, discord.DMChannel):
                channel_name = str(message.channel.recipient)
            else:
                channel_name = str(message.channel.name)

            confirm_embed = discord.Embed(
                color=0x046EB2,
                title="Set Region",
                description="<flag> Successfully updated region for `<chan>` to <reg> <flag>"
                    .replace("<flag>", str(region_flag))
                    .replace("<chan>", channel_name)
                    .replace("<reg>", str(chosen_region).upper())
            )

            await message.channel.send(embed=confirm_embed)
        else:
            await message.channel.send(
                "Unsupported region, for available regions do `<pref>help region`".replace("<pref>", prefix))
