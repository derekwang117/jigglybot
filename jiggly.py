import discord
from discord.ext import commands

import asyncio


bot = commands.Bot(command_prefix=".")
token = "ODQ0MjYyNzU4ODQxNDUwNTE2.YKP29w.P3yXpSdmvEMG5VtllstodR_ne2E"


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if 'copium' in message.content.lower() or 'sadge' in message.content.lower():
        embed = discord.Embed(title='Hey {}, do you know about the CAPS at the State University of New York Stony Brook University at Stony Brook, New York'.format(message.author),
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
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


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


def main():
    bot.run(token)


if __name__ == '__main__':
    main()
