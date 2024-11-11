import discord
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot siap! Masuk sebagai {bot.user}')

@bot.command()
async def create_channel(ctx, channel_name: str):
    # Validasi format input
    if not re.match(r'^\d{3}-\d{2}-[a-zA-Z0-9-]+-[a-zA-Z0-9-]+$', channel_name):
        await ctx.send("Format input salah! Harus seperti ini: 072-24-pt-dummy-tech-mr-alif")
        return

    categories = [cat for cat in ctx.guild.categories if cat.name.startswith("QUO-")]

    if not categories:
        new_category = await ctx.guild.create_category(f"QUO-{channel_name.split('-')[0]}-001")
        await create_channel_in_category(new_category, channel_name, ctx)
        return

    categories.sort(key=lambda x: int(x.name.split('-')[-1]))
    last_category = categories[-1]

    if len(last_category.channels) >= 50:
        new_category_number = str(int(last_category.name.split('-')[-1]) + 1).zfill(3)
        new_category = await ctx.guild.create_category(f"QUO-{channel_name.split('-')[0]}-{new_category_number}")
        await create_channel_in_category(new_category, channel_name, ctx)
    else:
        await create_channel_in_category(last_category, channel_name, ctx)

async def create_channel_in_category(category, channel_name, ctx):
    new_channel = await category.create_text_channel(channel_name)
    await ctx.send(f'Text channel {new_channel.mention} berhasil dibuat di kategori {category.name}')

    # Update kategori
    new_channel_number = re.findall(r'\d+', channel_name)
    if new_channel_number:
        new_number = new_channel_number[0].zfill(3)
        old_name_parts = category.name.split('-')
        updated_category_name = f"{old_name_parts[0]}-{old_name_parts[1]}-{new_number}"
        await category.edit(name=updated_category_name)
        print(f"Updated category name to: {updated_category_name}")

        # Kirim pesan ke text channel 'quo-library'
        library_channel = discord.utils.get(ctx.guild.text_channels, name='quo-library')
        if library_channel:
            await library_channel.send(f'QUO baru dibuat: {new_channel.mention}')

@bot.command()
async def hello(ctx):
    user_name = ctx.author.name
    await ctx.send(f"Halo, {user_name}!")

bot.run('MTMwMDQ0NDQyODQ2ODQ4NjIxNQ.GoRkBb.i8mT0rCQXu4dVYmMXkGnQIvfiHQqWJ_EwlEwj8')
