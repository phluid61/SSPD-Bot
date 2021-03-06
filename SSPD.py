
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pprint import pprint
import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
import logging

logging.basicConfig(level=logging.INFO)

now = datetime.datetime.now()
bot = commands.Bot(command_prefix='&')
client = discord.Client()

# credential file for discord token
token_file = open("dToken.txt", "r")
d_token = token_file.readline()

# authorisation to access google sheet
scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
gc = gspread.authorize(creds)
dc = gspread.authorize(creds)

# initialise current sheet
sheet = gc.open("Warnings List").sheet1
# intialise test sheet
# test = gc.open("SSPD-Test").sheet1

#-------------------------DANGER: SET TEST SHEET EQUAL TO PROD : DANGER---------------------------#
test = sheet

all = sheet.get_all_records(False, 3, "")


#-----Hardcode-----

#------------------


@bot.event
#@commands.has_role("Moderators™")
async def on_ready():
    print("ID: " + str(bot.user.id))
    print(bot.user)
    print(bot.user.name + " Ready...")

#----------------------


@bot.event
async def on_message(message):
    if message.author != bot.user:

        if str.lower(message.content) == "ayy":
            channel = message.channel
            await channel.send("lmao")

        if "fuck" in str.lower(message.content) and "sspd" in str.lower(message.content):
            channel = message.channel
            await channel.send("Hey " + message.author.name + " What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.")


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def ping(ctx):
    await ctx.send("pong!")


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def getline(ctx, num):
    await ctx.send(GetRow(num))


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def strike(ctx, user: discord.Member, rule):
    print(bool(alreadyListedCheck(user, test)))
    if bool(alreadyListedCheck(user, test)) == False:
        row_index = next_available_row(test)
        if test.cell(row_index, 1).value == "":
            cell_list = test.range(
                letters[0]+str(row_index)+":" + letters[4]+str(row_index))
            cell_list[0].value = str(user)
            cell_list[1].value = str("Rule " + rule)
            cell_list[2].value = str(now.strftime("%Y-%m-%d"))
            cell_list[3].value = str(ctx.message.author)
            test.update_cells(cell_list)
    else:

        alreadyListedCheck(user, test)
    await notification(ctx, user, rule)


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def channelTest(ctx, flag: int):
    if flag == 3:
        general = bot.get_channel(266593626501545984)
        await general.send("test" + str(flag))
    elif flag == 2:
        modChannel = bot.get_channel(300045476554735618)
        await modChannel.send("test" + str(flag))
    elif flag == 1:
        logChannel = bot.get_channel(373156271056224256)
        await logChannel.send("test" + str(flag))
    else:
        ctx.send("Incrrect usage. \n channeltest [x] where 0<x<4")


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def pmTest(ctx, user: discord.Member, *message: str):
    await user.send(message)
    #-----------------------------


def GetRow(num):
    warnings = sheet.row_values(num)
    # remove empty cells
    warnings = list(filter(lambda x: x != '', warnings))
    # warnings.insert(5, "|")
    return warnings


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+2


def alreadyListedCheck(user: discord.Member, worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    found = list()
    for item in str_list:
        if user.id in item:
            found = str_list.index(item)
            break
    return found


def firstEmptyColum():
    return True


async def notification(ctx, user: discord.Member, rule):
    embed = discord.Embed(title="POO LAGOONER DETECTED: Disciplinary Action Taken", description="Strike dealt to @" +
                          str(user) + " for rule" + str(rule) + ".", color=0xFF0000)
    embed.set_footer(
        text="Further misbehaviour may result in deportation to Poo Island.")
    embed.set_image(url="https://i.imgur.com/eYTcdNe.jpg")
    # await client.send_message(discord.Object(id='general'), embed=embed)
    noti_string = str(str(user) + " striked for rule " +
                      rule + " on " + now.strftime("%Y-%m-%d") + ".")
    await ctx.send(embed=embed)
    print(noti_string)


a = ""
# print(bool(a))
a = "a"
# print(bool(a))
letters = ["A", "B", "C", "D", "E", "F", "G",
           "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
row_index = next_available_row(test)
# print(row_index)

a = ""
# print(bool(a))
a = "a"
# print(bool(a))
letters = ["A", "B", "C", "D", "E", "F", "G",
           "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
row_index = next_available_row(test)
# print(row_index)

bot.run(d_token)
