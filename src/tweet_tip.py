from twitter import *
import os
from pygments import highlight
from pygments import lexers
from pygments.style import Style
from pygments.token import Token
from pygments.formatters.img import ImageFormatter
from pygments.styles import get_style_by_name
import math
from PIL import Image, ImageDraw
from gradient_fill import create_cont
from read_tip import snip
import twitter_creds

def construct_tweet():

    get_pad = lambda j, k: math.ceil((j-k)/2)

    #generate code snippet
    code = snip("Tips50.txt")
    lexer = lexers.get_lexer_by_name('python')
    style = get_style_by_name('xcode')
    formatter = ImageFormatter(
    full=True, style="paraiso-dark", line_numbers=False, font_size=40, line_pad=7.5)


    # Highlight
    with open('temp_snip.png', 'wb') as f:
        f.write(highlight(code[1], lexer, formatter))
    
    #snippet
    code_snippet = Image.open(r"temp_snip.png").convert("RGBA")

    #create background
    colors = [(0, 144, 218), (219, 10, 91), (255, 198, 0)]
    backg = create_cont(colors, 2000, 1000, 135)
    ypad = get_pad(backg.size[1],code_snippet.size[1])
    xpad = 246

    #create combined image
    backg.paste(code_snippet, (xpad, ypad), code_snippet)
    img_to_jpg = Image.new(
        "RGB", (backg.size[0], backg.size[1]), (255, 255, 255))
    img_to_jpg.paste(backg, mask=backg.split()[3])
    img_to_jpg.save("temp_img.jpg", 'JPEG', quality=80)

    post_tip(twitter_creds.token, twitter_creds.token_secret, twitter_creds.api_key, twitter_creds.api_secret, code[0])







def post_tip(token, token_secret, consumer_key, consumer_secret, caption):

    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    with open("temp_img.jpg", "rb") as imagefile:
        imagedata = imagefile.read()
    

    params = {"media[]": imagedata, "status": caption}

    t.statuses.update_with_media(**params)

    #cleanup
    os.remove("temp_img.jpg")
    os.remove("temp_snip.png")
