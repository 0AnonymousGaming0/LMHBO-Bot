import discord
import signal
import sys
import random

client = discord.Client()


def terminate_handler(signal, frame):
    print('Caught termination signal, exiting.')
    save_all()
    sys.exit(0)
signal.signal(signal.SIGINT, terminate_handler)

with open('currency', 'r') as f:
    coins = eval(f.read())

with open('commandused','r') as f:
    commandused = eval(f.read())

with open('messagesent','r') as f:
    messagesent = eval(f.read())

def getmessagesent(user):
    try:
        return messagesent[user]
    except KeyError:
        messagesent[user] = 0
        return 0

def setmessagesent(user, messages):
    messagesent[user] = messages

def getcommandused(user):
    try:
        return commandused[user]
    except KeyError:
        commandused[user] = 0
        return 0

def setcommandused(user, command):
    commandused[user] = command

def getcoins(user):
    try:
        return coins[user][0], coins[user][1]
    except KeyError:
        coins[user] = [0, 0]
        return coins[user][0], coins[user][1]

def setcoins(user, coin1=None, coin2=None):
    if coin1 is None:
        coin1 = getcoins(user)[0]
    if coin2 is None:
        coin2 = getcoins(user)[1]
    print(user, coin1, coin2)
    coins[user] = [coin1, coin2]

class LeaderBoardPosition:

    def __init__(self, user, coins):
        self.user = user
        self.coins = coins

