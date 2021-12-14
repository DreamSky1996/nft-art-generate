import os
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops 

SIZE = 2000

def getFileNamesInDirectory(dirName):
    path = 'images/' + dirName
    files = os.listdir(path)
    return files

backdrops = getFileNamesInDirectory("backdrop")
individuals = getFileNamesInDirectory("individual")
verticalLines = getFileNamesInDirectory("verticalLines")

def addIndividual(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (840, 1450), im2)
    return dst


def addVerticalLines(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height))
    dst.paste(im1, (0, 0))
    im2 = im2.resize((SIZE, SIZE))
    dst.paste(im2, (0, 0), im2)
    return dst


def addText(im1, color, text, left, long, parallel, xor_f = False):
    # result w, h
    WIDTH_PER_LETTER = 65
    width = len(text) * WIDTH_PER_LETTER
    gap = width
    height = SIZE if long else int(SIZE/4)

    # get text size
    font = ImageFont.truetype("Retro Gaming.ttf", 400)
    w, h = font.getsize(text)
    rh = int(h * 0.73)

    # text -> image
    num_image = Image.new("RGBA", (w, rh), color=None)
    draw = ImageDraw.Draw(num_image)
    draw.text((0, rh-h), text=text, fill=color, font=font)
    num_image = num_image.resize((width, height))

	# past 1
    num_image1 = Image.new('RGBA', (SIZE, SIZE))
    if not parallel:
        num_image1.paste(num_image, (int(SIZE/2) - int(width/2), int(SIZE/2)- int(height/2)))
    else:
        num_image1.paste(num_image, (int(SIZE/2) - width - int(gap/2), int(SIZE/2)- int(height/2)))
        num_image1.paste(num_image, (int(SIZE/2) + int(gap/2), int(SIZE/2)- int(height/2)))

    # rotate
    rotate = 45 if left else -45
    num_image1 = num_image1.rotate(rotate)

    # paste 2
    if xor_f:
        im3 = ImageChops.logical_xor(im1.convert("1"), num_image1.convert("1"))
        return im3
    else:
        im1.paste(num_image1, (0, 0), num_image1)
        return im1


def generateParcel1(individual, text):
    background_img = Image.open("images/backdrop/white.png").convert("RGBA")
    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")

    step1 = addIndividual(background_img, individual_img)
    step2 = addVerticalLines(step1, verticalLine_img)
    step3 = addText(step2, (0,0,0), text,left= True, long = True, parallel = False)
    step4 = addText(step3, (0,0,0), text,left= False, long = True, parallel = False)

    return step4

def generateParcel2(individual, text):
    background_img = Image.open("images/backdrop/white.png").convert("RGBA")
    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")

    step1 = addIndividual(background_img, individual_img)
    step2 = addVerticalLines(step1, verticalLine_img)
    step3 = addText(step2, (0,0,0), text,left= True, long = True, parallel = False)
    step4 = addText(step3, (255,255,255), text,left= False, long = False, parallel = False, xor_f=True)

    return step4

def generateParcel3( text):
    background_img = Image.open("images/backdrop/white.png").convert("RGBA")
    verticalLine_img = Image.open('images/verticalLines/black.png').convert("RGBA")

    ret = addVerticalLines(background_img, verticalLine_img)
    ret = addText(ret, (255,255,255), text,left= True, long = True, parallel = True)
    ret = addText(ret, (0,0,0), text,left= False, long = True, parallel = True)

    ret = addText(ret, (0,0,0), text,left= True, long = True, parallel = False)
    ret = addText(ret, (255,255,255), text,left= False, long = True, parallel = False)

    return ret
def generateParcel4( individual,text):
    background_img = Image.open("images/backdrop/white.png").convert("RGBA")
    individual_img = Image.open('images/individual/' + individual).convert("RGBA")
    verticalLine_img = Image.open('images/diagonallines_black.png').convert("RGBA")
    backright_img = Image.open('images/backright_white.png').convert("RGBA")
    backleft_img = Image.open('images/backleft_white.png').convert("RGBA")
    ret = addIndividual(background_img, individual_img)
    ret = addVerticalLines(ret, verticalLine_img)

    ret = addVerticalLines(ret, backright_img)
    ret = addVerticalLines(ret, backleft_img)

    ret = addText(ret, (0,0,0), text,left= True, long = True, parallel = False)
    ret = addText(ret, (0,0,0), text,left= False, long = True, parallel = False)

    return ret

def main():
    index = 0
    # generate parcel 1
    # for individual in individuals:
    #     if "black" in individual:
    #         continue
    #     result = generateParcel1(individual, "7893456")
    #     # save
    #     result.save("output/parcel1/" + str(index) + ".png", "PNG")
    #     # verbose
    #     print("Generated {}th item".format(index))
    #     # increase index
    #     index = index + 1
    
    # generate parcel 2
    # for individual in individuals:
    #     if "black" in individual:
    #         continue
    #     result = generateParcel2(individual, "7893456")
    #     # save
    #     result.save("output/parcel2/" + str(index) + ".png", "PNG")
    #     # verbose
    #     print("Generated {}th item".format(index))
    #     # increase index
    #     index = index + 1
    
    # generate parcel 3
    result = generateParcel3( "7893456")
    # save
    result.save("output/parcel3/" + str(index) + ".png", "PNG")
    # verbose
    print("Generated {}th item".format(index))
    # increase index
    index = index + 1

    # generate parcel 4
    for individual in individuals:
        if "black" in individual:
            continue
        result = generateParcel4(individual, "7893456")
        # save
        result.save("output/parcel4/" + str(index) + ".png", "PNG")
        # verbose
        print("Generated {}th item".format(index))
        # increase index
        index = index + 1
    


if __name__ == '__main__':
    main()
