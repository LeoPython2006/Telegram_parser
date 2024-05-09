import configparser


config = configparser.ConfigParser()


# наполнение конфига
# config['DEFAULT'] = {'ServerAliveInterval': '45',
#                      'Compression': 'yes',
#                      'CompressionLevel': '9'}
# config['forge.example'] = {}
# config['forge.example']['User'] = 'hg'
# config['topsecret.server.example'] = {}
# topsecret = config['topsecret.server.example']
# topsecret['Port'] = '50022'     # mutates the parser
# topsecret['ForwardX11'] = 'no'  # same here
# config['DEFAULT']['ForwardX11'] = 'yes'

config['Telegram'] = {}
config['Telegram']['api_id'] = '23293092'
config['Telegram']['api_hash'] = 'e192f6e222a5b892d9d084bbef93ac2d'
config['Telegram']['username'] = 'tg_username'


with open('config.ini', 'w') as configfile:
  config.write(configfile)