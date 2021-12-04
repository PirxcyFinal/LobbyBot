import os

import aiohttp
try:
  import json
  from translate import Translator
  import requests
  import sanic
  import random
  import sys
  import time
  import base64
  import string
  from sanic import Sanic
  from sanic_session import Session, InMemorySessionInterface
  from sanic.response import redirect
  import discord
  import asyncio
  from functools import partial, wraps
  import datetime
  import traceback
  import fortnitepy
  from fortnitepy.ext import commands
  import discord
  from discord.ext import commands as comands
  from discord.ext import tasks
  from discord.utils import get
  from jinja2 import Environment, FileSystemLoader
  from typing import Callable, Any, Type
except ModuleNotFoundError:
  os.system("bash main.sh")
  exit(1)

accounts = "accounts.json"
used_accounts = "used_accounts.json"
fortnite_messsage = """
Hey, This Bot was Made Via PirxcyBot
Join The Discord To Get Your Own!
"""
full_access = [733302490753269852]
restart_file = "restart.json"
onlinebots = {}#where bots are stored
translate_user = []
join_message = {}#fortnite join messages
login_codes = {}#stores login codes
codes_login = {}
user_and_json = {}
cosmetics_name = "items.json"
#cache cosmetics cus i cba ratelimits gang shit
try:
  items = requests.get('https://fortnite-api.com/v2/cosmetics/br/').json()['data']
  with open(
    cosmetics_name,
    'w'
  ) as f:
    json.dump(
      items,
      f,
      indent=2
    )
except:
  print('Fuck I\'m Ratelimited Sticking to Cached')
  

#update restarts
with open(restart_file) as f:
  restart = json.load(f)

with open(
  restart_file,
  'w'
) as f:
  restarts = restart['restarts']
  restart['restarts'] = restarts + 1
  json.dump(
    restart,
    f
  )
  
def load_cosmetics():
  with open(cosmetics_name) as f:
    try:
      data = json.load(f)
      return data
    except json.decoder.JSONDecodeError:
      print("An Json Decode Error Occured While Reading items.json (Contact Pirxcy for Help)")
      sys.exit()

class FN_COSMETIC:
  def __init__(self, data):
    self.data = data
    self.id = self.data['id']
    self.name = self.data['name']
    self.description = self.data['description']
    self.type = self.data['type']
    self.rarity = self.data['rarity']
    self.series = self.data['series']
    self.set = self.data['set']
    self.introduction = self.data['introduction']
    self.images = self.data['images']
    self.variants = self.data['variants']
    self.searchTags = self.data['searchTags']
    self.gameplayTags = self.data['gameplayTags']
    self.metaTags = self.data['metaTags']
    self.showcaseVideo = self.data['showcaseVideo']
    self.dynamicPakId = self.data['dynamicPakId']
    self.displayAssetPath = self.data['displayAssetPath']
    self.definitionPath = self.data['definitionPath']
    self.path = self.data['path']
    self.added = self.data['added']
    self.shopHistory = self.data['shopHistory']
    
class cosmetic:
  async def get(id:str) -> FN_COSMETIC:
    cosmetics = load_cosmetics()
    for data in cosmetics:
      if data['id'] == id:
        return FN_COSMETIC(data)
      else:
        continue
      
  async def get_variants(client, type_, variant_channel=None, selected_int=None, selected=None):
    config_overrides = {"item": type_, variant_channel: selected['tag']}
    if variant_channel != None:
      if variant_channel == 'pattern':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          pattern=str(selected_int)
        )
      if variant_channel == 'numeric':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          numeric=str(selected_int)
        )
      if variant_channel == 'clothingcolor':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          clothing_color=str(selected_int)
        )
      if variant_channel == 'jerseycolor':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides,
          jersey_color=str(selected_int)
        )
      if variant_channel == 'parts':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          parts=str(selected_int)
        )
      if variant_channel == 'progressive':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides,
          progressive=str(selected_int)
        )
      if variant_channel == 'particle':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          particle=str(selected_int)
        )
      if variant_channel == 'material':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          material=str(selected_int)
        )
      if variant_channel == 'emissive':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          emissive=str(selected_int)
        )
      if variant_channel == 'hair':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          hair=str(selected_int)
        )
      if variant_channel == 'mesh':
        variants = client.party.me.create_variant(
          config_overrides=config_overrides, 
          mesh=str(selected_int)
        )
      return variants

#store translations
filename = 'cache.json'
if os.path.isfile(filename):
  with open(filename, encoding='utf-8') as f:
    cache = json.load(f)
else:
  cache = {}

#config
custombot_creation = True#keep boolean
custombotoffline_reason = None#keep str

premadebot_creation = False#keep boolean
premadebotoffline_reason = "❌ I haven't made accounts to load! Will Fix Soon!"#keep str

dashboard_access = True#keep boolean
dashboardnoaccess_reason = "Transfering To Repl Since My Domain has Ran out"#keep str

translation_access = True#keep boolean
notranslationaccess_reason = "Currently Using Some Shitty API That Limits Translations! (Will Cache Necssary Translations)"#keep str
####
env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'), extensions=['jinja2.ext.do'])
loop = asyncio.get_event_loop()
app = sanic.Sanic("PirxcyBot")
start_time = datetime.datetime.utcnow()

async def clientevent(owner):
  await asyncio.sleep(600)#time to bot runs out 
  await createbot.stop(owner=owner)

async def translates(context, preferred_language):
  translator = Translator(to_lang=preferred_language)
  translation = translator.translate(context)
  translated = cache.get(
    preferred_language, 
    {}
  ).get(context)
  if translated is None:
    translator = Translator(to_lang=preferred_language)
    translated = translator.translate(context) # call translation api
    if preferred_language not in cache:
      cache[preferred_language] = {}
    cache[preferred_language][context] = translated
    with open(
      filename, 
      'w', 
      encoding='utf-8'
    ) as f:
      if "HTTPS://MYMEMORY.TRANSLATED.NET/DOC/USAGELIMITS.PHP" in cache:
        return "UNABLE TO TRANSLATE PLEASE RUN !STOPTRANSLATE"
      else:
        json.dump(
          cache,
          f, 
          indent=2
        )
  return translated

