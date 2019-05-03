# CoverCreator
A tool to automate creation of cover photos for Facebook events. You supply the background image, and the script will do the rest. A solid color and logos will be overlayed and the title and subtitle will be positioned in the center of the image. If the background image is not the correct dimensions, it will be resized and cropped to fit.

## Requirements
[pillow](https://python-pillow.org/)

Install with PyPI: `pip install pillow`

## Usage
You need to prepare a few things in order for the script to work properly.
All files should be in the same folder as the script.

* Save your logos or other graphics as logos_overlay.png. logos_overlay.png should be exactly the correct dimensions (1568, 588). The logos and graphics should be placed exactly where you want them to be.
* `DEFAULT_BACKGROUND` should be your default background. It should be exactly the correct dimensions, but it is not required. It must be a format pillow can work with.
* `BACKGROUND` should be the background you wish to use for the cover photo. It must be a format pillow can work with.
* `TITLE_FONT` and `SUBTITLE_FONT` should be edited to the font you would like to use. You must place a copy of the font file within the same folder as the script. You should use .otf or .ttf formats.
* Offsets may be edited to your liking, I have found that these positions suits my style and fits in great with the position of the logos I use.
* Colors may be edited if you wish.

When you have prepared all of the above, you can run the script. Simply start the script and follow the instructions in the terminal. Enter the title, subtitle and the color(s) you wish and hit enter. The created images will be saved to the same folder as the script is in. They will be saved as title_color.

The resulting image will look like the following;
![resulting cover photo][cover]

[cover]: https://github.com/LaiAlexander/CoverCreator/img/cover.png "Cover photo example"