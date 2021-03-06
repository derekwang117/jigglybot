import os
import asyncio
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

import BlackJack
from BlackJack import BlackJackBoard
import database

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')
token = os.environ.get('discord_bot_jiggly_token')


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild.id == 234850044124069888:
        if 'ken' in message.content.lower() or 'ryu' in message.content.lower() or 'pikachu' in message.content.lower():
            await message.channel.send('busted')
        if message.author.id == 249331440011968516:
            choice = random.randrange(10)
            if choice < 3:
                await message.channel.send('cringe!!!')
            elif choice < 6:
                await message.channel.send('loser!!!')
            elif choice < 9:
                await message.channel.send('ur mom!!!')
            elif choice < 10:
                await message.channel.send("8th place :)")

    if message.guild.id == 655969060248616990:
        if message.author.discriminator == "1906":
            if "kys" in message.content.lower() or "kill yourself" in message.content.lower():
                await message.channel.send("https://cdn.discordapp.com/attachments/656232507049639966/928386071782363146/unknown.png")

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    rng_ping = random.random()
    if rng_ping < 0.01:
        await ctx.channel.send('ping')
    else:
        await ctx.channel.send("pong")


@bot.command()
async def fizzbuzz(ctx, upper: int):
    for number in range(1, upper + 1):
        string = ""
        if number % 3 == 0:
            string += "fizz"
        if number % 5 == 0:
            string += "buzz"
        if string == "":
            string += str(number)
        await ctx.channel.send(string)


@bot.command()
async def roll(ctx, arg: int):
    x = random.randint(1, arg)
    await ctx.channel.send('{0} rolls {1} (1-{2})'.format(ctx.message.author, x, arg))


@bot.command()
async def deathroll(ctx, other: discord.Member = None, rolled: int = 0):
    if other is None or rolled <= 0:
        return
    is_other_turn = False
    roller = ctx.message.author
    while rolled != 1:
        original = rolled
        rolled = random.randint(1, rolled)
        if not is_other_turn:
            roller = ctx.message.author
        else:
            roller = other
        await ctx.channel.send('{0} rolls {1} (1-{2})'.format(roller, rolled, original))
        is_other_turn = not is_other_turn
        await asyncio.sleep(1)
    await ctx.channel.send('{} lost the roll'.format(roller))


@bot.command()
async def coins(ctx):
    author = ctx.message.author
    await ctx.channel.send("{0} has {1} coins".format(author.name, database.get_coins(author.id)))


@bot.command()
@commands.cooldown(1, 60*60*23, BucketType.user)
async def gank(ctx):
    database.add_coins(ctx.message.author.id, 100)
    await ctx.channel.send("{} has ganked and gotten 100 coins".format(ctx.message.author))


@bot.command()
async def blackjack(ctx, coins: int = 0):
    def check(reaction, user):
        x = user == ctx.message.author
        y = reaction.message == message
        z = str(reaction.emoji) == '????' or str(reaction.emoji) == '????'
        return x and y and z

    if coins < 0:
        coins = 0
    if coins > database.get_coins(ctx.message.author.id):
        await ctx.channel.send("Sorry, you do not have enough coins to wager that bet")

    else:
        board = BlackJackBoard()
        embed = discord.Embed(title='Blackjack with {}'.format(ctx.message.author),
                              description='You wager {0} coins\n'
                                          'React H to hit and S to stand\n\n'
                                          '{1}\n{2}\n'
                                          '====================='
                              .format(coins, board.user_state(), board.dealer_start()))
        message = await ctx.channel.send(embed=embed)

        reaction = None
        user = None

        if BlackJack.get_value(board.dealer) == 21:
            embed.description += '\nThe dealer hit blackjack, you lose!'
            await message.edit(embed=embed)
            board.end()
            database.add_coins(ctx.message.author.id, -coins)

        await message.add_reaction('????')
        await message.add_reaction('????')
        while not board.isDone:
            # get next react
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)
            except asyncio.TimeoutError:
                await ctx.channel.send('Blackjack timed out')
                board.end()
            else:
                # if react is hit
                if str(reaction.emoji) == '????':
                    embed.description += '\n\nYou hit'
                    if not board.hit(board.player):
                        embed.description += '\n{}\n\nYou went over 21, you lose!'.format(board.user_state())
                        await message.edit(embed=embed)
                        board.end()
                    else:
                        embed.description += '\n{}'.format(board.user_state())
                        await message.edit(embed=embed)

                # if react is stand
                else:
                    embed.description += '\n\nYou stand'
                    embed.description += '\n{0}\n{1}\n'.format(board.user_state(), board.dealer_state())
                    await message.edit(embed=embed)
                    await asyncio.sleep(0.5)

                    while BlackJack.get_value(board.dealer) < 17:
                        embed.description += '\nThe dealer hits'
                        if not board.hit(board.dealer):
                            embed.description += '\n{}'.format(board.dealer_state())
                            embed.description += '\n\nThe Dealer went over 21, you win!'
                            board.end()
                            board.isWinner = 1
                        else:
                            embed.description += '\n{}\n'.format(board.dealer_state())
                        await message.edit(embed=embed)
                        await asyncio.sleep(0.5)

                    if not board.isDone:
                        board.end()
                        p_value = BlackJack.get_value(board.player)
                        d_value = BlackJack.get_value(board.dealer)
                        embed.description += '\nYou have {0} while the dealer has {1}, '.format(p_value, d_value)
                        if p_value > d_value:
                            embed.description += 'you win!'
                            board.isWinner = 1
                        elif p_value == d_value:
                            embed.description += 'you tie!'
                            board.isWinner = 0
                        else:
                            embed.description += 'you lose!'
                        await message.edit(embed=embed)

            if user:
                await message.remove_reaction(reaction, user)

        if board.isWinner == 1:
            database.add_coins(ctx.message.author.id, coins)
        elif board.isWinner == -1:
            database.add_coins(ctx.message.author.id, -coins)


