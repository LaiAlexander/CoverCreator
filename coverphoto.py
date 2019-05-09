"""
A script to automate the creation of cover photos for Facebook
TODO default to an image if no image is suppplied
"""

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
    "blue": { # proper name is dark blue
        "name": "dark blue",
        "rgb": (46, 49, 146) #2e3192
    }
}
DIMENSIONS = (1568, 588)
ASPECT_RATIO = DIMENSIONS[0] / DIMENSIONS[1]
OVERLAY_LOGOS = Image.open("logos_overlay.png")
BACKGROUND = "bg.jpg"
DEFAULT_BACKGROUND = "default_background.png"
FONTS = { #Fonts to be used for overlayed text
    "title": ImageFont.truetype("Kelson Sans Bold.otf", 90),
    "subtitle": ImageFont.truetype("Kelson Sans Bold.otf", 50)
}
V_OFFFSETS = { # Vertical offsets of text to be overlayed
    "title": -6,
    "titleonly": -6 + 25, # Offset a bit more when only title
    "subtitle": 90,
    "subtitle2": 152
}

def create_color_overlay(background, color):
    img = Image.new(background.mode, DIMENSIONS, color["rgb"])
    return img

def blend_color(background, color):
    overlay = create_color_overlay(background, color)
    blended_img = Image.blend(background, overlay, 0.65)
    return blended_img

def overlay_images(background, overlay):
    # TODO figure out this mess. I think it's actually most simple to just switch mode.
    # alpha_composite requires both images to have an alpha channel
    background = background.convert(mode="RGB")
    # background.mode = "RGB" # necessary to get proper antialiasing on overlay
    # when background is png/rgba
    background.paste(overlay, (0, 0), overlay)
    # background = Image.alpha_composite(background, overlay) # this is simpler,
    # and works just as well
    return background

def overlay_text(background, text, font, offset):
    draw = ImageDraw.Draw(background)
    width, height = draw.textsize(text, font)
    draw.text(((background.size[0] - width) / 2, (background.size[1] - height) / 2 + offset),
              text, font=font)

def create_coverphoto(background, ext, title, subtitle, subtitle2, color):
    if not title:
        title = "cover"
    background = resize_background(background)
    cover = overlay_images(blend_color(background, color), OVERLAY_LOGOS)
    if subtitle or subtitle2:
        overlay_text(cover, title, FONTS["title"], V_OFFFSETS["title"])
        overlay_text(cover, subtitle, FONTS["subtitle"], V_OFFFSETS["subtitle"])
        overlay_text(cover, subtitle2, FONTS["subtitle"], V_OFFFSETS["subtitle2"])
    else:
        overlay_text(cover, title, FONTS["title"], V_OFFFSETS["titleonly"])
    cover.save(title + "_" + color["name"] + "." + ext, quality=95) # Quality only affects jpg images

def open_background_img(filename):
    try:
        background = Image.open(filename)
        ext = filename.split(".")[-1]
    except OSError:
        background = Image.open(DEFAULT_BACKGROUND)
        ext = DEFAULT_BACKGROUND.split(".")[-1]
    return background, ext

def resize_background(background):
    if background.size == DIMENSIONS:
        return background
    if background.size[0] < DIMENSIONS[0] / 1.33 or background.size[1] < DIMENSIONS[1] / 1.33:
        print("Resolution is low. "
              + "You will get a better result if you have an image with higher resolution.")
    background_aspect_ratio = background.size[0] / background.size[1]
    # TODO the following could probably be a function instead of two almost identical blocks of code
    if background_aspect_ratio <= ASPECT_RATIO: # background is taller
        print("bg aspect <= aspect ratio")
        print(background_aspect_ratio)
        resize_ratio = background.size[0] / DIMENSIONS[0]
        new_height = int(background.size[1] / resize_ratio)
        print(background.size)
        background = background.resize((DIMENSIONS[0], new_height), Image.ANTIALIAS)
        print(background.size)
        if background.size[1] > DIMENSIONS[1]:
            padding = (background.size[1] - DIMENSIONS[1]) / 2
            coords = (0, padding, DIMENSIONS[0], background.size[1] - padding)
            background = background.crop(coords)
            print(background.size)
    else: # background is wider
        print("bg aspect > aspect ratio")
        resize_ratio = background.size[1] / DIMENSIONS[1]
        new_width = int(background.size[0] / resize_ratio)
        print(background.size)
        background = background.resize((new_width, DIMENSIONS[1]), Image.ANTIALIAS)
        print(background.size)
        if background.size[0] > DIMENSIONS[0]:
            padding = (background.size[0] - DIMENSIONS[0]) / 2
            coords = (padding, 0, background.size[0] - padding, DIMENSIONS[1])
            background = background.crop(coords)
            print(background.size)
    return background

def run():
    background, ext = open_background_img(BACKGROUND)
    title = input("Title: ")
    subtitle = input("Subtitle: ")
    subtitle2 = input("Second subtitle: ")
    overlay_color = input("Overlay color (cyan, magenta, green, orange, blue or all): ")
    overlay_color = str(overlay_color).lower()
    if overlay_color == "all":
        for color in ESN_COLORS.values():
            create_coverphoto(background, ext, title, subtitle, subtitle2, color)
        return
    overlay_color = ESN_COLORS.get(overlay_color, ESN_COLORS["blue"])
    create_coverphoto(background, ext, title, subtitle, subtitle2, overlay_color)
    # create_coverphoto("Eventname", "Location", "Date etc", ESN_COLORS["blue"])

run()
