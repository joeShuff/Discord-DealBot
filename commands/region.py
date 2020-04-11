import discord

from db.db_controller import set_region

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
    chosen_region = message.content.replace("<pref>region ".replace("<pref>", prefix), "").split(" ")[0]

    if chosen_region.upper() in possible_regions:
        set_region(message.channel.id, chosen_region)
        region_flag = possible_regions[chosen_region.upper()]

        confirm_embed = discord.Embed(
            color=0x046EB2,
            title="Set Region",
            description="<flag> Successfully updated region for `".replace("<flag>", region_flag) + str(message.channel.name) + "` to " + str(chosen_region.upper())
        )

        await message.channel.send(embed=confirm_embed)
    else:
        await message.channel.send(
            "Unsupported region, for available regions do `<pref>help region`".replace("<pref>", prefix))
