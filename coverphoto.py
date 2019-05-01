from PIL import Image

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
DIMENSIONS = (1568, 588)
OVERLAY_LOGOS = Image.open("logos_overlay.png")
BACKGROUND = Image.open("background.jpg")

def create_overlay(color):
    # color = ESN_COLORS.get(color, ESN_COLORS["dark blue"])
    img = Image.new(BACKGROUND.mode, DIMENSIONS, color["rgb"])
    return img

def blend_images(background, color):
    overlay = create_overlay(color)
    blended_img = Image.blend(background, overlay, 0.65)
    return blended_img

def overlay_images(background, overlay):
    background.paste(overlay, overlay)
    return background

def create_coverphoto(title, subtitle, color):
    ext = BACKGROUND.filename.split(".")[-1]
    overlay_images(blend_images(BACKGROUND, color), OVERLAY_LOGOS).save("cover_" + color["name"] + "." + ext)

def run():
    title = input("Title: ")
    subtitle = input("Subtitle: ")
    overlay_color = input("Overlay color (valid colors are cyan, magenta, green, orange and dark blue): ")
    overlay_color = str(overlay_color).lower()
    overlay_color = ESN_COLORS.get(overlay_color, ESN_COLORS["dark blue"])
    # create_coverphoto(title, subtitle, overlay_color)
    for color in ESN_COLORS.values():
        create_coverphoto("title", "subtitle", color)
run()