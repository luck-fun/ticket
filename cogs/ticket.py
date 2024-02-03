import disnake
import asyncio
import os
from disnake.ext import commands

tickets = []
# Определяем класс "ButtonView", который наследуется от disnake.ui.View.
class ButtonView(disnake.ui.View):
    def __init__(self):
        self.tickets = tickets
        super().__init__(timeout=None)


    # Создаем кнопку "button1" с соответствующей функцией-обработчиком.
    @disnake.ui.button(label="Создать тикет", style=disnake.ButtonStyle.grey, custom_id="button1")
    async def button1(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.author.id in self.tickets:
            _channel: disnake.TextChannel = disnake.utils.get(
                interaction.guild.text_channels, name=f"Обращение от {interaction.author.name}")
            if _channel:
                embed = disnake.Embed(description=f"У вас уже есть открытое обращение. {_channel.mention}")
            else:
                embed = disnake.Embed(description="У вас уже есть открытое обращение.")
            return await interaction.send(embed=embed, delete_after=10.0)

        if not disnake.utils.get(interaction.guild.categories, name="Тикеты"):
            await interaction.guild.create_category("Тикеты")

        support = interaction.guild.get_role(1175454210825916447)
        # Creates the ticket channel
        channel = await interaction.guild.create_text_channel(
            name=f"Обращение от {interaction.author.name}",
            category=disnake.utils.get(interaction.guild.categories, name="Тикеты"),
            topic=f"Тикет создан {interaction.author.name} ({interaction.author.id}) Время создания: {interaction.created_at}",
            reason=f"Тикет создан {interaction.author.name}",
        )
        self.tickets.append(interaction.author.id)
        # Sets the permissions for the ticket channel
        await channel.set_permissions(interaction.author, view_channel=True, send_messages=True, read_messages=True,
                                      read_message_history=True, attach_files=True, embed_links=True,
                                      add_reactions=True, external_emojis=True, use_external_emojis=True,
                                      use_slash_commands=True)
        await channel.set_permissions(interaction.guild.default_role, view_channel=False, send_messages=False,
                                      read_messages=False)
        await channel.set_permissions(support, view_channel=True, send_messages=True, read_messages=True,
                                      read_message_history=True, attach_files=True, embed_links=True,
                                      add_reactions=True, external_emojis=True, use_external_emojis=True,
                                      use_slash_commands=True)

        embed = disnake.Embed(title=f'Добро пожаловать на сервер {interaction.guild.name}',
                              description=f'Благодарим вас за обращение в поддержку {interaction.guild.name}\. Пожалуйста, сформулируйте свой вопрос или жалобу так, чтоб вас не пришлось переспрашивать')
        embed.set_footer(text=f'Обращение создано {interaction.author}', icon_url=interaction.author.avatar.url)
        embed.set_thumbnail(url=interaction.author.avatar.url)
        view = Button2View()
        await channel.send(embed=embed, view=view)
        await channel.send(f'{interaction.author.mention}', delete_after=0.1)

        # Sends a message to the user
        embed = disnake.Embed(title='Обращение создано',
                              description=f"Ваше обращение было создано в канале {channel.mention} \n Пожалуйста, проследуйте в этот канал и задайте там свой вопрос", color=0x2F3136)
        embed.set_footer(text=f'Обращение создано {interaction.author}', icon_url=interaction.author.avatar.url)
        embed.set_thumbnail(url=interaction.author.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Button2View(disnake.ui.View):
    def __init__(self):
        self.tickets = tickets
        super().__init__(timeout=None)

    @disnake.ui.button(label="Закрыть тикет", style=disnake.ButtonStyle.grey, custom_id="button2")
    async def button2(self, button: disnake.Button, interaction: disnake.Interaction):

            channel = disnake.utils.get(interaction.guild.channels, name=f"Обращение-от- {interaction.author.name}")
            await interaction.channel.delete()

            if interaction.author.id in self.tickets:
                self.tickets.remove(interaction.author.id)


class ButtonsRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    # Создаем команду "buttons", которая будет выводить сообщение с кнопкой.
    @commands.command()
    async def buttons(self, ctx):
        view = ButtonView()

        # Получаем роль по ее ID (необходимо указать конкретный ID вместо ...).

        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name="Поддержка")
        embed.description = f"Появились вопросы/хотите заказать? Откройте тикет по кнопке ниже! "

        embed.set_image(url="https://i.imgur.com/QzB7q9J.png")
        await ctx.send(embed=embed, view=view)

    # Создаем слушателя события "on_ready", который добавляет персистентную кнопку.
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return


        self.bot.add_view(ButtonView(), message_id=1198631907886374913)


# Функция setup, которая добавляет класс ButtonsRole как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(ButtonsRole(bot))
