import urllib.request
import json
import io
from PIL import Image
import os


version_url = "http://ddragon.leagueoflegends.com/api/versions.json"
response = urllib.request.urlopen(version_url)
data = json.loads(response.read())
api_version = data[0]



url = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json" %api_version

response = urllib.request.urlopen(url)
data = json.loads(response.read())

# create a folder to save the images

if not os.path.exists('images'):
    os.makedirs('images')

for champion in data["data"].values():
    champ = champion["id"]

    img_url = "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(api_version, champ)
    img_data = urllib.request.urlopen(img_url).read()

    # save the image to a file in the folder
    with open(f"images/{champ}.png", "wb") as f:
        f.write(img_data)

    img = Image.open(io.BytesIO(img_data))
    img = img.resize((64, 64), Image.LANCZOS)

