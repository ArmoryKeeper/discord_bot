from infos_git import *
import discord
import datetime
import requests
import json
import subprocess

# kreiranje objekta klienta
client = discord.Client()


# prilikom ukljucenja
@client.event
async def on_ready():
    general_channel = client.get_channel(hodnik)
    await general_channel.send('Yay online sam, vreme ukljucenja: ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    await general_channel.send('Za prikazivanje opcija kucajte komandu help')


@client.event
async def on_message(message):
    general_channel = client.get_channel(hodnik)
    poruka = message.content.lower()
    global response
    global response_json
    if poruka == 'petko':
        await general_channel.send('Ko? Sta? ')

    # if poruka == 'rad main':
    #     subprocess.call(['python','bot_main.py'])

    # if poruka == 'rad alt':
    #     subprocess.call(['python','bot_alt.py'])

    if poruka == 'cls': # ping - pong za proveru rada bota
        await message.delete()

    if poruka == 'help':
        await general_channel.send(help)
    
    if poruka == 'bot_version':
        myEmbed = discord.Embed(title = 'Trenutna verzija', description = 'Trenutna verzija bota je v1.1', color=0x95eb34 )
        myEmbed.add_field(name='Verzija:', value ='v1.1')
        myEmbed.add_field(name='Datum zadnjeg update:',value='23.11.2021. godine')
        myEmbed.set_footer(text='Uskoro nove stvari! Stay tuned!')
        myEmbed.set_author(name='Bole')
        await general_channel.send(embed=myEmbed)       
    
    if poruka == 'finansije':
        finansijechannel = client.get_channel(finansije)
        poruka = message.content.split()
        novi_unos = poruka[1] +' '+ poruka[2] + ' ' + poruka[3]

        await finansijechannel.send(f'Spremno za update sledece: {novi_unos}')
    
    if poruka == 'vreme osvezi':
        response = requests.get(url="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/301537?apikey=CA9NQQq3k812FGW4wXWlCvA4pOD2onbY&details=true&metric=true")
        await general_channel.send(response.status_code)
        response_json = json.loads(response.content)

    if message.content.lower().startswith('vreme') and message.author.name != 'Jarvis':
        
        if message.content.lower() == 'vreme posao':
            temp07 = ''
            temp15 = ''
            rainprob = ''
            for sets in response_json:
                if sets['DateTime'].split('T')[1].split(':')[0] == '07':
                    temp07 = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                elif sets['DateTime'].split('T')[1].split(':')[0] == '15':
                    temp15 = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                    rainprob += str(sets['RainProbability']) + '%'       
            await general_channel.send(f'''Vremenska prognoza Uzice:\n
                    Temperatura u 0700: {temp07}
                    Temperatura u 1500: {temp15}
                    Mogucnost padanja kise: {rainprob}''')

        if message.content.lower() == 'vreme 3h':
            brojac = 0
            sat = ''
            temp = ''
            vv = ''
            rainprob = ''
            ro = ''
            iconp = ''
            for sets in response_json:
                if brojac == 3:
                    break
                sat = sets['DateTime'].split('T')[1].split(':')[0]
                temp = str(sets['Temperature']['Value']) + sets['Temperature']['Unit']
                ro = str(sets['RealFeelTemperature']['Value']) + sets['RealFeelTemperature']['Unit']
                iconp = sets['IconPhrase']
                vv = str(sets['RelativeHumidity'])
                rainprob = str(sets['RainProbability']) + '%'

                await general_channel.send(f'''  Vremenska prognoza Uzice za {sat}h:\n
                                Temperatura : {temp}
                                Realan osecaj : {ro}
                                Oblacnost: {iconp}
                                Vlaznost vazduha: {vv}
                                Mogucnost padanja kise: {rainprob}

                                ''')
                brojac += 1

        
        
    
    if ((not poruka in lista_komandi) and (message.author.name != 'Jarvis')) == True:
        await message.delete()
        await general_channel.send('Niste uneli pravilnu komandu stoga vam je poruka obrisana')



# Pokretanje klijenta
client.run(token)