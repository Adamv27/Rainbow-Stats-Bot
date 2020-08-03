import discord
import requests
from bs4 import BeautifulSoup

       
class MyClient(discord.Client):
    #Lets you know bot is logged in
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
             
        if message.content.startswith('!stats'):
            #just take the username as a string
            username = message.content[6:]
            username = str(username.strip())

            URL = 'https://r6.tracker.network/profile/pc/'+username
            
            #request to connect to the stats website
            headers = {"User-Agemt": 'user agent here'}
            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, 'html.parser')
            kd = []
            
            for div in soup.findAll('div', attrs={'class': 'trn-card__content trn-card--light pt8 pb8'}):
                await message.channel.send(div.text.strip())

            for div in soup.findAll('div', attrs={'style': 'display: flex; justify-content: space-between;'}):
                await message.channel.send(div.text.strip())
       
client = MyClient()
client.run('put client token here')