@bot.command(name='caps')
async def copypasta_caps(ctx):
    embed = discord.Embed(
        title='Hey {}, do you know about the CAPS at the State University of New York Stony Brook University at Stony Brook, New York'.format(
            ctx.message.author),
        description='In the State University of New York Stony Brook University at Stony Brook, New York, '
                    'Counseling and Psychological Services are available. The main webpage is [here](https://www.stonybrook.edu/caps/). '
                    'For more information about virtual counseling, click [here](https://www.stonybrook.edu/commcms/studentaffairs/caps/about/caps-is-virtual.php).\n\n '
                    'The offices in the State University of New York Stony Brook University at Stony Brook, New York are at: \n\n'
                    'West Campus:\n'
                    'Student Health Services - Second Floor\n'
                    '1 Stadium Drive\n'
                    'Stony Brook, NY 11794-3100\n\nand\n\n'
                    'HSC Office:\n'
                    'Health Science Center, 3rd floor Room 3-040F\n\n'
                    'Please note: due to the novel coronavirus, the walk-in hours are temporarily suspended')
    await ctx.channel.send(embed=embed)


@bot.command(name='10pull')
async def ten_pull(ctx):
    mirror_rate = 0.00001
    five_star = 0.01
    four_star = 0.03
    five_pull = four_pull = three_pull = 0
    mirror = 0
    for x in range(0, 10):
        pull = round(random.random(), 3)
        if pull < mirror_rate:
            mirror += 1
        if pull < five_star:
            five_pull += 1
        elif pull < four_star:
            four_pull += 1
        else:
            three_pull += 1
    username = ctx.message.author.name
    results = "{0}:\nFive star count: {1}\nFour star count: {2}\nThree star count: {3}".format(username, five_pull,
                                                                                               four_pull, three_pull)
    if (five_pull):
        results += '\n{} Five star pulled'.format(ctx.message.author.mention)

    if mirror:
        results += '\nMirror of Kalandra pulled'
    await ctx.channel.send(results)


@bot.command(name='eject')
async def eject(ctx, arg: discord.Member = None):
    if arg:
        embed = discord.Embed(title="Emergency Meeting", description='Vote to eject {}'.format(arg.mention))
        message = await ctx.send(embed=embed)
        reactions = ['????', '9??????', '8??????', '7??????', '6??????', '5??????', '4??????', '3??????', '2??????', '1??????']
        await message.add_reaction('????')
        await message.add_reaction('????')

        for x in range(0, 10):
            await message.add_reaction(reactions[x])
            await asyncio.sleep(1)
        message = await bot.get_channel(message.channel.id).fetch_message(message.id)

        if message.reactions[0].count > message.reactions[1].count:
            await arg.move_to(None)

            str = ". ?????????????????????????????? ??????????????? ??????.\n\n?????????.????????? ??????.???????????????????????? ??????. ???\n\n.?????? ?????????????????? ??? ??? . ?????? ??? ???????????????\n\n??????????????? {0} " \
                  "was ejected.??? ??????.\n\n??????'???????????? ???????????????   ??? ?????????\n\n??????????????????.?????????. ,????????????.??? . ".format(arg)

            await ctx.send(str)

        else:
            await ctx.channel.send("No one was ejected (Skipped)")

        for x in range(0, 10):
            await message.clear_reaction(reactions[x])


@bot.command(name='spike')
async def spike_blast_zone(ctx, arg: discord.Member = None):
    if (ctx.message.author.discriminator != "5749" and ctx.message.author.discriminator != "4108"):
        vc_list = []
        for channel in ctx.guild.voice_channels:
            vc_list.append(channel)
        original_vc = arg.voice.channel
        x = vc_list.index(original_vc)
        x = 0 - (len(vc_list) - x - 1)
        vc_list = vc_list[x:]
        vc_list = vc_list[:8]
        for vc in vc_list:
            await arg.move_to(vc)
        await arg.move_to(original_vc)
        await ctx.channel.send("{} got spiked (-1 stock)".format(arg))


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description='help: Shows this message\n'
                    'ping: pong\n'
                    'eject: Vote to kick a member from vc\n'
                    'spike: Spike a member down 8 channels and brings them back\n'
                    'deathroll: WoW style gambling\n'
                    'blackjack: 1 player blackjack (Enter value after blackjack to specify how much to wager)')
    await ctx.channel.send(embed=embed)


def main():
    bot.run(token)


if __name__ == '__main__':
    main()
