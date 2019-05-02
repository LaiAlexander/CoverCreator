from PIL import Image, ImageDraw, ImageFont

ESN_COLORS = {
    "cyan": {
        "name": "cyan",
        "rgb": (0, 174, 239) #00aeef
    },
    "magenta": {
        "name": "magenta",
        "rgb": (236, 0, 140) #ec008c
    },
    "green": {
        "name": "green",
        "rgb": (122, 193, 67) #7ac143
    },
    "orange": {
        "name": "orange",
        "rgb": (244, 123, 32) #f47b20
    },
    "dark blue": {
        "name": "dark blue",
        "rgb": (46, 49, 146) #2e3192
    }
}

def open_background_img(filename):
    background = Image.open(filename)
    if background.size[0] < DIMENSIONS[0] / 1.33 or background.size[1] < DIMENSIONS[1] / 1.33:
        print("Background resolution is low. You will get a better result if you have an image with higher resolution.")
    ratio = background.size[0] / DIMENSIONS[0]
    # Something is not right with the resizing
    new_height = int(background.size[1] * ratio)
    background = background.resize((DIMENSIONS[0], new_height), Image.ANTIALIAS)
    if background.size[1] > DIMENSIONS[1]:
        print(background.size)
        padding = (background.size[1] - DIMENSIONS[1]) / 2
        coords = (0, padding, DIMENSIONS[0], background.size[1] - padding)
        background = background.crop(coords)
        print(background.size)
    return background

DIMENSIONS = (1568, 588)
OVERLAY_LOGOS = Image.open("logos_overlay.png")
BG_NAME = "background.jpg"
BACKGROUND = open_background_img(BG_NAME)
TITLE_FONT = ImageFont.truetype("Kelson Sans Bold.otf", 90)
SUBTITLE_FONT = ImageFont.truetype("Kelson Sans Bold.otf", 50)
TITLE_V_OFFSET = -6
SUBTITLE_V_OFFSET = 90
SUBTITLE2_V_OFFSET = 152

def create_color_overlay(color):
    img = Image.new(BACKGROUND.mode, DIMENSIONS, color["rgb"])
    return img

def blend_color(background, color):
    overlay = create_color_overlay(color)
    blended_img = Image.blend(background, overlay, 0.65)
    return blended_img

def overlay_images(background, overlay):
    # TODO figure out this mess. I think it's actually most simple to just switch mode. alpha_composite requires both images to have an alpha channel
    # background = background.convert(mode="RGB")
    background.mode = "RGB" # necessary to get proper antialiasing on overlay when background is png/rgba
    background.paste(overlay, (0, 0), overlay)
    # background = Image.alpha_composite(background, overlay) # this is simpler, and works just as good
    return background

def overlay_text(background, text, font, offset):
    draw = ImageDraw.Draw(background)
    width, height = draw.textsize(text, font)
    draw.text(((background.size[0] - width) / 2, (background.size[1] - height) / 2 + offset), text, font=font)

def create_coverphoto(title, subtitle, subtitle2, color):
    ext = BG_NAME.split(".")[-1]
    if not title:
        title = "cover"
    cover = overlay_images(blend_color(BACKGROUND, color), OVERLAY_LOGOS)
    if subtitle or subtitle2:
        overlay_text(cover, title, TITLE_FONT, TITLE_V_OFFSET)
        overlay_text(cover, subtitle, SUBTITLE_FONT, SUBTITLE_V_OFFSET)
        overlay_text(cover, subtitle2, SUBTITLE_FONT, SUBTITLE2_V_OFFSET)
    else:
        overlay_text(cover, title, TITLE_FONT, TITLE_V_OFFSET + 25)
    cover.save(title + "_" + color["name"] + "." + ext)

def run():
    title = input("Title: ")
    subtitle = input("Subtitle: ")
    subtitle2 = input("Second subtitle: ")
    overlay_color = input("Overlay color (cyan, magenta, green, orange,dark blue or all): ")
    overlay_color = str(overlay_color).lower()
    if overlay_color == "all":
        for color in ESN_COLORS.values():
            create_coverphoto(title, subtitle, subtitle2, color)
        return
    overlay_color = ESN_COLORS.get(overlay_color, ESN_COLORS["dark blue"])
    create_coverphoto(title, subtitle, subtitle2, overlay_color)
    # create_coverphoto("Eventname", "Location", "Date etc", ESN_COLORS["dark blue"])

run()