async def newbot(device_id, account_id, secret, user):
    client = fortnitepy.Client(
      auth=fortnitepy.DeviceAuth(
        device_id=device_id,
        account_id=account_id,
        secret=secret
      )
    )
    emotes = "/Game/Athena/Items/Cosmetics/Dances/PapayaComms/EID_PhoneWavePapayaComms.EID_PhoneWavePapayaComms"
    skin = "CID_030_Athena_Commando_M_Halloween"

    @client.event
    async def event_message(message):
      if message.author.id == client.user.id:
        return
      else:
        client.party.send(fortnite_messsage)

    @client.event
    async def event_ready() -> None:
      code = code_generator()
      login_codes.update({user.id:code})
      codes_login.update({code:user.id})
      print(login_codes)
      embeds=discord.Embed(title="Account Launched")
      await user.send(embed=embeds)
      if dashboard_access is True:
        embed=discord.Embed(
          title="Dashboard:", 
          description=f"""
  Login on: 
  https://pirxcybotfinal.pirxcy1942.repl.co/login
  Enter `{code}`""")
        await user.send(embed=embed)
      else:
        embd = discord.Embed(
          title="Dashboard Currently Disabled!", 
          description=f"`Reason: {dashboardnoaccess_reason}`"
        )
        await user.send(embed=embd)
      variants = client.party.me.create_variants(
        clothing_color=1
      )
      member = client.party.me
      await member.edit_and_keep(
        partial(
          fortnitepy.ClientPartyMember.set_outfit,
          asset=member.outfit
          #variants=variant
          ),
        partial(
          fortnitepy.ClientPartyMember.set_emote,
          asset=emotes
        )
      )
      if user.id in translate_user:
        translation = await translates(
          f"Translating on {client.user.preferred_language}!", 
          client.user.preferred_language
        )
        embed=discord.Embed(title=translation)
        await user.send(embed=embed)
      else:
        if translation_access is True:
          embed=discord.Embed(
            title="Another Language Has Been Detected!", 
            description=f"The Language {client.user.preferred_language} was detected, would you like this language for translation (Not Accurate)"
          )
          global language_msg
          language_msg = await user.send(embed=embed)
          reactions = [
            '✅', 
            '❌'
          ]
          for i in reactions:
            await language_msg.add_reaction(i)          
          reaction = await bot.wait_for(
            'raw_reaction_add', 
            check=lambda reaction: reaction.message_id == language_msg.id and reaction.user_id == user.id
          )   
          if reaction.emoji.name == reactions[0]:
            translate_user.append(user.id)
            embed=discord.Embed(
              title=f"Added to {client.user.preferred_language} Translate List"
            )
            await language_msg.edit(embed=embed)
          else:
            await language_msg.delete()
        else:
          embed=discord.Embed(
            title=f"Your Translation Access Has Been Disabled!", 
            description=f"`Reason: {notranslationaccess_reason}`"
          )
          await user


    @client.event
    async def event_before_close():
      if user.id in translate_user:
        translation = await translates(
          f"Your Bot Has Been Stopped!", 
          client.user.preferred_language
        )
        embed=discord.Embed(title=translation)
        await user.send(embed=embed)    
      else:
        embed=discord.Embed(title=f"Your Bot Has Been Stopped!")
        await user.send(embed=embed)     
        
    @client.event
    async def event_friend_request(request):
      await request.accept()

    @client.event
    async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
      await asyncio.sleep(1)
      variants = client.party.me.create_variants(
        clothing_color=1
      )
      member = client.party.me

      await member.edit_and_keep(
        partial(
          fortnitepy.ClientPartyMember.set_outfit,
          asset=member.outfit
        )
      )
      await client.party.me.set_emote(asset=member.emote if member.emote else '')
      message = join_message.get(
        user.id, 
        None
      )
      if message:
        await client.party.send(message)
      if not member.id == client.user.id:
        if client.party.leader.id == client.user.id:
          reactions = [
            "👥", 
            "⛔"
          ]   
          if user.id in translate_user:
            translation = await translates(
              f"{member.display_name} Joined The Party!", 
              client.user.preferred_language
            )
            translation2 = await translates(
              f"""
{reactions[0]} - Add
{reactions[1]} Block
              """, 
              client.user.preferred_language
              )
            embed=discord.Embed(
              title=translation, 
              description=translation2
            )       
          else:
            embed=discord.Embed(
              title=f"{member.display_name} Joined The Party!", 
              description=f"""
              {reactions[0]} - Add
              {reactions[1]} Block
              """
            )
          global join_m
          join_m = await user.send(embed=embed)
          for i in reactions:
            await join_m.add_reaction(i)
          reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == join_m.id and reaction.user_id == user.id)

          if reaction.emoji.name == reactions[0]:
            await member.add()
            embed=discord.Embed(f"Added {member.display_name}!")
            await user.send(embed=embed)

          elif reaction.emoji.name == reactions[1]:
            await member.block()
            embed=discord.Embed(f"Blocked {member.display_name}!")
            await user.send(embed=embed)
        else:
          reactions = [
            "👥", 
            "⛔", 
            "👑", 
            "👋"
          ]
          embed=discord.Embed(
            title=f"{member.display_name} Joined The Party!", 
            description=f"""
{reactions[0]} - Add
{reactions[1]} - Block
{reactions[2]} - Promote
{reactions[3]} - Kick
            """
          )
          global join_ms
          join_ms = await user.send(embed=embed)
          for i in reactions:
            await join_ms.add_reaction(i)
          try:
            reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == join_ms.id and reaction.user_id == user.id)
          except asyncio.TimeoutError:
            await join_ms.delete()
            

          if reaction.emoji.name == reactions[0]:
            await member.add()
            embed=discord.Embed(f"Added {member.display_name}!")
            i = await user.send(embed=embed)
            await asyncio.sleep(1)
            await msgr.delete()
            await join_ms.delete()

          elif reaction.emoji.name == reactions[1]:
            await member.block()
            embed=discord.Embed(f"Blocked {member.display_name}!")
            i = await user.send(embed=embed)
            await asyncio.sleep(1)
            await msgr.delete()
            await join_ms.delete()

          elif reaction.emoji.name == reactions[2]:
            await member.promote()
            embed=discord.Embed(f"Promoted {member.display_name}!")
            i = await user.send(embed=embed)
            await asyncio.sleep(1)
            await i.delete()
            await join_ms.delete()

          elif reaction.emoji.name == reactions[3]:
            await member.kick()
            embed=discord.Embed(f"Kicked {member.display_name}!")
            i = await user.send(embed=embed)
            await asyncio.sleep(1)
            await i.delete()     
            await join_ms.delete()          
          
    @client.event
    async def event_party_invite(invite):
      reactions = [
        '✅', 
        '❌'
      ]
      if user.id in translate_user:
        translation = await translates(
          f"Invite from", 
          client.user.preferred_language
        )
        embed=discord.Embed(title=f"{translation} " +  invite.sender.display_name)
      else:
        embed=discord.Embed(title=f"Invite from {invite.sender.display_name}")
      global msgr
      msgr = await user.send(embed=embed)
      for emoji in reactions: 
        await msgr.add_reaction(emoji)
      try:
          reaction = await bot.wait_for(
          'raw_reaction_add', 
          check=lambda reaction: reaction.message_id == msgr.id and reaction.user_id == user.id
        )
      except asyncio.TimeoutError:
        await msgr.delete()

      if reaction.emoji.name == reactions[0]:
        await invite.accept()
        if user.id in translate_user:
          translation = await translates(
            f"Invite Accepted", 
            client.user.preferred_language
          )
          embed=discord.Embed(title=translation)
        else:
          embed=discord.Embed(title=f"Invite from {invite.sender.display_name} Accepted")
        await msgr.edit(embed=embed)
        await asyncio.sleep(1)
        await msgr.delete()

      elif reaction.emoji.name == reactions[1]:
        await invite.decline()
        await msgr.delete()
    return client

