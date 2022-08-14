import yaml

databasessavefile = 'config/database.yaml'
# databasessavefile = 'database.yaml'

seting = open('config/botsetting.yaml')
# a = open('botsetting.yaml')
botconfig = yaml.load(seting, Loader=yaml.FullLoader)



