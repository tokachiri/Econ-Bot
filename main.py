import random
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Command
from discord.ext.commands import (CommandOnCooldown)
import asyncio
from webserver import keep_alive
from zoo import (common, uncommon, rare )
import os
import json
from discord import Member, Embed

bot = commands.Bot(command_prefix='/')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('BOT IS ONLINE!')
    await bot.change_presence(
        activity=discord.Game(name="Fishy here to /help"))


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency * 1000)}`ms")


keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")


@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(colour=discord.Colour.green())

    embed.set_author(name="Help:")
    embed.add_field(name="/ping", value="Returns your ping", inline=False)
    embed.add_field(name="/bal", value="Check your balance", inline=False)
    embed.add_field(name="/fish", value="Get more fish :fish:", inline=False)
    embed.add_field(name="/dep", value="Deposit your fish", inline=False)
    embed.add_field(name="/with", value="Withdraw your fish", inline=False)
    embed.add_field(name="/shop", value="Go shopping", inline=False)
    embed.add_field(name="/buy [item]", value="Buy stuff from the shop", inline=False)
    embed.add_field(name="/echo", value="Echo", inline=False)

    await ctx.send(author, embed=embed)


@bot.command()
async def bal(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await getdata()

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]

    embed = discord.Embed(
        title=f"{ctx.author}'s balance", color=discord.Color.green())
    embed.add_field(name="Wallet", value=f" {wallet} :fish:")
    embed.add_field(name="Bank", value=f"{bank} :fish:")
    await ctx.send(embed=embed)


@bot.command()
@cooldown(1, 7, BucketType.user)
async def fish(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await getdata()

    earn = random.randint(1, 10)

    await ctx.send(f"You caught {earn} :fish:")

    users[str(user.id)]["wallet"] += earn

    with open("bank.json", "w") as f:
        json.dump(users, f)


@bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f'You can do this again in {exc.retry_after:.1f} seconds')


mainshop = [{
    "rarity":1,
    "name":
    "Dog",
    "pic":
    ":dog:",
    "price":
    500,
    "description":
    "Super loyal pet that will help you hunt for animals"
},
            {
                "rarity": 1,
                "name": "Cat",
                "pic": ":cat:",
                "price": 500,
                "description":
                "Super loyal pet that will help you hunt for loot"
            },
            {
                "rarity":
                2,
                "name":
                "Fox",
                "pic":
                ":fox:",
                "price":
                1000,
                "description":
                "Sneaky fox that will help you hunt for rarer animals"
            },
            {
                "rarity":
                2,
                "name":
                "Hamster",
                "pic":
                ":hamster:",
                "price":
                1000,
                "description":
                "Super cute pet that will help you hunt for rarer loot"
            } 





@bot.command()
async def shop(ctx):
    em = discord.Embed(title="**:fish: Shop :fish:**")
    for item in mainshop:
        rarity = item["rarity"]
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        pic = item["pic"]
        
        color = ""
        if rarity == 1:
          color = ":white_circle:"
        elif rarity == 2:
          color = ":green_circle:"
        elif rarity == 3:
          color = ":blue_circle:"
        em.add_field(
            name=f"{color} {name} {pic} - {price} :fish:", value=f"{desc}")
    await ctx.send(embed=em)


@bot.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buyitem(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That doesn't exist lol")
            return

        else:
            await ctx.send(f"You need more fish in your wallet to buy {amount} {item}")
            return

    await ctx.send(f"{ctx.author} just bought {amount} {item}")


@bot.command(aliases=["inventory"])
async def inv(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await getdata()
    try:
        inv = users[str(user.id)]["inv"]
    except:
        inv = []

    em = discord.Embed(title=f"{ctx.author}'s inventory")
    for item in inv:
        name = item["item"].capitalize()
        amount = item["amount"]
        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)

@bot.command()
async def zoo(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await getdata()
    try:
        zoo = users[str(user.id)]["zoo"]
    except:
        zoo = []
    em = discord.Embed(title=f"{ctx.author}'s zoo")
    for item in zoo:
        name = item["item"].capitalize()
        amount = item["amount"]
        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)

@bot.command()
async def hunt(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await getdata()
  rand1 = random.randint(0,19)
  rand2 = random.randint(0,8)
  randomcommon = (common[rand1])
  randomuncommon = (uncommon[rand1])
  randomrare = (rare[rand2])


  earn = random.choice
#####################################
#############################WITHDRAW


@bot.command(pass_context=True, aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Enter the amount you want to withdraw")
        return

    bal = await updatefish(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have that much fish in your bank")
        return
    if amount < 0:
        await ctx.send("No")
        return

    await updatefish(ctx.author, amount)
    await updatefish(ctx.author, -1 * amount, "bank")

    await ctx.send(f"You withdrew {amount} :fish:")


@bot.command(pass_context=True, aliases=['deposit'])
async def dep(ctx, amount=None):
    await open_account(ctx.author)
    bal = await updatefish(ctx.author)
    if amount == None:
        await ctx.send("Enter the amount you want to deposit")
        return
    if amount == "all":
        amount = bal[0]

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("You don't have that much fish in your wallet")
        return
    if amount < 0:
        await ctx.send("No")
        return

    await updatefish(ctx.author, -1 * amount)
    await updatefish(ctx.author, amount, "bank")

    await ctx.send(f"You deposited {amount} :fish:")


#####################################DEPOSIT


@bot.command()
async def give(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Try again but this time actually donate something")
        return

    bal = await updatefish(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send("You don't have that much money in your bank")
        return
    elif amount < 0:
        await ctx.send("No")
        return

    else:
        await updatefish(ctx.author, -1 * amount, "bank")
        await updatefish(member, amount, "bank")

        await ctx.send(
            f"{ctx.author} successfully gave {member} **{amount}** :fish: through their bank!"
        )
        return


@bot.command(pass_context=True, aliases=['say'])
async def echo(ctx, *, message: str):
    await ctx.send(message)


###################################

##############################HYPERS
####################################


async def open_account(user):
    users = await getdata()
    if str(user.id) in users:  ####CHECKS FOR FISH ACCOUNT
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True




################FISH DATA
async def getdata():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users




async def updatefish(user, change=0, mode="wallet"):
    users = await getdata()
    users[str(user.id)][mode] += change
    with open("bank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


async def buyitem(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await getdata()

    bal = await updatefish(user)

    if bal[0] < cost:
        return [False, 2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inv"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["inv"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["inv"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["inv"] = [obj]

    with open("bank.json", "w") as f:
        json.dump(users, f)
    await updatefish(user, cost * -1, "wallet")
    return [True, "Worked"]

async def rand():
  rand = random.randint(0,10)
  return rand

async def pickcommon():
  pickcom = random.choice(common)
  return pickcom
###################FISH DATA
###################WILDLANDS

bot.run(TOKEN)
