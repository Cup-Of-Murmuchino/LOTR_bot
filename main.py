import discord
from discord.ext import commands
from PIL import Image
import os

client = commands.Bot(command_prefix="!")

# Region owners
colonists_regions = []
nation_regions = []
brigands_regions = []
treasury_regions = []
events_regions = []

# Dict of all flag
flags = {"red": Image.open("flag_red.png"),
         "blue": Image.open("flag_blue.png"),
         "green": Image.open("flag_green.png"),
         "chest": Image.open("flag_chest.png")
}


# px - half resolution flag image
px = 64
# Regions coordinates
regions_cords = {
    "11111": (516 - px, 245 - px),
    "22222": (170 - px, 195 - px),
    "33333": (1160 - px, 145 - px),
    "44444": (900 - px, 260 - px),
    "55555": (420 - px, 495 - px),
    "66666": (225 - px, 685 - px),
    "77777": (765 - px, 490 - px),
    "88888": (1065 - px, 660 - px),
    "99999": (1375 - px, 410 - px),
    "21111": (685 - px, 760 - px),
    "32222": (1415 - px, 870 - px),
    "43333": (90 - px, 990 - px),
    "54444": (445 - px, 980 - px),
    "65555": (785 - px, 930 - px),
    "76666": (1030 - px, 1030 - px),
    "87777": (1175 - px, 1195 - px),
    "98888": (100 - px, 1185 - px),
    "12333": (285 - px, 1185 - px),
    "23133": (550 - px, 1185 - px),
    "43211": (740 - px, 1100 - px),
    "78917": (1375 - px, 1350 - px),
    "98213": (135 - px, 1405 - px),
    "12312": (480 - px, 1405 - px),
    "98989": (850 - px, 1350 - px)
}


def get_active_regions():
    """Возвращает список кортежев - координаты, и тип команды(тег, метка, имя клана, и т.д.)"""
    active_regions = []
    for regions in colonists_regions:
        active_regions.append((regions_cords[regions], "blue"))
    for regions in brigands_regions:
        active_regions.append((regions_cords[regions], "red"))
    for regions in nation_regions:
        active_regions.append((regions_cords[regions], "green"))
    for regions in treasury_regions:
        active_regions.append((regions_cords[regions], "chest"))
    return active_regions


@client.command()
async def карта(ctx, *agr):
    region_map = Image.open("map.png")
    for region in get_active_regions():
        region_map.paste(flags[region[1]], region[0], flags[region[1]])
    region_map.save("map_remake.png")
    await ctx.send(file=discord.File("map_remake.png"))


@client.command()
async def team(ctx):
    await ctx.send(f"Владения месный: {nation_regions}, владения колонистов: {colonists_regions}, владения разбойников: {brigands_regions}")


@client.command()
async def update(ctx, team, *agr):
    clans = [colonists_regions, nation_regions, brigands_regions]
    teams = {"red": brigands_regions,
            "blue": colonists_regions,
            "green": nation_regions
    }
    clans.remove(teams[team])
    teams[team].append(str(agr[0]))
    for region in clans:
        try:
            region.remove(agr[0])
        except ValueError:
            pass
    await ctx.send(f"Вы добавили во владения {team}, регион {agr[0]}")


@client.command()
async def delete(ctx, team, *agr):
    teams = {"red": brigands_regions,
             "blue": colonists_regions,
             "green": nation_regions
             }
    teams[team].remove(agr[0])
    await ctx.send(f"Вы удалили из владений {team}, регион {agr[0]}")


client.run("ODcxNDc5OTIzMTMzNTI2MDY3.YQb67A.e6RIf9gosZWXufZE1I88eDJ6JwE")



