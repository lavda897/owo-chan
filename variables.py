from database import db

col = db["selfconfig"]

STARTUP_FILE = "../std-startup.xml"
BOT_PREFIX = ('owo ','OwO ','Owo ','OWO ','oWo ')

loaded_extensions = []
post_limit = []

try:
    post_limit.append(col.find_one({"_name": "limits"}, {"_id": 0, "_name": 0}))
except:
    post_limit.append({"post_limit": 14})
    print("Failed to fetch data from database.")

over_limit = 'Limit must be less than {}'.format(post_limit[0]['post_limit'])
non_nsfw_channel = "Your can't use that command here, kids here eh"

neko_base_url = 'https://nekos.life/api/'
neko_img = '/v2/img/'
neko_possible = [
    'femdom', 'classic', 'erok', 'erofeet', 'les', 'lewdk',
    'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri', 'kuni', 'tits',
    'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo', 'lewd', 'cum',
    'spank', 'Random_hentai_gif', 'fox_girl', 'boobs', 'feet',
    'kemonomimi', 'solog', 'bj', 'yuri', 'trap', 'anal', 'blowjob',
    'holoero', 'hentai', 'futanari', 'ero', 'solo', 'pwankg', 'eron', 'erokemo']