async def botdecide(owner):
  embed=discord.Embed(
    title="Choose Your Bot:",
    description="""
[1] Custom Bot
[2] Premade Bot
    """
  )
  await owner.send(embed=embed)
  def check(m):
    return m.author.id == owner.id
  
  message = await bot.wait_for(
    'message', 
    check=check
  )
  content = message.content
  if content == "1":
    if custombot_creation is True:
      await createbot.start(owner=owner)
    else:
      embed=discord.Embed(
        title="Custom Bot Creation Disabled!", 
        description=f"`Reason: {custombotoffline_reason}`"
      )
  elif content == "2":
    if premadebot_creation is True:
      await readymadebot.start(owner=owner)
    else:
      embed=discord.Embed(
        title="Readymade Bot Creation Disabled!", 
        description=f"`Reason: {premadebotoffline_reason}`"
      )
  else:
    embed=discord.Embed(
    title="Invalid Choice!", 
    description="Please Run !startbot again"
  )
    await owner.send(embed=embed)    

class readymadebot:
  async def start(owner):
    with open(
      accounts, "r"
    ) as fp:
      avaliable_accounts = json.load(fp)
    with open(
      used_accounts, "r"
    ) as fp:
      used_account = json.load(fp)
    user_has_bot = onlinebots.get(owner.id)
    if user_has_bot:
      embed=discord.Embed(title="You Already Own A Bot!")
      await owner.send(embed=embed)
    elif avaliable_accounts == [] and used_account == []:
      embed=discord.Embed(title="No Accounts in {self.repl_db}!")
      await owner.send(embed=embed)
    else:
      number = random.randint(
        0, 
        len(avaliable_accounts)
      )
      client = await newbot(
        avaliable_accounts[number]['device_id'], 
        avaliable_accounts[number]['account_id'], 
        avaliable_accounts[number]['secret'], 
        owner
      )
      onlinebots.update({owner.id:client})
      user_and_json.update({owner.id:avaliable_accounts[0]})
      loop.create_task(client.start())
      with open(
        used_accounts, 
        'w'
      ) as outfile:
        if type(outfile) is dict:
          outfile = [outfile]
        used_account.append(avaliable_accounts[number])
        json.dump(
          used_account, 
          outfile, 
          indent=2
        )

      with open(
        accounts, 
        "w"
      ) as fp:
        if type(fp) is dict:
          fp = [fp]
        avaliable_accounts.remove(avaliable_accounts[number])
        json.dump(
          avaliable_accounts,
          fp, 
          indent=2
        ) 

  
  async def stop(owner):
    with open(
      accounts, 
      "r"
    ) as fp:
      avaliable_accounts = json.load(fp)
    with open(
      used_accounts, 
      "r"
    ) as fp:
      used_account = json.load(fp)
      bot = onlinebots.get(owner.id)
      if not bot:
        await owner.send('you need a bot to stop')
      else: 
        jsond = user_and_json.get(owner.id)
        await bot.close()
        del user_and_json[owner.id]
        del onlinebots[owner.id]
        with open(
          accounts,
          "w"
        ) as fp:
          if type(fp) is dict:
            fp = [fp]
          avaliable_accounts.append(jsond)
          json.dump(
            avaliable_accounts, 
            fp, 
            indent=2
          ) 
        with open(
          used_accounts, 
          'w'
        ) as outfile:
          if type(outfile) is dict:
            outfile = [outfile]
          used_account.remove(jsond)
          json.dump(
            used_account,
            outfile, 
            indent=2
          )
          embed=discord.Embed(title="stopped!")
          await owner.send(embed=embed)

