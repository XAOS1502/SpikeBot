import discord
from discord.ext import commands
import json
import string
from .utils import launcher

info = launcher.bot()
owner = info['owner']

class Setup():
	def __init__(self,bot):
		self.bot = bot

	async def send_cmd_help(self,ctx):
		if ctx.invoked_subcommand:
			pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
			for page in pages:
			    await self.bot.send_message(ctx.message.channel, page)
		else:
		    pages = self.bot.formatter.format_help_for(ctx, ctx.command)
		    for page in pages:
		    	await self.bot.send_message(ctx.message.channel, page)

	
	def owner_only(ctx):

		def is_owner(ctx):
			return ctx.message.author.id == owner

		if is_owner(ctx):
			return True
			
		return ctx.message.author == ctx.message.server.owner

	@commands.group(pass_context=True)
	@commands.check(owner_only)
	async def config(self,ctx):
		"""Configure the bot for your server."""
		if ctx.invoked_subcommand is None:
			await self.send_cmd_help(ctx)

	@config.command(pass_context=True)
	async def set(self,ctx):
		server = ctx.message.server
		user = ctx.message.author
		channel = ctx.message.channel
		config = json.loads(open('cogs/utils/t_config.json').read())
		x = await self.bot.say('**Welcome to the interactive bot setup system**\n\n*Bot prefix:*')
		prefix = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not prefix:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(prefix)
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Mod role:*')
		mod_role = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not mod_role:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(mod_role)
		
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Admin Role:*')
		admin_role = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not admin_role:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(admin_role)
		
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Admin Channel:*')
		admin_chat = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not admin_chat:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(admin_chat)
		
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Announcement Channel:*')
		a_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not a_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(a_channel)
		
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Tournament Channel:*')
		t_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not t_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(t_channel)
		
		x = await self.bot.edit_message(x,'**Welcome to the interactive bot setup system**\n\n*Mod logs channel:*')
		m_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not m_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		await self.bot.delete_message(m_channel)
		
		
		msg = []
		mod_role = discord.utils.get(server.roles, name=mod_role.content)
		if mod_role is None:
			msg.append('Mod Role')
			x = await self.bot.edit_message(x, 'Could not find: '+', '.join(msg).strip(', '))
		else:
			mod_role = mod_role.id


		admin_role = discord.utils.get(server.roles,name=admin_role.content)
		if admin_role is None:
			msg.append('Admin Role')
			x = await self.bot.edit_message(x, 'Could not find: '+', '.join(msg).strip(', '))
		else:
			admin_role = admin_role.id


		
		config[server.id] = {

		"prefix": prefix.content.strip(),
		"mod_role": mod_role,
		"admin_role": admin_role,
		"admin_chat": admin_chat.content.strip(string.punctuation),
		"announcements": a_channel.content.strip(string.punctuation),
		"tournaments": t_channel.content.strip(string.punctuation),
		"mod_log" : m_channel.content.strip(string.punctuation)

		}

		config = json.dumps(config, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(config)
		x = await self.bot.say('**Configuration Complete.**')

	@config.command(pass_context=True)
	async def show(self,ctx):
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		config = data[server.id]

		try:

			prefix = config['prefix']

			mod_role = discord.utils.get(server.roles, id=config['mod_role'])

			admin_role = discord.utils.get(server.roles, id=config['admin_role'])

			admin_chat = self.bot.get_channel(config['admin_chat'])

			announcements = self.bot.get_channel(config['announcements'])

			if self.bot.get_channel(config['tournaments']):
				tournaments = self.bot.get_channel(config['tournaments'])
				tournaments = tournaments.mention
			else:
				tournaments = None

			mod_log = self.bot.get_channel(config['mod_log'])

			

			em = discord.Embed(color=0x00FFFFF)
			em.set_author(name='Server Configuration', icon_url=server.icon_url)
			em.set_thumbnail(url=server.icon_url)
			em.add_field(name='Mod Role',value=mod_role.mention)
			em.add_field(name='Admin Role',value=admin_role.mention)
			em.add_field(name='Admin Channel',value=admin_chat.mention)
			em.add_field(name='Announcements',value=announcements.mention)
			em.add_field(name='Tournaments',value=tournaments)
			em.add_field(name='Mod-Logs', value=mod_log.mention)
			em.set_footer(text='ID: '+server.id+' | Prefix: '+prefix)

			await self.bot.say(embed=em)
		except:
			config = json.dumps(config, indent=4, sort_keys=True)
			await self.bot.say('All channels must be mentions, roles must have exact spelling and capitalisation. If there is something down there which is null, u did something wrong. Everything should be numbers except for the prefix.\n```json\n{}```'.format(config))

	@config.command(pass_context=True)
	async def prefix(self,ctx,*, prefix : str):
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		data[server.id]['prefix'] = prefix

		data = json.dumps(data, indent=4, sort_keys=True)


		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)


		await self.bot.say('Changed server prefix to: `{}`'.format(prefix))



def setup(bot):
	bot.add_cog(Setup(bot))

