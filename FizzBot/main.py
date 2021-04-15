# bot.py
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import urllib.request
import discord
import os

TOKEN = " YOUR TOKEN HERE "

command = '-'

def champList(summoner):
  URL ="https://championmastery.gg/summoner?summoner="+summoner+"&region=NA"

  #Create a handle, page, to handle the contents of the website
  page = requests.get(URL)

  #Store the contents of the website under doc
  doc = lh.fromstring(page.content)

  #Parse data that are stored between <tr>..</tr> of HTML
  tr_elements = doc.xpath('//tr')

  champs=[]

  for i in range(1,len(tr_elements)-1):
    arr = (tr_elements[i].text_content().split())
    temp =""
    for x in arr:
      try:
        x != int(x)
        break;
      except ValueError:
        temp+=(x+" ")
    champs.append(temp.strip())

  return champs

def counterPick(champ):
  URL = 'https://lolcounter.com/champions/'+champ
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, 'html.parser')#gets website data

  div = soup.find('div',class_='weak-block') #cleans content to only be counter pick table

  tempLinkArr=[]# temp counter champ array
  counterArr=[]#final counter array

  for a in div.find_all('a', href=True): #finds all the links in counter pick table
      tempLinkArr.append(a['href']) #adds counter champ to linkArr

  for i in range(0,len(tempLinkArr)-1,4): #cleans data
    counterArr.append(tempLinkArr[i].split("/")[-1])

  counterArr=counterArr[:-1]

  return counterArr

def addUser(username, summoner):
  f = open("databaseIO.txt", "w")
  f.write("1 " + summoner + " " + username)
  f.close()
  os.system("java Database.java")

def getUser(username):
  f = open("databaseIO.txt", "w")
  f.write("0 " + username)
  f.close()
  os.system("java Database.java")
  f = open("databaseIO.txt", "r")
  a = (f.read())
  f.close()
  return a

def removeUser(username):
  f = open("databaseIO.txt", "w")
  f.write("2 " + username)
  f.close()
  os.system("java Database.java")

def readMessage():
    f = open("databaseIO.txt", "r")
    return f.readline(3)

def itemBuild(champ):
  page = requests.get("https://u.gg/lol/champions/"+champ+"/build").content
  soup = BeautifulSoup(page,'html.parser')
  images=soup.findAll('img')
  image_src = [x['src'] for x in images]
  image_src = [x for x in image_src if x.endswith('.png')]
  image_array = []
  print("\n".join(image_src))
  counter=0
  for image in image_src:
    urllib.request.urlretrieve(image, "src/"+str(counter)+".png")
    image_array.append("src/"+str(counter)+".png")
    counter+=1
  return image_array

def spell(champ):
  page = requests.get("https://u.gg/lol/champions/"+champ+"/build").content
  soup = BeautifulSoup(page,'html.parser')
  images=soup.findAll('img')
  image_src = [x['src'] for x in images]
  image_src = [x for x in image_src if x.endswith('.png')]
  image_array = []
  counter=0
  for image in image_src:
    if "spell/Su" in image:
      urllib.request.urlretrieve(image, "srcSpell/"+str(counter)+".png")
      image_array.append("srcSpell/"+str(counter)+".png")
      counter+=1
  return image_array

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global command
    if message.author == client.user:
        return
    if (str(message.content)== command + "help"):
        await message.channel.send("**Commands:**")
        await message.channel.send("**" + command + "register LEAGUE_USERNAME** allows access to all other commands.")
        await message.channel.send("**" + command + "delete** delete league username associated with your account.")
        await message.channel.send("**" + command + "counter CHAMP** returns the 5 best counter champions that you have played.")
        await message.channel.send("**" + command + "champlist LEAGUE_USERNAME** returns all the champions a given league user has played.")
        await message.channel.send("**" + command + "spell CHAMP** the best spells for a given champion.")
        await message.channel.send("**" + command + "build CHAMP** some good old fashion spam.")
        await message.channel.send("**" + command + "change COMMAND** change the string used for your command! Default is '-'")

    if (str(message.content).split()[0] == command + "register"):
        addUser(str(message.content).split()[1],str(message.author))
        await message.channel.send("Registered!")

    elif str(message.content)[0]== command and getUser(str(message.author)).strip()=="Error: User not found" and str(message.content).split()[0] != "-delete":
      await message.channel.send("Use the " + command + "register command to get a customized experience.")
    else:
      if (str(message.content).split()[0]== command + "counter"):
        arr=counterPick(str(message.content).split()[1])
        arr2=champList(str(message.author)) 
        print(arr)
        print(arr2)
        counter=1
        for i in range(len(arr)):
          if arr[i] in arr2:
            await message.channel.send(str(counter) +". "+arr[i])
            counter+=1
            if (counter==6):
              break;
        if counter==1:
          await message.channel.send("Oh No! You do not have any of the counter champs!")
      if (str(message.content).split()[0] == command + "champlist"):
        arr = champList(message.content.split()[1])
        await message.channel.send(", ".join(arr))
      if (str(message.content).split()[0] == command + "build"):
        arr = itemBuild(message.content.split()[1])
        for image in arr:
          await message.channel.send(file=discord.File(image))
          os.remove(image)
      if (str(message.content).split()[0] == command + "spell"):
        arr = spell(message.content.split()[1])
        for image in arr:
          await message.channel.send(file=discord.File(image))
          os.remove(image)
      if (str(message.content).split()[0] == command + "test"):
        getUser(str(message.author))
      if (str(message.content).split()[0] == command + "delete"):
          removeUser(str(message.author))
          if readMessage()[0] == 'E':
              await message.channel.send("There was nothing to delete")
              await message.channel.send("Use -register to get a customized experience")
          else:
              await message.channel.send("Deleted!")
      if (str(message.content).split()[0] == command + "change"):
        command = str(message.content).split()[1]
        await message.channel.send("Changed!")

client.run(TOKEN)