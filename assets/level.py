from PIL import Image, ImageDraw, ImageFont


def write_center(text, font, draw, area, fill):
    (w, h) = font.getsize(text)

    draw.text(((area[0]-w)/2,(area[1]-h-40)/2), text, font=font, fill=fill)


def draw(level):
    image = Image.new("RGBA", (512, 512), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("./assets/Montserrat-SemiBold.ttf", 230)

    draw.rounded_rectangle((0, 0, 512, 512), 256, "#242424")
    write_center(str(level), font, draw, (512, 512), "#ffffff")

    image.save(f"./assets/levels/{level}.png", "PNG")

for level in range(1, 30+1):
    draw(level)