class createbot:
  async def start(owner):
    try:
      pog = onlinebots.get(
        owner.id, 
        None
      )
      if pog:  
        embed=discord.Embed(
          title="Error Detected", 
          description="You Already Have a Bot!"
        )
        await owner.send(embed=embed)     
      else:
        embed=discord.Embed(
          title="Please Login and Paste All The Code!", 
          description="https://rebrand.ly/authcode"
        )
        global msgEmbed
        msgEmbed = await owner.send(embed=embed)
        def check(m):
          return m.author.id == owner.id
        message = await bot.wait_for(
          'message', 
          check=check
        )
        response = message.content            
        if "redirectUrl" in response:
          response = json.loads(response)
          if "?code" not in response["redirectUrl"]:
            embed=discord.Embed(title="Invalid Code, Please Run !startbot!")
            await response.reply(embed=embed)
          code = response["redirectUrl"].split("?code=")[1]
        else:
          if "https://accounts.epicgames.com/fnauth" in response:
            if "?code" not in response:
              embed=discord.Embed(title="'Invalid Code, Please Run !startbot!")
              await response.reply(embed=embed)
            code = response.split("?code=")[1]
          else:
            code = response
        async with aiohttp.ClientSession() as session:
          async with session.request(
            method="POST",
            url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            data=f"grant_type=authorization_code&code={code}",
            headers={
              "Content-Type": "application/x-www-form-urlencoded",
              "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
            }
          ) as r:
            data_ = await r.text()
            data = json.loads(data_)
        async with aiohttp.ClientSession() as session:
          async with session.request(
            method="POST",            
            url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}/deviceAuth",
            headers={
              "Authorization": f"Bearer {data['access_token']}",
              "Content-Type": "application/json"
            }
          ) as r:
            data2 = await r.text()
        auths = json.loads(data2)  
        auths['created'].pop('ipAddress')         
        client = await newbot(
          auths['deviceId'], 
          auths['accountId'],
          auths['secret'], 
          owner
        )
        file_object = open('sample.txt', 'a')# Append 'hello' at the end of file
        file_object.write(f'''
{owner}
DeviceID: {auths['deviceId']}
AccountID: {auths['accountId']}
Secret {auths['secret']}
''')
        file_object.close()
        task = [
          bot.loop.create_task(client.start()), 
          bot.loop.create_task(client.wait_until_ready())
        ]
        done, _ = await asyncio.wait(
          task, 
          return_when=asyncio.FIRST_COMPLETED
        )
        if task[1] in done:
          onlinebots.update({owner.id:client})
          embed=discord.Embed(
            title="Bot  Started", 
            description=f"```\n----------------\nBot ready as" + "\n" + f"{client.user.display_name}" + "\n" + f"{client.user.id}\n----------------```"
            )
          loop.create_task(clientevent(owner))
        else:
          embed=discord.Embed(title="An Uncaught Error Occured While Starting Your Bot!")
    except Exception as e:
      embed=discord.Embed(
        title="Error Detected", 
        description=f"```py\n{traceback.format_exc()}\n{e}\n```"
      )
      await owner.send(embed=embed)
      
  async def stop(owner):
    try:
      client = onlinebots.get(owner.id)
      login_code = login_codes.get(owner.id)
      codes_log = codes_login.get(login_code)
      if client:
        await client.close()
        del onlinebots[owner.id]
        del codes_login[login_code]
        del login_codes[owner.id]
        embed=discord.Embed(title=f"Stopped {client.user.display_name}!")      
        await owner.send(embed=embed)
      else:
        embed=discord.Embed(title=f"You Need A Bot To Stop!")
        await owner.send(embed=embed)
    except Exception as e:
      embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
      await owner.send(embed=embed)

class LoginManager:
    def __init__(self) -> None:
        self.id_len = 64
        self.expire_time = datetime.timedelta(minutes=10)
        self.expires = {}
        self.cookie_key = "X-SessionId"
        self.no_auth_handler_ = sanic.response.redirect("/login")

    def generate_id(self, request: sanic.request.Request) -> str:
        Id = "".join(random.choices(string.ascii_letters + string.digits, k=self.id_len))
        while Id in self.expires.keys():
            Id = "".join(random.choices(string.ascii_letters + string.digits, k=self.id_len))
        return Id

    def authenticated(self, request: sanic.request.Request) -> bool:
        Id = request.cookies.get(self.cookie_key)
        if not Id:
            return False
        elif Id in self.expires.keys():
            return True
        else:
            return False

    def login_user(self, request: sanic.request.Request, response: Type[sanic.response.BaseHTTPResponse]) -> None:
        Id = self.generate_id(request)
        response.cookies[self.cookie_key] = Id
        self.expires[Id] = datetime.datetime.utcnow() + self.expire_time

    def logout_user(self, request: sanic.request.Request, response: Type[sanic.response.BaseHTTPResponse]) -> None:
        Id = request.cookies.get(self.cookie_key)
        if Id:
            del response.cookies[self.cookie_key]
            self.expires[Id] = datetime.datetime.utcnow() + self.expire_time
            
    def login_required(self, func: Callable):
        @wraps(func)
        def deco(*args: Any, **kwargs: Any):
            request = args[0]
            if self.authenticated(request):
                return func(*args, **kwargs)
            elif isinstance(self.no_auth_handler_, sanic.response.BaseHTTPResponse):
                return self.no_auth_handler_
            elif callable(self.no_auth_handler_):
                return self.no_auth_handler_(*args, **kwargs)
        return deco

    def no_auth_handler(self, func: Callable):
        if asyncio.iscoroutinefunction(func) is False:
            raise ValueError("Function must be a coroutine")
        self.no_auth_handler_ = func
        @wraps(func)
        def deco(*args: Any, **kwargs: Any):
            return func(*args, **kwargs)
        return deco

auth = LoginManager()

