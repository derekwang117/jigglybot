import asyncio
import random

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')
token = "insert token here"


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild.name == 'hoo haa':
        if 'ken' in message.content.lower() or 'pikachu' in message.content.lower():
            await message.channel.send('busted')

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    rng_ping = random.random()
    if rng_ping < 0.01:
        await ctx.channel.send('ping')
    else:
        await ctx.channel.send("pong")


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
        reactions = ['🔟', '9️⃣', '8️⃣', '7️⃣', '6️⃣', '5️⃣', '4️⃣', '3️⃣', '2️⃣', '1️⃣']
        await message.add_reaction('👍')
        await message.add_reaction('👎')

        for x in range(0, 10):
            await message.add_reaction(reactions[x])
            await asyncio.sleep(1)
        message = await bot.get_channel(message.channel.id).fetch_message(message.id)

        if message.reactions[0].count > message.reactions[1].count:
            await arg.move_to(None)

            str = ". 　　　。　　　　•　 　ﾟ　　。 　　.\n\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {0} " \
                  "was ejected.　 。　.\n\n　　'　　　　 　ﾟ　　。   　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 . ".format(arg)

            await ctx.send(str)

        else:
            await ctx.channel.send("No one was ejected (Skipped)")

        for x in range(0, 10):
            await message.clear_reaction(reactions[x])


@bot.command(name='spike')
async def spike_blast_zone(ctx, arg: discord.Member = None):
    vc_list = []
    for channel in ctx.guild.voice_channels:
        vc_list.append(channel)
    original_vc = arg.voice.channel
    x = vc_list.index(original_vc)
    x = 0 - (len(vc_list) - x - 1)
    vc_list = vc_list[x:]
    vc_list = vc_list[:10]
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
                    'spike: Spike a member down 10 channels and brings them back')
    await ctx.channel.send(embed=embed)



def main():
    bot.run(token)


if __name__ == '__main__':
    main()
