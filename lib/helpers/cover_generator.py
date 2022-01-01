import os, aiohttp, aiofiles
from PIL import Image, ImageFont, ImageDraw


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.ttf", 45)
    font2 = ImageFont.truetype("etc/font2.ttf", 35)
    draw.text((27, 610), f"Title - {title}...", (255, 255, 255), font=font)
    draw.text((27, 535), f"Played by - {requested_by}", (255, 255, 255), font=font2)
    # draw.text((50, 630), f"Views: {views}", (0, 0, 0), font=font)
    # draw.text((50, 670),f"Played by: {requested_by}", (0, 0, 0), font=font)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")