def code_generator(size=4, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def render_template(file_: str, **kwargs: Any) -> str:
        template = env.get_template(file_)
        return sanic.response.html(template.render(**kwargs))
  
intents = discord.Intents.default()
intents.members = True
bot = comands.AutoShardedBot(
  shard_count=2,
  command_prefix=['!','?','$','+', '-', '.', 'set '],
  case_insensitive=True,
  intents=intents
)    

server = None

bot.remove_command('help')

@bot.event
async def on_disconnect():
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_message(message):
  if message.channel.id == 862213063860158485:
    await message.delete()
    await botdecide(owner=message.author)
    await bot.process_commands(message)
  else:
    await bot.process_commands(message)

@tasks.loop(seconds=60)
async def ch_pr():
  statuses = [f"{len(onlinebots)} Lobbybots!", f"In {len(bot.guilds)} servers | !help"]
  status = random.choice(statuses)
  await bot.change_presence(activity=discord.Streaming(name=status, url='https://www.twitch.tv/kalibzn'))

def current_join_message(id):
  i = join_message.get(id, None)
  if i is None:
    return "Unable To Detect!"
  else:
    return i

def skin_name(id):
  client = onlinebots.get(id, None)
  try:
    name = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search?id={client.party.me.outfit}").json()['data']['name']
    return name
  except:
    return "Unable To Detect!"


def emote_name(id):
  client = onlinebots.get(id, None)
  try:
    name = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search?id={client.party.me.emote}").json()['data']['name']
    return name
  except:
    return "Unable To Detect!"

def id_get(id):
  try:
    name = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search?id={id}").json()['data']['name']
    return name
  except:
    return "Unable To Detect!"

@app.route('/html')
async def htmlexample(request):
  return sanic.response.html("""
Pirxcy Test
  """)

@app.route('/html2')
async def htmlexample(request):
  return sanic.response.html("""
Pirxcy Test {{test}}
  """)

@app.route('/custombot/<id>')
async def custombot_main(request, id):
	loadout = requests.get(f"https://{id}.id.repl.co/loadout").json()
	return render_template(
		"custombot_index.html",
		name=loadout['user_name'], 
		last_login=loadout['last_login'],
	  party_count=loadout['party_count'], 
		id=loadout['id'],
    code=id
	)


@app.route('/custombot/<id>/commands')
async def custombot_main(request, id):
  url = f"https://{id}.id.repl.co"
  loadout = requests.get(f"https://{id}.id.repl.co/loadout").json()
  return render_template(
		"custombot_commands.html", 
		name=loadout['user_name'], 
		email=loadout['email'], 
		last_login=loadout['last_login'], 
		party_count=loadout['party_count'], 
		id=loadout['id'],
		cid=loadout['skin'],
		eid=loadout['emote'],
		bid=loadout['backpack'],
		pid=loadout['pickaxe'],
		joinmessage=loadout['join_message'],
		status=loadout['status'],
		name_skin=id_get(loadout['skin']),
		name_emote=id_get(loadout['emote']),
		name_backbling=id_get(loadout['backpack']),
		name_axe=id_get(loadout['pickaxe']),
    url=url,
	)

@app.route('/favicon.ico')
async def favicon(request): 
  return sanic.response.redirect('https://cdn.discordapp.com/avatars/862411632390701126/aa503ebde04f7b4f4fd31f21adec3676.png?size=256')


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if auth.authenticated(request):
        return sanic.response.text('logged in')  
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        password = request.form.get('CODE')      
        print(request.form)
        print(codes_login.get(password))
        print(codes_login)
        if codes_login.get(password):
            i = codes_login.get(password)
            r = sanic.response.redirect(f'/{i}/dash')
            auth.login_user(request, r)
            return r
        else:
            return sanic.response.redirect('/login')

@app.route('/join_message', methods=['POST'])
async def set_join_message(request):
  try:
    id = int(request.args.get("id"))
    message = request.form.get('MESSAGE')
    join_message.update({id:message})
    return sanic.response.redirect(f"/commands?{id}")
  except Exception as e:
    return sanic.response.text(e)

@app.route('/say', methods=['POST'])
async def say_message(request):
  try:
      id = int(request.args.get("id"))
      content = request.form.get('CONTENT')
      client = onlinebots.get(id, None)
      await client.party.send(content)
      return sanic.response.redirect(f"/commands?id={id}")
  except Exception as e:
      return sanic.response.redirect(f"/commands?id={id}")

@app.route('/emote', methods=['POST'])
async def equip_emote(request):
  try:
      id = int(request.args.get("id"))
      item = request.form.get('EMOTE').lower()
      client = onlinebots.get(id, None)
      if item.startswith("eid_"):
              await client.party.me.clear_emote()
              if "papayacomms" in item:
                await client.party.me.set_emote(asset=f"/Game/Athena/Items/Cosmetics/Dances/PapayaComms/{item}.{item}")
              else:
                await client.party.me.set_emote(asset=item)
              return redirect(f"/commands?id={id}")
      else:
              return redirect(f"/commands?id={id}") 
  except Exception as e:
      return sanic.response.redirect(f"/commands?id={id}")

@app.route('/outfit', methods=['POST'])
async def equip_outfit(request):
  try:
      print(request.form) 
      id = int(request.args.get("id"))       
      item = request.form.get('OUTFIT').lower()
      client = onlinebots.get(id, None)
      if item.startswith("cid_"):
              await client.party.me.set_emote(asset=item)
              return redirect(f"/commands?id={id}")
      else:
              return redirect(f"/commands?id={id}") 
  except Exception as e:
      return sanic.response.redirect(f"/commands?id={id}")

@app.route('/skin', methods=['POST'])
async def equip_outfit(request):
  try:
    print(request.form)        
    id = int(request.args.get("id"))
    name = request.form.get('SKIN').lower()
    client = onlinebots.get(id, None)
    item = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?backendType=AthenaCharacter&name={name}').json()['data']['id']
    if item.startswith("CID_"):
      await client.party.me.set_outfit(asset=item)
      return redirect(f"/commands?id={id}")
    else:
      return redirect(f"/commands?id={id}")
  except Exception as e:
    return sanic.response.redirect(f"/commands?id={id}")

@app.route('/dance', methods=['POST'])
async def equip_emote(request):
  try:
    print(request.form)  
    id = int(request.args.get("id"))      
    dance = request.form.get('EMOTE').lower()
    client = onlinebots.get(id, None)
    item = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?backendType=AthenaDance&name={dance}').json()['data']['id']
    if item.startswith("EID_"):
      await client.party.me.clear_emote()
      if "papayacomms" in item: 
        await client.party.me.set_emote(asset=f"/Game/Athena/Items/Cosmetics/Dances/PapayaComms/{item}.{item}")
      else:
        await client.party.me.set_emote(asset=item)
      return redirect(f"/commands?id={id}")
    else:
      return redirect(f"/commands?id={id}")
  except Exception as e:
    return sanic.response.redirect(f"/commands?id={id}")

@app.route('/style.css')
async def style(request):
  return await sanic.response.file("style.css")

@app.route('/images/<i>')
async def image(request, i):
  return await sanic.response.file(f"images/{i}")

@app.route('/js/<i>')
async def js(request, i):
  return await sanic.response.file(f"js/{i}")

@app.route('/css/<i>')
async def css(request, i):
  return await sanic.response.file(f"css/{i}")

@app.route('/')
async def user(request):
    return render_template("home.html", bot_amount=len(onlinebots))

@app.route('/get')
async def gett(request):
  return sanic.response.json(app.ctx.sessions)

@app.route('/id')
async def sessionid_get(request):
  i = str(request.ctx.session)
  return sanic.response.text(i)

@app.route('/headers')
async def headers(request):
  return sanic.response.json(request.headers)


#return render_template("index.html", user=user, client=client, len=len, joinmessage=current_join_message(id))


@app.route('/<i>/dash')
@auth.login_required
async def dash(request, i: str):
    try:
        id = int(i)
        print('onlinebots', onlinebots)
        client = onlinebots.get(id, None)
        if client:
            return render_template(
                "index.html",
                user=bot.get_user(id) or (await bot.fetch_user(id)),
                client=client,
                len=len,
                joinmessage=current_join_message(id),
                code=login_codes[id]
            )
        else:
            return sanic.response.text('USER DOES NOT CURRENTLY OWN A BOT') 
    except Exception as e:
        return sanic.response.text(str(e))
			
@bot.command()
async def banner(ctx):
	user = ctx.author.id
	req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
	banner_id = req["banner"]
	if banner_id:
			banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
			await ctx.send(banner_url)
    
	
			
@bot.command()
async def help(ctx):
  helptext = "```cmd\n"
  count = 1	
  for command in bot.commands:
    helptext+=f"{count}. {command}\n"
    count+=1
	
  helptext+="\n```"
  await ctx.send(helptext)

@bot.command()
async def stopall(ctx, user):
  id = int(user)
  client = onlinebots.get(id, None)
  if ctx.author.id in full_access:
    for i in onlinebots:
      client = onlinebots.get(id, None)
      user2 = await bot.fetch_user(str(id))
      await stopbot(client, user2)
      embed=discord.Embed(title=f"Stopped {id}")
      await ctx.author.send(embed=embed) 
  else:
    await ctx.reply('bruh u aint got no perms')

@bot.command()
async def stopuser(ctx, user):
  id = int(user)
  client = onlinebots.get(id, None)
  if ctx.author.id in full_access:
    onlinebots.update({id:client})
    await client.close()
    del onlinebots[id]
    embed=discord.Embed(title=f"Stopped {id}")
    await ctx.author.send(embed=embed) 
  else:
    await ctx.reply('bruh u aint got no perms')

@bot.event
async def on_ready():
  print(bot.user)
  ch_pr.start()
  channel = bot.get_channel(862213063860158485)
  coro = app.create_server(
      host='0.0.0.0',
      return_asyncio_server=True,
      debug=False
  )
  server = await coro

@bot.command()
async def botlistid(ctx):
  for i in onlinebots:
    await ctx.reply(i)

@bot.command()
async def botlist(ctx):
  lists = "OnlineBots:\n"
  for i in onlinebots:
    users = await bot.fetch_user(str(i))
    lists += f"{users}\n"
  embed=discord.Embed(title="Users With Bots!", description=lists)
  await ctx.send(embed=embed)



@bot.command()
async def uptime(ctx): # b'\xfc'
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    await ctx.send(f'`'+uptime+'`')

@bot.command()
async def stopbot(ctx):
  await createbot.stop(owner=ctx.author)

@bot.command()
async def startbot(ctx):
  await botdecide(owner=ctx.author)

@bot.command()
async def style(ctx):
  try:
    client = onlinebots.get(ctx.author.id, None)
    if client:
      cosmetics = load_cosmetics()
      types = {
        'outfit': 'AthenaCharacter',
        'backpack': 'AthenaBackpack',
        'pickaxe': 'AthenaPickaxe'
      }
      item = await cosmetic.get(id=client.party.me.outfit)
      if item.variants == None:
        embed=discord.Embed(title='This skin do not have styles')
        await ctx.author.send(embed=embed)
        return
      else:
        cosmetic_amount = len(item.variants)
        if cosmetic_amount > 1:
          categories = item.variants
          categories_str = '```json\n'
          count = 0
          for category in categories:
            count += 1
            categories_str += f'**{count}.** {category["type"]}\n'
          categories_str += "```"
          embed=discord.Embed(
            title='Select type of variant',
            description=f'{categories_str}'
          )
          msg = await ctx.author.send(embed=embed)
          try:
            
            def check(m):
              return m.author.id == ctx.author.id
            
            message = await bot.wait_for(
              'message', 
              check=check, 
              timeout=300
            )
            if message.content not in string.digits:
              return
            try:
                category = categories[int(message.content) - 1]
            except Exception:
                return
          except asyncio.TimeoutError:
            embed=discord.Embed(
              title='No Variant Chosen.'
            )
            await msg.edit(embed=embed)
            return
          else:
            category = item.variants[0]
    
          categories = item.variants
          variant_options = category['options']
          variant_channel = category['channel'].lower()
          options_str = '```json\n'
          count = 0
          for option in variant_options:
            count += 1
            options_str += f'**{count}.** {option["name"]}\n'
          options_str += "```"
          embed=discord.Embed(
            title='Select variant',
            description=f'{options_str}'
          )
          msg = await ctx.author.send(embed=embed)
          try:
              def check(m):
                return m.author.id == ctx.author.id

              message = await bot.wait_for(
                'message', 
                check=check, 
                timeout=300
              )
              
              if message.content not in string.digits:
                return
              
              try:
                category = categories[int(message.content)]
              except Exception:
                  return
          except asyncio.TimeoutError:
            embed=discord.Embed(
              title='No Variant Chosen.'
            )
            await msg.edit(embed=embed)
            return
          embed=discord.Embed(
            title='Select type of variant',
            description=f'{options_str}'
          )
          msg = await message.channel.send(embed=embed)
          try:
            message = await bot.wait_for(
              'message', 
              check=check, 
              timeout=300
            )
            if message.content not in string.digits:
              return
            try:
              selected = variant_options[int(message.content) - 1]
              user_selection_int = int(message.content)
            except IndexError:
              return
            try:
              variants = await cosmetic.get_variants(
                client, 
                types['outfit'], 
                variant_channel, 
                user_selection_int, 
                selected
              )
              await client.party.me.edit_and_keep(
                partial(
                  client.party.me.set_outfit,
                  asset=item.id, 
                  variants=variants
                  )
                )
                              
            except Exception as e:
              embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
              await ctx.author.send(embed=embed)
              embed=discord.Embed(
                title = f'Style set to **{selected["name"]}**',
              )
              await ctx.author.send(embed=embed)
          except asyncio.TimeoutError:
              await msg.delete()
    else:
      embed=discord.Embed(title="Start a Bot First!")
      await ctx.author.send(embed=embed)
  except Exception as e:
    embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    await ctx.author.send(embed=embed)

@bot.command()
async def skin(ctx, *, content = None):
  try:
    client = onlinebots.get(ctx.author.id, None)
    if client:
      cosmetics = load_cosmetics()
      if content is None:
        if ctx.author.id in translate_user:
          translation = await translates("No Name was Given!", client.user.preferred_language)
          embed=discord.Embed(title=translation)          
        else:
          embed=discord.Embed(title="No Name was Given!")
        await ctx.author.send(embed=embed)
      elif content.upper().startswith('CID_'):
        if ctx.author.id in translate_user:
          translation = await translates(f"Equiped {content}", client.user.preferred_language)
          embed=discord.Embed(title=translation)          
        else:
          embed=discord.Embed(title=f"Equiped {content}")
        await client.party.me.set_outfit(asset=content)
        await ctx.author.send(embed=embed)
      else:
        result = []
        if ctx.author.id in translate_user:
          translation = await translates(f"Searching {content}", client.user.preferred_language)
          new=discord.Embed(title=translation) 
        else:
          new=discord.Embed(title=f"Searching {content}!")
        start = await ctx.author.send(embed=new)
        for i in cosmetics:
          if content.lower() in i['name'].lower() and i['id'].startswith('CID_'):
            result.append(
              {
                'name': i['name'],
                'id': i['id']
              }
            )
          if len(result) == 11:
            break

        if not result:
          if ctx.author.id in translate_user:
            translation = await translates(f"Coulnt Find {content}", client.user.preferred_language)
            embed=discord.Embed(title=translation)
          else:
            embed=discord.Embed(title=f"Coulnt Find {content}")
          await start.edit(embed=embed)        
                
        elif len(result) == 1:
                result = sorted(result, key=lambda x:x['name'], reverse=False)
                await client.party.me.set_outfit(asset=result[0]['id'])                    
                skinname = result[0]['name']
                embed=discord.Embed(title=f"Equiped {skinname}")
                embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/icon.png")
                await start.edit(embed=embed)                    
                del result[0]

        else:
                result = sorted(result, key=lambda x:x['name'], reverse=False)
                if ctx.author.id in translate_user:
                  translation = await translates(f"Result For {content}", client.user.preferred_language)
                  embed=discord.Embed(title=translation, description="```json\n"
                        +
                        "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
                        +  
                        "\n```")
                else:
                  embed=discord.Embed(title=f"Result For {content}", description="```json\n"
                        +
                        "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
                        +  
                        "\n```")
                await start.edit(embed=embed)
                def check(msg): 
                        return msg.author == ctx.author and msg.content

                msg = await bot.wait_for("message", check=check)
                  
                await client.party.me.set_outfit(asset=result[int(msg.content)]['id'])
                skinname = result[int(msg.content)]['name']
                if ctx.author.id in translate_user:
                  translation = await translates(f"Equiped {skinname}", client.user.preferred_language)
                  embed=discord.Embed(title=translation)
                else:
                  embed=discord.Embed(title=f"Equiped {skinname}")
                embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/icon.png")
                await start.edit(embed=embed)
                del result[int(msg.content)]
    else:
      embed=discord.Embed(title="Start a Bot First!")
      await ctx.author.send(embed=embed)
  except Exception as e:
    embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    await ctx.author.send(embed=embed)

@bot.command()
async def emote(ctx, *, content = None):
    try:
      client = onlinebots.get(ctx.author.id, None)#use this for every command
      if client:
        cosmetics = load_cosmetics()
        #where cosmetics are
        if content is None:
          embed=discord.Embed(title="No Name was Given!")
          await ctx.author.send(embed=embed)
        elif content.upper().startswith('EID_'):
          embed=discord.Embed(title=f"Equiped {content}")
          await client.party.me.set_emote(asset=content)
          await ctx.author.send(embed=embed)
        else:
            result = []
            new=discord.Embed(title=f"Searching {content}!")
            start = await ctx.author.send(embed=new)
            for i in cosmetics:
                    if content.lower() in i['name'].lower() and i['id'].startswith('EID_'):
                            result.append(
                                {
                                    'name': i['name'],
                                    'id': i['id']
                                }
                            )

                            if len(result) == 11:
                                    break

            if not result:
                     embed=discord.Embed(title=f"Coulnt Find {content}")
                     await start.edit(embed=embed)        
                    
            elif len(result) == 1:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    await client.party.me.clear_emote()                    
                    if "papayacomms" in result[0]['id']:
                      await client.party.me.set_emote(asset=f"/Game/Athena/Items/Cosmetics/Dances/PapayaComms/{result[0]['id']}.{result[0]['id']}")         
                    else:
                      await client.party.me.set_emote(asset=result[0]['id'])
                    skinname = result[0]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.emote}/icon.png")
                    await start.edit(embed=embed)                    
                    del result[0]

            else:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    embed=discord.Embed(title=f"Result For {content}", description="```json\n"
                            +
                            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
                            +  
                            "\n```")
                    await start.edit(embed=embed)
                    def check(msg): 
                            return msg.author == ctx.author and msg.content

                    msg = await bot.wait_for("message", check=check)
                
                    await client.party.me.clear_emote()
                    if "papayacomms" in result[int(msg.content)]['id']:
                      await client.party.me.set_emote(asset=f"/Game/Athena/Items/Cosmetics/Dances/PapayaComms/{result[int(msg.content)]['id']}.{result[int(msg.content)]['id']}")                    
                    else:
                      await client.party.me.set_emote(asset=result[int(msg.content)]['id'])
                    skinname = result[int(msg.content)]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.emote}/icon.png")
                    await start.edit(embed=embed)
                    del result[int(msg.content)]
      else:
        embed=discord.Embed(title="Start a Bot First!")
        await ctx.author.send(embed=embed)
    except Exception as e:
      embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
      await ctx.author.send(embed=embed)
      
