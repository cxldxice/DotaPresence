from PIL import Image, ImageDraw, ImageFont


def write_center(text, font, draw, area, fill):
    (w, h) = font.getsize(text)

    draw.text(((area[0]-w)/2, (area[1]-h-40)/2), text, font=font, fill=fill)


def draw(level):
    image = Image.new("RGBA", (512, 512), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("./Trajan Bold.ttf", 230)

    # draw.rounded_rectangle((0, 0, 512, 512), 256, "#d0bda5")
    draw.rounded_rectangle((0, 0, 512, 512), radius=256,
                           fill="#242424", outline="#d0bda5", width=25)
    write_center(str(level), font, draw, (512, 512), "#d9af7a")

    image.save(f"./levels/{level}.png", "PNG")


for level in range(1, 30 + 1):
    draw(level)
