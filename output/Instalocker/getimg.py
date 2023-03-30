import urllib.request
import json
import io
from PIL import Image
import os



images_dir = os.path.join(os.getcwd(), 'images')

image_files = os.listdir(images_dir)

version_url = "http://ddragon.leagueoflegends.com/api/versions.json"
response = urllib.request.urlopen(version_url)
data = json.loads(response.read())
api_version = data[0]

url = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json" % api_version

response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(type(image_files))
data_len = len(data["data"])
str_data_len = str(data_len)
if len(image_files) != len(data["data"]):
    print("New champion(s) detected!")
    for champion in data["data"].values():
        champ = champion["id"]
        champ_png = champ + ".png"
        if champ_png not in image_files:
            img_url = "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(api_version, champ)
            img_data = urllib.request.urlopen(img_url).read()
            # save the image to a file in the folder
            with open(f"images/{champ}.png", "wb") as f:
                f.write(img_data)
            print("updating image folder")
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((64, 64), Image.LANCZOS)
            print(f"Added {champ} to the images folder.!")