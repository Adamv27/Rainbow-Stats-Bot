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

            for div in soup.findAll('div', attrs={'class': 'trn-card__content trn-card--light pt8 pb8'}):
                await message.channel.send(div.text.strip())

            for div in soup.findAll('div', attrs={'style': 'display: flex; justify-content: space-between;'}):
                await message.channel.send(div.text.strip())

            #Link to get top operators 
            URL = F'https://r6.tracker.network/profile/pc/{username}/operators'
            response = requests.get(URL)
            soup = BeautifulSoup(response.text, 'html.parser')

            # attacker operator
            attackRow = soup.select('.trn-table__row')[1]
            attacker = attackRow.text.split()
            
            # only prints the name and time played
            await message.channel.send(f'{attacker[0]}')
            await message.channel.send(f'{attacker[1]} {attacker[1]}')

            # defender operator
            defendRow = soup.find(class_='trn-card trn-card--ftr-blue')
            defender = defendRow.text.split()

            await message.channel.send(f'{defender[18]}')
            await message.channel.send(f'{defender[19]} {defender[20]}')

client = MyClient()
