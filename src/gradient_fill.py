import math
from PIL import Image, ImageDraw, ImageFilter


def create_cont(colors, w, h, direction):

    #padding lambda
    get_pad = lambda j, k: math.ceil((j - k)/2)

    #standard container padding
    pad = math.ceil(w*.1)
    
    #text container measurements
    text_cont_height = math.ceil(h - (pad*1.25))
    text_cont_width = math.ceil(w - (pad*1.25))
    
    #shadow measurements
    shadow_w = math.ceil(text_cont_width+3)
    shadow_h = math.ceil(text_cont_height+3)
   
    #generate background, container, & drop-shadow
    backg = Image.new("RGBA", (w, h), color="#ffffff")
    
    text_cont = create_rounded_rectangle_mask([text_cont_width, text_cont_height], 10)
    
    text_cont_shadow = makeShadow(
        [shadow_w, shadow_h], 300, 10, [0, 0], (68, 68, 68, 0), (0, 0, 0, 100))

    #shadow padding
    shadow_w_pad = get_pad(w, text_cont_shadow.size[0])
    shadow_h_pad = get_pad(h, text_cont_shadow.size[1])

    #generate background gradient variables
    diver = get_grad_divisor([backg.size[0], backg.size[1]], direction)

    
    #generate gradient
    grad_backg = create_grad(backg, colors, diver["degree"], diver["divisor"])

    #draw text container buttons
    text_cont = draw_buttons(text_cont)

    #paste text container and drop-shadow to background gradient
    grad_backg.paste(text_cont_shadow, (shadow_w_pad, shadow_h_pad), text_cont_shadow)
    grad_backg.paste(text_cont, (get_pad(w,text_cont_width),get_pad(h, text_cont_height)), text_cont)

    return grad_backg


def get_grad_divisor(size, direction):

    #tan(theta) = slope
    deg = math.tan(math.radians(direction))

    #pre-generation of color percentages
    vals = [(deg*(x-(size[0]/2))) - (y-(size[1]/2))
            for x in range(size[0]) for y in range(size[1])]

    #find min or max (vals[x]/min or max) = % change
    diver_max = max(vals)

    diver_min = min(vals)

    diver = diver_max if math.fabs(
        diver_min) < diver_min else math.fabs(diver_min)

    return { "degree": deg, "divisor": diver }



def create_grad(im, colors, deg, div):

    pixel_data = im.load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):

            dist0 = (deg*(x-(im.size[0]/2))) - (y-(im.size[1]/2))

            div = math.fabs((deg*(0-(im.size[0]/2))) - (9-(im.size[1]/2)))

            dist = (dist0+div)/(div)


            dist_change = lambda d: d if d < 1 else d-1

            from_change = lambda z: z if dist < 1 else colors[1]

            to_change = lambda z: z if dist < 1 else colors[2]

            r, g, b = map(lambda start, end: start+end,
                          map(lambda start: start*(1-dist_change(dist)),
                              from_change(colors[0])),
                          map(lambda end: end*dist_change(dist), to_change(colors[1])))
            pixel_data[x, y] = int(r), int(g), int(b)
            
    return im


def create_rounded_rectangle_mask(size, radius, alpha=255):
    factor = 5  # Factor to increase the image size that I can later antialiaze the corners
    radius = radius * factor
    image = Image.new(
        'RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180,
                  270, fill=(47,30,46, alpha + 55))

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius,
                my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(47,30,46, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(47,30,46, alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image

def draw_buttons(im):
    size = math.floor(im.size[1]*0.04625)
    draw = ImageDraw.Draw(im)
    x_start = lambda x: size*x + (size*(x))
    x_end = lambda x: size*(x+1) + (size*(x))
    draw.ellipse([(x_start(1),size), (x_end(1),size*2)], fill="#ff605c")
    draw.ellipse([(x_start(2), size), (x_end(2), size*2)], fill="#ffbd44")
    draw.ellipse([(x_start(3), size), (x_end(3), size*2)], fill="#00ca4e")

    return im


def makeShadow(size, iterations, border, offset, backgroundColour, shadowColour):
    # image: base image to give a drop shadow
    # iterations: number of times to apply the blur filter to the shadow
    # border: border to give the image to leave space for the shadow
    # offset: offset of the shadow as [x,y]
    # backgroundCOlour: colour of the background
    # shadowColour: colour of the drop shadow

    #Calculate the size of the shadow's image
    fullWidth = size[0] + abs(offset[0]) + 2*border
    fullHeight = size[1] + abs(offset[1]) + 2*border

    #Create the shadow's image. Match the parent image's mode.
    shadow = Image.new("RGBA", (fullWidth, fullHeight), backgroundColour)

    # Place the shadow, with the required offset
    # if <0, push the rest of the image right
    shadowLeft = border + max(offset[0], 0)
    # if <0, push the rest of the image down
    shadowTop = border + max(offset[1], 0)
    #Paste in the constant colour
    shadow.paste(shadowColour,
                 [shadowLeft, shadowTop,
                  shadowLeft + size[0],
                  shadowTop + size[1]])

    # Apply the BLUR filter repeatedly
    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    # Paste the original image on top of the shadow
    # if the shadow offset was <0, push right
    imgLeft = border - min(offset[0], 0)
    # if the shadow offset was <0, push down
    imgTop = border - min(offset[1], 0)
    #shadow.paste(image, (imgLeft, imgTop))

    return shadow