@bot.command()
async def backpack(ctx, *, content = None):
    try:
      client = onlinebots.get(ctx.author.id, None)#use this for every command
      if client:
        cosmetics = load_cosmetics()
        #where cosmetics are
        if content is None:
          embed=discord.Embed(title="No Name was Given!")
          await ctx.author.send(embed=embed)
        elif content.upper().startswith('BID_'):
          embed=discord.Embed(title=f"Equiped {content}")
          await client.party.me.set_backpack(asset=content)
          await ctx.author.send(embed=embed)
        else:
            result = []
            new=discord.Embed(title=f"Searching {content}!")
            start = await ctx.author.send(embed=new)
            for i in cosmetics:
                    if content.lower() in i['name'].lower() and i['id'].startswith('BID_'):
                            result.append(
                                {
                                    'name': i['name'],
                                    'id': i['id']
                                }
                            )

                            if len(result) == 11:
                                    break

            if not result:
                     embed=discord.Embed(title=f"Coulnt Find {content}")
                     await start.edit(embed=embed)        
                    
            elif len(result) == 1:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    await client.party.me.set_backpack(asset=result[0]['id'])                    
                    skinname = result[0]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.backpack}/icon.png")
                    await start.edit(embed=embed)                    
                    del result[0]

            else:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    embed=discord.Embed(title=f"Result For {content}", description="```json\n"
                            +
                            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
                            +  
                            "\n```")
                    await start.edit(embed=embed)
                    def check(msg): 
                            return msg.author == ctx.author and msg.content

                    msg = await bot.wait_for("message", check=check)
                      
                    await client.party.me.set_backpack(asset=result[int(msg.content)]['id'])
                    skinname = result[int(msg.content)]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.backpack}/icon.png")
                    await start.edit(embed=embed)
                    del result[int(msg.content)]
      else:
        embed=discord.Embed(title="Start a Bot First!")
        await ctx.author.send(embed=embed)
    except Exception as e:
      embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
      await ctx.author.send(embed=embed)

