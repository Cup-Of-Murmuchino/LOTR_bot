import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image
import json
import os

client = commands.Bot(command_prefix="/")
print("Hello world")
# Region owners


with open("clans.json", "rb") as file:
    clans = json.load(file)
    colonists_regions = clans["colonists_regions"]
    nation_regions = clans["nation_regions"]
    brigands_regions = clans["brigands_regions"]
    treasury_regions = clans["treasury_regions"]
    events_regions = clans["events_regions"]


# Dict of all flag
flags = {"red": Image.open("flag_red.png"),
         "blue": Image.open("flag_blue.png"),
         "green": Image.open("flag_green.png"),
         "chest": Image.open("flag_chest.png")
}

# px - half resolution flag image
px = 16
# Regions coordinates
regions_info = {
    "Shift": (34, 87, 64),
    "BigOasis": (286, 197, 86),
    "MushroomMadness": (610, 92, 32),
    "SnowPeak": (104, 332, 64),
    "Resonance": (373, 401, 64),
    "NaturalComplex": (689, 273, 64),
    "CornerHopelessness": (48, 657, 44),
    "FieldsOfPerdition": (208, 560, 86),
    "Melting": (417, 576, 64),
    "Distance": (661, 630, 64)
}


def updjson():
    with open('clans.json') as f:
        data = json.load(f)
    # update the data dictionary then re-dump it in the file
    data.update({
        "colonists_regions": colonists_regions,
        "nation_regions": nation_regions,
        "brigands_regions": brigands_regions,
        "treasury_regions": treasury_regions,
        "events_regions": events_regions
    })

    with open('clans.json', 'w') as data_file:
        json.dump(data, data_file, indent=2)


def get_active_regions():
    """Возвращает список кортежев - координаты, и тип команды(тег, метка, имя клана, и т.д.)"""
    active_regions = []
    for regions in colonists_regions:
        active_regions.append((regions_info[regions], "blue"))
    for regions in brigands_regions:
        active_regions.append((regions_info[regions], "red"))
    for regions in nation_regions:
        active_regions.append((regions_info[regions], "green"))
    for regions in treasury_regions:
        active_regions.append((regions_info[regions], "chest"))
    return active_regions


@client.command()
async def map(ctx, *agr):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    region_map = Image.open("map_new.png")
    for region in get_active_regions():
        # Paste flag on map. First img flag. Second - its region pos in map x,y([0][0] = pos, [0][1] flag size)
        # region[1] = name of the flag,
        # region [0] = info of the region: [0] - pos x on map, [1] - pos y on map, [2] - size of flag
        curr_flag = flags[region[1]].resize((region[0][2], region[0][2]))
        region_map.paste(curr_flag, (region[0][0]-(int(region[0][2]/2)), region[0][1]-(int(region[0][2]/2))), curr_flag)
    region_map.save("map_remake.png")
    await ctx.send(file=discord.File("map_remake.png"))


@client.command()
async def team(ctx):
    await ctx.message.delete()
    if get(ctx.author.roles, name="Region editor"):
        await ctx.send(f"Владения месный: {nation_regions}, владения колонистов: {colonists_regions}, владения разбойников: {brigands_regions}")


def region_is_exists(name):
    exist = False
    for region in regions_info.keys():
        if name == region:
            exist = True
            return exist
    return exist


@client.command()
async def update(ctx, team, *agr):
    await ctx.message.delete()
    if get(ctx.author.roles, name="Region editor"):
        if region_is_exists(agr[0]):
            clans_to_clear = [colonists_regions, nation_regions, brigands_regions]
            teams = {"red": brigands_regions,
                    "blue": colonists_regions,
                    "green": nation_regions
            }
            # Delete current clan in check_to_delete_region list (clans_to_clear)
            clans_to_clear.remove(teams[team])
            # Give region to current clan

            # Check region in another clans, and delete it if exists
            for region in clans_to_clear:
                try:
                    region.remove(agr[0])
                except ValueError:
                    pass
            check_region_exists = 0
            for region in teams[team]:
                if region == agr[0]:
                    check_region_exists = 1
                    break
            if not check_region_exists:
                teams[team].append(str(agr[0]))
                updjson()
                await ctx.send(f"{ctx.author.mention}, вы добавили во владения {team}, регион {agr[0]}")
                await map(ctx)
            else:
                await ctx.send(f"{ctx.author.mention}, такой регион уже имееться во владениях этого клана.")
        else:
            await ctx.send(f"{ctx.author.mention}, вы не правильно написали имя региона!")
    else:
        await ctx.send(f"{ctx.author.mention}, у вас не прав на изменения регионов у кланов!")


@client.command()
async def delete(ctx, team, *agr):
    await ctx.channel.purge(limit=1)
    if get(ctx.author.roles, name="Region editor"):
        if region_is_exists(agr[0]):
            teams = {"red": brigands_regions,
                     "blue": colonists_regions,
                     "green": nation_regions,
                     }
            teams[team].remove(agr[0])
            updjson()
            await ctx.send(f"{ctx.author.mention}, вы удалили из владений {team}, регион {agr[0]}")
        else:
            await ctx.send(f"{ctx.author.mention}, вы не правильно написали имя региона!")
    else:
        await ctx.send(f"{ctx.author.mention}, у вас не прав на изменения регионов у кланов!")




@client.command()
async def addchest(ctx, *agr):
    if get(ctx.author.roles, name="Region editor"):
        treasury_regions.append(agr[0])
        updjson()


client.run(os.environ.get("TOKEN"))



