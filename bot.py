import discord
from discord import member
from discord.ext import commands
import discord.utils
from discord.ext.commands import bot



client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Prefix !'))
    print('Zalogowano do bota.')

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.messege.channel
    await client.send_message(channel, '{} has added {} to the messege: {}'.format(user.name, reaction.emoji, reaction.messege.content))

@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.messege.channel
    await client.send_message(channel, '{} has removed {} to the messege: {}'.format(user.name, reaction.emoji, reaction.messege.content))

@client.command()
@commands.has_permissions(administrator=True)
async def activity(ctx , * , activity):
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=activity))
    embed = discord.Embed(title='Wykonano', description=f'Zmieniono status bota {activity}', color=discord.Colour.green())
    embed.set_footer(text='Powered by Discord.py')
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error,):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌ Error', description='⚠Nie masz uprawnień do tego polecenia ⚠',
                              color=discord.Colour.red())
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Powered by Discord.py")
        await ctx.messege.delete()

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='❌ Error',description='⚠ Niepoprawny argument tego polecenia spróbuj jeszcze raz. ⚠',color=discord.Colour.red())
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
        await ctx.send(embed=embed)
        await ctx.messege.delete()

@client.command()
async def docs(ctx):
    embed = discord.Embed(title='Dokumentacja bota',
                          description='Oto dokumentacja bota https://discordpy.readthedocs.io/en/stable/',
                          color=discord.Colour.purple())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    await ctx.send(embed=embed)


@client.command(aliases=['in'])
async def invite(ctx):
    embed = discord.Embed(title='Dokumentacja bota',
                          description='Oto zaproszenie na serwer https://discord.gg/d42YAgwUs5',
                          color=discord.Colour.purple())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    await ctx.send(embed=embed)

Owner = 'Sponton#4170'

@client.command(aliases=['ow'])
async def owner(ctx):
    embed = discord.Embed(title='Właściciel bota',description='Właścicielem bota jest '+ Owner,color=discord.Colour.purple())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title='Wykonano polecenie', description='Pomoślnie usunięto ' + amount + 'wiadomośći',
                          color=discord.Colour.green())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='Nie podano powodu'):
    try:
        await member.send(embed=discord.Embed(title='Wykonano',
                                              description=member.mention + ' został pomyślnie wyrzucony, Powód: ' + reason,
                                              color=discord.Colour.green()))
    except:
        await ctx.send(embed=discord.Embed(title='Error', description=member.name + "Ten członek ma wyłączone DM",
                                           color=discord.Colour.red()))

    await member.kick(reason=reason)
    embed = discord.Embed(title='Wykonano',
                          description=member.mention + 'został pomyślnie wyrzucony, Powód:' + reason, color=discord.Colour.green())
    await ctx.send(embed=embed)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='Nie podane powodu.'):
    embed = discord.Embed(title='Wykonano',description=member.mention + ' został zbanowany powód: ' + reason,color=discord.Colour.red())
    await member.ban(reason=reason)
    await member.send('Zostałeś zbanowny powód: ' + reason)
    await ctx.send(embed=embed)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    assert isinstance(banned_users)
    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            embed = discord.Embed(title='Wykonano', description='✅' + member.mention + ' pomyślnie został unbanowany.',
                                  color=discord.Colour.green())
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
            return

    embed = discord.Embed(title='Error', description='❌' + member.mention + ' nie został znaleziony.',
                          color=discord.Colour.red())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")

    await ctx.send(embed=embed)

@client.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, ):
    muted_role = ctx.guild.get_role(839100357174755368)

    await member.add_roles(muted_role)

    embed = discord.Embed(title='Wykonano', description='✅ ' + member.mention + ' pomyślnie został zmutowny.',
                          color=discord.Colour.green())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    embed.add_field(name='ID', value=member.id, inline=True)

@client.command(aliases=['um'])
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    muted_role = ctx.guild.get_role(839100357174755368)

    await member.remove_roles(muted_role)

    embed = discord.Embed(title='Wykonano', description='✅ ' + member.mention + ' pomyślnie został unmutowany.',
                          color=discord.Colour.green())
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")

@client.command(aliases=['user', 'info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(title='Info ' + member.name, description=member.mention, color=discord.Colour.blue())
    embed.add_field(name='ID', value=member.id, inline=True)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Wywołane przez {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def pomoc(ctx):
    author = ctx.messege.author

    embed = discord.Embed(title='Help command', description='Help command', color=discord.Colour.orange())

    embed.set_author(name='Help:')
    embed.set_field(name='!help', value = 'Help command', inline=False)

    await ctx.send(author, embed=embed)
    await member.send('Wiadomość została wysłana w DM.')


TOKEN = "ODM3MDQxMDY4NzM3NDI5NTQ1.YImxPg.1em6dGDfQn0LGHfulH9WHP821zU"

client.run(TOKEN)
