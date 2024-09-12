"""
NoProfanity
A plugin to detect and handle profanity in messages.

Copyright (C) 2024 ItsAsheer (@NullyIsHere)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import nextcord
from nextcord.ext import commands
import aiohttp
import json

def extract_message_info(message):
    if all(hasattr(message, attr) for attr in ['id', 'content', 'author']):
        server_id = getattr(message.guild, 'id', None) or getattr(message.server, 'id', None)
        if server_id:
            return {
                'message_id': message.id,
                'content': message.content,
                'author_id': message.author.id,
                'server_id': server_id
            }
    return None

class NoProfanity(commands.Cog):
    """A template cog written for unifier-plugin template repo"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self, ctx):
        await ctx.send('This is a template plugin!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_info = extract_message_info(message)
        if message_info is None:
            return

        async with aiohttp.ClientSession() as session:
            url = 'https://vector.profanity.dev'
            headers = {'Content-Type': 'application/json'}
            data = {'message': message_info['content']}

            async with session.post(url, headers=headers, json=data) as response:
                response_data = await response.json()

                if response_data.get("isProfanity"):
                    toret = {
                        'unsafe': True,
                        'description': f'Message flagged by NoProfanity, with score {response_data.get("score")}, for "{response_data.get("flaggedFor")}"',
                        'target': {message_info['author_id'], 60},
                        'delete': [message_info['message_id']],
                        'restrict': {},
                        'data': {}
                    }
                    # Handle the response data as needed
                    print(toret)

def setup(bot):
    bot.add_cog(NoProfanity(bot))