def save_all():
    with open('currency', 'w') as f:
        f.write(repr(coins))
    with open('commandused', 'w') as f:
        f.write(repr(commandused))
    with open('messagesent', 'w') as f:
        f.write(repr(messagesent))


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='1help (Use that command to get started with the bot)'))
    print('Logged in')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user = message.author.id
    name = message.author.name

    if message.content.startswith(""):
        setmessagesent(user, getmessagesent(user)+1)

    if message.content.startswith('1help'):
        if message.content[6:] == 'currency':
            embed = discord.Embed(title='**CURRENCY**',color=0x123456)
            embed.add_field(name='1bal',value='YOUR balance',inline=False)
            embed.add_field(name='1beg/1search',value='Try Begging/Searching',inline=False)
            embed.add_field(name='1leaderboard1/1leaderboard2',value='Richest Users',inline=False)
            embed.add_field(name='1rob',value='Try robbing people',inline=False)
            embed.add_field(name='1share_coin1/1share_coin2',value='Share your coins',inline=False)
            await message.channel.send(embed=embed)
            setcommandused(user, getcommandused(user)+1)
        else:
            embed = discord.Embed(title='**HELP**',description='PREFIX: 1',color=0x123456)
            embed.add_field(name='1help currency',value='Currency',inline=False)
            embed.add_field(name='169',value='69?',inline=False)
            await message.channel.send(embed=embed)
            setcommandused(user, getcommandused(user)+1)
        
    if message.content.startswith('1bal'):
        embed = discord.Embed(title='**BALANCE**', color=0xaa00aa)
        embed.add_field(name="**:joy:'s**", value=f'{getcoins(user)[0]}')
        embed.add_field(name="**:rofl:'s**", value=f'{getcoins(user)[1]}')
        await message.channel.send(embed=embed)
        setcommandused(user, getcommandused(user)+1)

    if message.content.startswith('1beg'):
        await message.channel.send("Sorry, this isn't *Dank Memer*, buddy.")
        setcommandused(user, getcommandused(user)+1)

    if message.content.startswith('1search'):
        await message.channel.send("Sorry, this isn't *Dank Memer*, buddy.")
        setcommandused(user, getcommandused(user)+1)
  
    if message.content.startswith('1leaderboard1'):
        setcommandused(user, getcommandused(user)+1)
        leaderboards = []
        for key, value in coins.items():
            leaderboards.append(LeaderBoardPosition(key, value))
        top = sorted(leaderboards, key=lambda x: x.coins[0], reverse=True)
        embed = discord.Embed(title='Richest (in terms of coin1)', color=0x1fd469)
        embed.add_field(name=f'**<< 1 >>** {client.get_user(top[0].user)}', value=f"""**{top[0].coins[0]}** :joy:'s""", inline=False)
        try:
            embed.add_field(name=f'**<< 2 >>** {client.get_user(top[1].user)}', value=f"""**{top[1].coins[0]}** :joy:'s""", inline=False)
            try:
                embed.add_field(name=f'**<< 3 >>** {client.get_user(top[2].user)}', value=f"""**{top[2].coins[0]}** :joy:'s""", inline=False)
                try:
                    embed.add_field(name=f'**<< 4 >>** {client.get_user(top[3].user)}', value=f"""**{top[3].coins[0]}** :joy:'s""", inline=False)
                    try:
                        embed.add_field(name=f'**<< 5 >>** {client.get_user(top[4].user)}', value=f"""**{top[4].coins[0]}** :joy:'s""", inline=False)
                    except IndexError: pass
                except IndexError: pass
            except IndexError: pass
        except IndexError: pass
        await message.channel.send(embed=embed)

    if message.content.startswith('1leaderboard2'):
        setcommandused(user, getcommandused(user)+1)
        leaderboards = []
        for key, value in coins.items():
            leaderboards.append(LeaderBoardPosition(key, value))
        top = sorted(leaderboards, key=lambda x: x.coins[1], reverse=True)
        embed = discord.Embed(title='Richest (in terms of coin2)', color=0x1fd469)
        embed.add_field(name=f'**<< 1 >>** {client.get_user(top[0].user)}', value=f"""**{top[0].coins[1]}** :rofl:'s""", inline=False)
        try:
            embed.add_field(name=f'**<< 2 >>** {client.get_user(top[1].user)}', value=f"""**{top[1].coins[1]}** :rofl:'s""", inline=False)
            try:
                embed.add_field(name=f'**<< 3 >>** {client.get_user(top[2].user)}', value=f"""**{top[2].coins[1]}** :rofl:'s""", inline=False)
                try:
                    embed.add_field(name=f'**<< 4 >>** {client.get_user(top[3].user)}', value=f"""**{top[3].coins[1]}** :rofl:'s""", inline=False)
                    try:
                        embed.add_field(name=f'**<< 5 >>** {client.get_user(top[4].user)}', value=f"""**{top[4].coins[1]}** :rofl:'s""", inline=False)
                    except IndexError: pass
                except IndexError: pass
            except IndexError: pass
        except IndexError: pass
        await message.channel.send(embed=embed)
    
    if message.content.startswith('1share_coin1'):
        setcommandused(user, getcommandused(user)+1)
        try:
            target, amount = message.content.split(' ')[1:]
            amount = int(amount)
        except ValueError:
            await message.channel.send('You provided invalid arguments, please try that again.')
        target = target[2:-1]
        if target[0] == '!':
            target = target[1:]
        target = int(target)
        await message.channel.send(f'Target: {target}')
        if amount > getcoins(user)[0]:
            await message.channel.send("You don't even have that many coins, smh.")
        if amount < 0:
            await message.channel.send("Nice try, genius.")
            return
        setcoins(target, getcoins(target)[0]+amount)
        setcoins(user, getcoins(user)[0]-amount)
        await message.channel.send('Successful')

    if message.content.startswith('1share_coin2'):
        setcommandused(user, getcommandused(user)+1)
        try:
            target, amount = message.content.split(' ')[1:]
            amount = int(amount)
        except ValueError:
            await message.channel.send('You provided invalid arguments, please try that again.')
        target = target[2:-1]
        if target[0] == '!':
            target = target[1:]
        target = int(target)
        await message.channel.send(f'Target: {target}')
        if amount > getcoins(user)[1]:
            await message.channel.send("You don't even have that many coins, smh.")
        if amount < 0:
            await message.channel.send("Nice try, genius.")
            return
        setcoins(target, getcoins(target)[1]+amount)
        setcoins(user, getcoins(user)[1]-amount)
        await message.channel.send('Successful')
    
    if message.content == '1rob':
        await message.channel.send("Don't rob people, that's illegal!")
        setcommandused(user, getcommandused(user)+1)
        
    if message.content == '1work':
       await message.channel.send ("If you want to get a job, go check out #custom-commands or #information")
       setcommandused(user, getcommandused(user)+1)
      
    if message.content == '169':
       await message.channel.send ("*Nice*")
       setcommandused(user, getcommandused(user)+1)
      
    elif message.content == '1status':
        number = random.randint(1,21)
        setcommandused(user, getcommandused(user)+1)
        if number <= 5:
            await message.channel.send("I'm doing well, thanks for asking")
        elif number <= 10:
            await message.channel.send("I'm fine, how are you?")
        elif number <= 15:
            await message.channel.send("Eh, I'm doing okay, you?")
        elif number <= 20:
            await message.channel.send("I'm doing fantastic!")
        elif number <= 21:
            await message.channel.send("I was doing well until stumbled upon you...jk, jk, you're great" )

    if message.content.startswith('1info'):
        setcommandused(user, getcommandused(user)+1)
        embed = discord.Embed(title=f"{message.author}'s info",color=0x456289)
        embed.add_field(name="**:joy:'s**",value=f'{getcoins(user)[0]}')
        embed.add_field(name="**:rofl:'s**",value=f'{getcoins(user)[1]}')
        embed.add_field(name='**Commands Used:**',value=f'{getcommandused(user)}',inline=False)
        embed.add_field(name='**Messages Sent:**',value=f'{getmessagesent(user)}')
        await message.channel.send(embed=embed)
            
    save_all()


client.run('NzEzNTI1MTAxMTk4NTczNTk4.Xsha7A.zE2IUWCdbUIo6EkiMHPIxapSMME')