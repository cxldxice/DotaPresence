import glob
from PIL import Image

size = (512, 512)


for icon in glob.glob("./assets/icons32/*.png"):
    im = Image.open(icon)
    im = im.resize(size, Image.NEAREST)

    new_path = icon.replace("32", "").lower().replace("\\", "/npc_dota_hero_")
    im.save(new_path, "PNG")