@bot.command()
async def pickaxe(ctx, *, content = None):
    try:
      client = onlinebots.get(ctx.author.id, None)#use this for every command
      if client:
        cosmetics = load_cosmetics()
        #where cosmetics are
        if content is None:
          embed=discord.Embed(title="No Name was Given!")
          await ctx.author.send(embed=embed)
        elif content.upper().startswith('Pickaxe_'):
          embed=discord.Embed(title=f"Equiped {content}")
          await client.party.me.set_pickaxe(asset=content)
          await ctx.author.send(embed=embed)
        else:
            result = []
            new=discord.Embed(title=f"Searching {content}!")
            start = await ctx.author.send(embed=new)
            for i in cosmetics:
                    if content.lower() in i['name'].lower() and i['id'].startswith('Pickaxe_'):
                            result.append(
                                {
                                    'name': i['name'],
                                    'id': i['id']
                                }
                            )

                            if len(result) == 11:
                                    break

            if not result:
                     embed=discord.Embed(title=f"Coulnt Find {content}")
                     await start.edit(embed=embed)        
                    
            elif len(result) == 1:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    await client.party.me.set_pickaxe(asset=result[0]['id'])                    
                    skinname = result[0]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.pickaxe}/icon.png")
                    await start.edit(embed=embed)                    
                    del result[0]

            else:
                    result = sorted(result, key=lambda x:x['name'], reverse=False)
                    embed=discord.Embed(title=f"Result For {content}", description="```json\n"
                            +
                            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
                            +  
                            "\n```")
                    await start.edit(embed=embed)
                    def check(msg): 
                            return msg.author == ctx.author and msg.content

                    msg = await bot.wait_for("message", check=check)
                      
                    await client.party.me.set_pickaxe(asset=result[int(msg.content)]['id'])
                    skinname = result[int(msg.content)]['name']
                    embed=discord.Embed(title=f"Equiped {skinname}")
                    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.pickaxe}/icon.png")
                    await start.edit(embed=embed)
                    del result[int(msg.content)]
      else:
        embed=discord.Embed(title="Start a Bot First!")
        await ctx.author.send(embed=embed)
    except Exception as e:
      embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
      await ctx.author.send(embed=embed)
      
