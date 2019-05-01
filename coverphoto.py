from PIL import Image

ESN_COLORS = {
    "CYAN": (0, 174, 239), #00aeef
    "MAGENTA": (236, 0, 140), #ec008c
    "GREEN": (122, 193, 67), #7ac143
    "ORANGE": (244, 123, 32), #f47b20
    "DARK BLUE": (46, 49, 146) #2e3192
}
DIMENSIONS = (1568, 588)
OVERLAY_LOGOS = Image.open("logos_overlay.png")
BACKGROUND = Image.open("background.jpg")

def create_overlay(color):
    img = Image.new(BACKGROUND.mode, DIMENSIONS, color)
    return img

def blend_images(background, color):
    overlay = create_overlay(color)
    blended_img = Image.blend(background, overlay, 0.3)
    return blended_img

def overlay_images(background, overlay):
    background.paste(overlay, overlay)
    return background

def create_coverphoto(title, subtitle, color):
    overlay_images(blend_images(BACKGROUND, color), OVERLAY_LOGOS).save("cover.png")

def run():
    title = input("Title: ")
    subtitle = input("Subtitle: ")
    overlay_color = input("Overlay color (valid colors are cyan, magenta, green, orange and dark blue): ")
    overlay_color = str(overlay_color).upper()
    overlay_color = ESN_COLORS.get(overlay_color, ESN_COLORS["DARK BLUE"])
    create_coverphoto(title, subtitle, overlay_color)
run()