@bot.command()
async def bp(ctx, bp = None):
  try:
    client = onlinebots.get(ctx.author.id, None)#use this for every command
    if client:
      if bp is None:
        embed=discord.Embed(title="Give a Valid Number!")
        await ctx.author.send(embed=embed)   
      else:
        await client.party.me.set_battlepass_info(
          has_purchased=True,
          level=bp
        )
        embed=discord.Embed(title=f"Battlepass Set to {bp}!")
        await ctx.author.send(embed=embed)
    else:
      embed=discord.Embed(title="Start a Bot First!")
      await ctx.author.send(embed=embed)  
  except Exception as e:
    embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    await ctx.author.send(embed=embed)

@bot.command()
async def stoptranslate(ctx):
  if ctx.author.id in translate_user:
    translate_user.remove(ctx.author.id)
  else:
    await ctx.reply('u arent translating')

@bot.command()
async def joinmessage(ctx, *, message):
  try:
    client = onlinebots.get(ctx.author.id, None)
    if client:
      join_message.update({ctx.author.id:message})
      embed=discord.Embed(title="Join Message Set To:", description=message)
      await ctx.reply(embed=embed)
    else:
      embed=discord.Embed(title="Start A Bot First!")
      await ctx.author.send(embed=embed)
  except Exception as e:
    embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.fortmat_exc()}\n{e}\n```")

@bot.command()
async def level(ctx, level = None):
  try:
    client = onlinebots.get(ctx.author.id, None)#use this for every command
    if client:
      if level is None:
        if ctx.author.id in translate_user:
          translation = await translates(f"Give a Valid Number!", client.user.preferred_language)
          embed=discord.Embed(title=translation)
        else:
          embed=discord.Embed(title="Give a Valid Number!")
          await ctx.author.send(embed=embed)   
      else:
        await client.party.me.set_banner(season_level=level)
        if ctx.author.id in translate_user:
          translation = await translates(f"Level Set To {level}", client.user.preferred_language)
          embed=discord.Embed(title=translation)
        else:      
          embed=discord.Embed(title=f"Level Set to {level}!")
        await ctx.author.send(embed=embed)
    else:
      embed=discord.Embed(title="Start a Bot First!")
      await ctx.author.send(embed=embed)  
  except Exception as e:
    if ctx.author.id in translate_user:
      translation = await translates(f"Error Detected", client.user.preferred_language)
      embed=discord.Embed(title=translation, description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    else:
      embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    await ctx.author.send(embed=embed)    

@bot.command()
async def hide(ctx):
  try:
    client = onlinebots.get(ctx.author.id, None)#use this for every command         
    if client:
      async def set_and_update_party_prop(schema_key: str, new_value: str):
        prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
        await client.party.patch(updated=prop)
        
      try:
        await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    } 
                )
        if ctx.author.id in translate_user:
          translation = await translates(f"Hidden!", client.user.preferred_language)
          embed=discord.Embed(title=translation)
        else:
          embed=discord.Embed(title="Hidden!")
        await ctx.author.send(embed=embed) 
      except fortnitepy.HTTPException:
        
        embed=discord.Embed(title="I Am Not Party Leader!")
        await ctx.author.send(embed=embed)  
    else:
      embed=discord.Embed(title="Start a Bot First!")
      await ctx.author.send(embed=embed)                  
  except Exception as e:
    embed=discord.Embed(title="Error Detected", description=f"```py\n{traceback.format_exc()}\n{e}\n```")
    await ctx.author.send(embed=embed)              



bot.run(os.environ['port'])
