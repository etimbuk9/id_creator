# import cv2
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
import os
from datetime import datetime as dt
from id_card_creator.settings import BASE_DIR
from .models import Setting


def createCodes(no):
    import qrcode
    qr = qrcode.make(str(no))
    # qr.save(str(no)+'.png')
    return qr

def createCodes1(no, name):
    import qrcode
    qr = qrcode.make(str(no))
    qr.save(str(name)+'.png')


def createStaffCodes(no, year):
    import qrcode
    staff_info = 'StaffID: '+str(no)+'\n'+'Year of Entry: '+str(year)
    qr = qrcode.make(str(staff_info))
    qr.save(str(no)+'.png')


def flattenAlpha(img, alpha_value):
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 127  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(round(255*alpha_value))  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))
    # print(checked)

    img.putalpha(mask)

    return img


def createID(surname, firstname, studentID, prog, passport,level):

    setting = Setting.objects.first()

    ## Font colors
    white = (255,255,255)
    black = (0,0,0)
    theme = (230,51,48)

    ## Fonts
    font_folder = os.path.join(BASE_DIR, 'static', 'fonts')

    fnt = ImageFont.truetype(os.path.join(font_folder, 'Myriad Pro Bold.ttf'),size=125)
    smallfnt = ImageFont.truetype(os.path.join(font_folder, 'Myriad Pro Bold.ttf'),size=63)
    normalFont = ImageFont.truetype(os.path.join(font_folder, 'Myriad Pro Bold.ttf'),size=85)
    normalBackFont = ImageFont.truetype(os.path.join(font_folder, 'MYRIADPRO-REGULAR.OTF'),size=85)

    ## Front Image Creation
    img = Image.new('RGB', (1500, 2550), color = (255, 255, 255))

    
    ## Add Uni Logo
    logo = Image.open(setting.logo)
    logo = logo.resize((round(logo.size[0]*0.8), round(logo.size[1]*0.8)))
    # foreground = Image.open("test2.png")
    img.paste(logo, (750-round(logo.size[0]/2), 320), logo)

    d = ImageDraw.Draw(img)

    ##Back Logo
    back_Logo = logo.resize((logo.size[0]*5, logo.size[1]*5))
    back_Logo = flattenAlpha(back_Logo, 0.05)
    img.paste(back_Logo, (750-round(back_Logo.size[0]/2), 800), back_Logo)


    d.polygon([(0,750), (750,0),(0,0)], fill=theme)

    coords = [[(0,675), (675,0),(0,0)], [(0,600), (600,0),(0,0)],[(0,525), (525,0),(0,0)],[(0,450), (450,0),(0,0)],[(0,375), (375,0),(0,0)]]
    coords1 = [[(0,641.25), (641.25,0),(0,0)],[(0,570), (570,0),(0,0)],[(0,498.75), (498.75,0),(0,0)],[(0,427.5), (427.5,0),(0,0)],[(0,356.25),(356.25,0),(0,0)]]

    level_num = int(str(level))/100

    for num in range(int(level_num)):
        d.polygon(coords[num], fill=white)
        d.polygon(coords1[num], fill=theme)

    para = textwrap.wrap(setting.name.upper() + ' ' + setting.address.upper(), width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 700, 20
    for line in para:
        w, h = d.textsize(line, font=normalFont)
        d.text(((MAX_W - w) / 2, current_h), line, font=normalFont, fill=(0,0,0))
        current_h += h + pad

    # w, h = d.textsize(setting.name.upper() + ' ' + setting.address.upper(), font=fnt)
    # d.text(((1500 - w) / 2, 700),setting.name.upper(), fill=(0, 0, 0), font=fnt)

    # w, h = d.textsize(setting.address.upper(), font=fnt)
    # d.text(((1500 - w) / 2, 850), setting.address.upper(), font=fnt, fill=(0,0,0))

    # d.text((410, 750),'MKPATAK'.upper(), fill=(0, 0, 0), font=fnt)

    w, h = d.textsize('student identity card'.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 1000), 'student identity card'.upper(), font=smallfnt, fill=(0,0,0))

    try:
        passp = Image.open(passport)
    except:
        passp = Image.open(setting.logo)
    size = 750
    passp.thumbnail((size,size), Image.ANTIALIAS)
    print(passp.size)
    img.paste(passp, (750-round(passp.size[0]/2), 1125))
    
    name = str(surname).upper()+' '+str(firstname).upper()
    
    w, h = d.textsize(name.upper(), font=normalFont)
    d.text(((1500 - w) / 2, 1125+passp.size[1]+50), name.upper(), font=normalFont, fill=(0,0,0))


    para = textwrap.wrap(str(prog).upper(), width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 1125+passp.size[1]+150, 20
    for line in para:
        w, h = d.textsize(line, font=normalFont)
        d.text(((MAX_W - w) / 2, current_h), line, font=normalFont, fill=(0,0,0))
        current_h += h + pad

    w, h = d.textsize(studentID.upper(), font=normalFont)
    d.text(((1500 - w) / 2, current_h+50), studentID.upper(), font=normalFont, fill=(0,0,0))

    ## Back Image Creation
    img2 = Image.new('RGB', (1500, 2550), color = (255, 255, 255))

    barcode_img = createCodes(studentID)
    # barcode = Image.open(studentID+'.png')
    barcode = createCodes(studentID)
    print(barcode.size)
    barcode = barcode.resize((750,750), Image.ANTIALIAS)
    print(barcode.size)

    img2.paste(barcode, (750-round(barcode.size[0]/2), 200))

    ## Back Logo
    back_Logo = logo.resize((logo.size[0]*3, logo.size[1]*3))
    back_Logo = flattenAlpha(back_Logo, 0.15)

    img2.paste(back_Logo, (750-round(back_Logo.size[0]/2), 1000), back_Logo)


    ## Back Text
    d1 = ImageDraw.Draw(img2)
    back_text = f'The card must be in the possession of the cardholder when on University premises and remains the property of {setting.name.title()} at all times. If found please return to security.'
    
    para = textwrap.wrap(back_text, width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 975, 20
    for line in para:
        w, h = d1.textsize(line, font=normalBackFont)
        d1.text(((MAX_W - w) / 2, current_h), line, font=normalBackFont, fill=(0,0,0))
        current_h += h + pad
    # d1.text((100,900), text=textwrap.fill(back_text,width=32, break_long_words=False,), fill=(0,0,0), font=normalFont)

    ## Registrar Sign
    sign = Image.open(setting.signature)
    size = 750
    sign.thumbnail((size,size), Image.ANTIALIAS)
    # print(passp.size)

    # sign = sign.resize((sign.size[0], sign.size[1]))
    print('Signature Size is: ', sign.size)

    img2.paste(sign, (round((MAX_W - sign.size[0])/2), 1650), sign)


    w, h = d1.textsize('Ag. Registrar', font=normalBackFont)
    d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 1930), 'Ag. Registrar', font=normalBackFont, fill=(0,0,0))

    w, h = d1.textsize(setting.website, font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2100), setting.website, font=smallfnt, fill=(0,0,0))

    w, h = d1.textsize(setting.phone_number, font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2200), setting.phone_number, font=smallfnt, fill=(0,0,0))
    
    out_folder = os.path.join(BASE_DIR, 'media')

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    img.save(out_folder+'/'+str(studentID)+'_front.png')
    img2.save(out_folder+'/'+str(studentID)+'_back.png')


def createIUFPID(surname, firstname, studentID, prog, passport, level=None):

    ## Font colors
    white = (255,255,255)
    black = (0,0,0)
    blue = (1, 153, 219)

    ## Fonts
    fnt = ImageFont.truetype('Myriad Pro Bold.ttf',size=125)
    smallfnt = ImageFont.truetype('Myriad Pro Bold.ttf',size=63)
    normalFont = ImageFont.truetype('Myriad Pro Bold.ttf',size=85)
    normalBackFont = ImageFont.truetype('MYRIADPRO-REGULAR.OTF',size=85)

    ## Front Image Creation
    img = Image.new('RGB', (1500, 2550), color = (255, 255, 255))

    
    ## Add Uni Logo
    logo = Image.open("logo.png")
    logo = logo.resize((round(logo.size[0]*0.8/2), round(logo.size[1]*0.8/2)))
    # foreground = Image.open("test2.png")
    img.paste(logo, (750-round(logo.size[0]/2), 320), logo)

    d = ImageDraw.Draw(img)

    ##Back Logo
    back_Logo = logo.resize((logo.size[0]*4, logo.size[1]*4))
    back_Logo = flattenAlpha(back_Logo, 0.03)
    img.paste(back_Logo, (750-round(back_Logo.size[0]/2), 800), back_Logo)


    # d.polygon([(0,750), (750,0),(0,0)], fill=blue)

    # d.rectangle((0,100,300,150), fill=white)

    coords = [[(0,675), (675,0),(0,0)], [(0,600), (600,0),(0,0)],[(0,525), (525,0),(0,0)],[(0,450), (450,0),(0,0)],[(0,375), (375,0),(0,0)]]
    coords1 = [[(0,641.25), (641.25,0),(0,0)],[(0,570), (570,0),(0,0)],[(0,498.75), (498.75,0),(0,0)],[(0,427.5), (427.5,0),(0,0)],[(0,356.25),(356.25,0),(0,0)]]

    # level_num = int(level)/100

    # for num in range(int(level_num)):
    #     d.polygon(coords[num], fill=white)
    d.polygon(coords1[-1], fill=blue)


    w, h = d.textsize('TOPFAITH INTERNATIONAL SECONDARY SCHOOL'.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 700),'TOPFAITH INTERNATIONAL SECONDARY SCHOOL'.upper(), fill=(0, 0, 0), font=smallfnt)

    w, h = d.textsize('MKPATAK'.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 800), 'MKPATAK'.upper(), font=smallfnt, fill=(0,0,0))

    # d.text((410, 750),'MKPATAK'.upper(), fill=(0, 0, 0), font=fnt)

    w, h = d.textsize('student identity card'.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 900), 'student identity card'.upper(), font=smallfnt, fill=(0,0,0))

    # d.text((340, 900),'student identity card'.upper(), fill=(0, 0, 0), font=smallfnt)

    # d.rectangle((0,1400,1500,2550), fill=(109,69,137))
    # d.polygon([(0,1400), (1500,2550),(0,1500)], fill=(109,69,137))
    # d.polygon([(1500,2000), (750,2550),(1500,2550)], fill=(109,69,137))

    try:
        passp = Image.open(passport)
    except:
        passp = Image.open("logo.png")
    size = 750
    passp.thumbnail((size,size), Image.ANTIALIAS)
    print(passp.size)
    img.paste(passp, (750-round(passp.size[0]/2), 1075))


    ## Bottom Section
    # # RHS
    # d.text((150, 1800),'Surname:', font=normalFont,fill=black,)
    # d.text((150, 1910),'Other Names:', font=normalFont,fill=black,)
    # d.text((150, 2020),'Student No:', font=normalFont,fill=black,)
    # d.text((150, 2130),'Programme:', font=normalFont,fill=black,)
    # # d.text((150, 1700),'Surname:'.upper(), font=normalFont,fill=(255, 255, 255),)

    # # LHS
    # d.text((750, 1800),str(surname).upper(), font=normalFont,fill=black,)
    # d.text((750, 1910),str(firstname).upper(), font=normalFont,fill=black,)
    # d.text((750, 2020),str(studentID), font=normalFont,fill=black,)
    # d.text((750, 2130),textwrap.fill(str(prog).upper(), width=15, break_long_words=False), font=normalFont,fill=black,)
    # d.text((150, 1700),'Surname:'.upper(), font=normalFont,fill=(255, 255, 255),)
    
    name = str(surname).upper()+' '+str(firstname).upper()
    
    w, h = d.textsize(name.upper(), font=normalFont)
    d.text(((1500 - w) / 2, 1125+passp.size[1]+50), name.upper(), font=normalFont, fill=(0,0,0))


    para = textwrap.wrap(prog.upper(), width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 1125+passp.size[1]+150, 20
    for line in para:
        w, h = d.textsize(line, font=normalFont)
        d.text(((MAX_W - w) / 2, current_h), line, font=normalFont, fill=(0,0,0))
        current_h += h + pad

    w, h = d.textsize(studentID.upper(), font=normalFont)
    d.text(((1500 - w) / 2, current_h+50), studentID.upper(), font=normalFont, fill=(0,0,0))

    ## Back Image Creation
    img2 = Image.new('RGB', (1500, 2550), color = (255, 255, 255))

    barcode_img = createCodes(studentID)
    barcode = Image.open(studentID+'.png')
    print(barcode.size)
    barcode = barcode.resize((750,750), Image.ANTIALIAS)
    print(barcode.size)

    img2.paste(barcode, (750-round(barcode.size[0]/2), 200))

    ## Back Logo
    back_Logo = logo.resize((logo.size[0]*3, logo.size[1]*3))
    back_Logo = flattenAlpha(back_Logo, 0.1)

    img2.paste(back_Logo, (750-round(back_Logo.size[0]/2), 1000), back_Logo)


    ## Back Text
    d1 = ImageDraw.Draw(img2)
    back_text = 'The card must be in the possession of the cardholder when on University premises and remains the property of Topfaith at all times. If found please return to security.'
    
    para = textwrap.wrap(back_text, width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 975, 20
    for line in para:
        w, h = d1.textsize(line, font=normalBackFont)
        d1.text(((MAX_W - w) / 2, current_h), line, font=normalBackFont, fill=(0,0,0))
        current_h += h + pad
    # d1.text((100,900), text=textwrap.fill(back_text,width=32, break_long_words=False,), fill=(0,0,0), font=normalFont)

    ## Registrar Sign
    sign = Image.open('MrsAugustine1.png')
    sign = sign.resize((round(sign.size[0]/3), round(sign.size[1]/3)))

    img2.paste(sign, (round((MAX_W - sign.size[0])/2), 1500), sign)


    w, h = d1.textsize('Principal', font=normalBackFont)
    d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 1930), 'Principal', font=normalBackFont, fill=(0,0,0))

    w, h = d1.textsize('topfaith.edu.ng | topfaith.sch.ng', font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2100), 'topfaith.edu.ng | topfaith.sch.ng', font=smallfnt, fill=(0,0,0))

    w, h = d1.textsize('08053475763, 07066211122', font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2200), '08053475763, 07066211122', font=smallfnt, fill=(0,0,0))
    
    out_folder = 'iufp/'+dt.now().strftime('%Y-%m-%d')

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    img.save(out_folder+'/'+str(studentID)+'_front.png')
    img2.save(out_folder+'/'+str(studentID)+'_back.png')



def createStaffID(surname, firstname, studentID, prog, passport, year):
    ## Fonts
    fnt = ImageFont.truetype('Myriad Pro Bold.ttf',size=125)
    smallfnt = ImageFont.truetype('Myriad Pro Bold.ttf',size=63)
    normalFont = ImageFont.truetype('MYRIADPRO-REGULAR.OTF',size=85)

    ## Front Image Creation
    img = Image.new('RGB', (1500, 2550), color = (255, 255, 255))
    
    ## Add Uni Logo
    logo = Image.open("TU_logo_cropped_1.png")
    logo = logo.resize((round(logo.size[0]*0.8), round(logo.size[1]*0.8)))
    # foreground = Image.open("test2.png")
    img.paste(logo, (750-round(logo.size[0]/2), 320), logo)

    d = ImageDraw.Draw(img)
    w, h = d.textsize('TOPFAITH UNIVERSITY'.upper(), font=fnt)
    d.text(((1500 - w) / 2, 700),'TOPFAITH UNIVERSITY'.upper(), fill=(0, 0, 0), font=fnt)

    w, h = d.textsize('MKPATAK'.upper(), font=fnt)
    d.text(((1500 - w) / 2, 850), 'MKPATAK'.upper(), font=fnt, fill=(0,0,0))

    # d.text((410, 750),'MKPATAK'.upper(), fill=(0, 0, 0), font=fnt)

    w, h = d.textsize('Staff identity card'.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 1000), 'staff identity card'.upper(), font=smallfnt, fill=(0,0,0))

    # d.text((340, 900),'student identity card'.upper(), fill=(0, 0, 0), font=smallfnt)

    # d.rectangle((0,1400,1500,2550), fill=(109,69,137))

    ##Back Logo
    back_Logo = logo.resize((logo.size[0]*5, logo.size[1]*5))
    back_Logo = flattenAlpha(back_Logo, 0.08)

    img.paste(back_Logo, (750-round(back_Logo.size[0]/2), 800), back_Logo)

    ## Passport
    try:
        passp = Image.open(passport)
    except:
        passp = Image.open("TU_logo_cropped_1.png")
    size = 750
    passp.thumbnail((size,size), Image.ANTIALIAS)
    print(passp.size)
    img.paste(passp, (750-round(passp.size[0]/2), 1125))

    


    ## Bottom Section
    name = firstname+' '+surname
    
    w, h = d.textsize(name.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 1125+passp.size[1]+50), name.upper(), font=smallfnt, fill=(0,0,0))

    w, h = d.textsize(prog.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 1125+passp.size[1]+130), prog.upper(), font=smallfnt, fill=(0,0,0))

    w, h = d.textsize(studentID.upper(), font=smallfnt)
    d.text(((1500 - w) / 2, 1125+passp.size[1]+210), studentID.upper(), font=smallfnt, fill=(0,0,0))

    # d.text((150, 1800),'Surname:', font=normalFont,fill=(255, 255, 255),)
    # d.text((150, 1910),'Other Names:', font=normalFont,fill=(255, 255, 255),)
    # d.text((150, 2020),'Student No:', font=normalFont,fill=(255, 255, 255),)
    # d.text((150, 2130),'Programme:', font=normalFont,fill=(255, 255, 255),)
    # d.text((150, 1700),'Surname:'.upper(), font=normalFont,fill=(255, 255, 255),)

    # LHS
    # d.text((750, 1800),str(surname).upper(), font=normalFont,fill=(255, 255, 255),)
    # d.text((750, 1910),str(firstname).upper(), font=normalFont,fill=(255, 255, 255),)
    # d.text((750, 2020),str(studentID), font=normalFont,fill=(255, 255, 255),)
    # d.text((750, 2130),textwrap.fill(str(prog).upper(), width=15, break_long_words=False), font=normalFont,fill=(255, 255, 255),)
    # d.text((150, 1700),'Surname:'.upper(), font=normalFont,fill=(255, 255, 255),)

    ## Back Image Creation
    img2 = Image.new('RGB', (1500, 2550), color = (255, 255, 255))

    ## Back Logo
    # back_Logo = logo.resize((logo.size[0]*6, logo.size[1]*6))
    # back_Logo = flattenAlpha(back_Logo, 0.05)

    img2.paste(back_Logo, (750-round(back_Logo.size[0]/2), 800), back_Logo)

    ## Barcode Creation
    barcode_img = createStaffCodes(studentID, year=year)
    barcode = Image.open(studentID+'.png')
    print(barcode.size)
    barcode = barcode.resize((750,750), Image.ANTIALIAS)
    print(barcode.size)

    img2.paste(barcode, (750-round(barcode.size[0]/2), 200))

    ## Back Text
    d1 = ImageDraw.Draw(img2)
    back_text = 'The card must be in the possession of the cardholder when on University premises and remains the property of Topfaith University at all times. If found please return to security.'
    
    para = textwrap.wrap(back_text, width=32)
    MAX_W, MAX_H = 1500, 2550
    current_h, pad = 975, 20
    for line in para:
        w, h = d1.textsize(line, font=normalFont)
        d1.text(((MAX_W - w) / 2, current_h), line, font=normalFont, fill=(0,0,0))
        current_h += h + pad
    # d1.text((100,900), text=textwrap.fill(back_text,width=32, break_long_words=False,), fill=(0,0,0), font=normalFont)

    ## Registrar Sign
    sign = Image.open('EDSnT.png')
    sign = sign.resize((sign.size[0]*2, sign.size[1]*2))

    img2.paste(sign, (round((MAX_W - sign.size[0])/2), 1650), sign)


    w, h = d1.textsize('Ag. Registrar', font=normalFont)
    d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 1930), 'Ag. Registrar', font=normalFont, fill=(0,0,0))

    w, h = d1.textsize('topfaith.edu.ng', font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2100), 'topfaith.edu.ng', font=smallfnt, fill=(0,0,0))

    w, h = d1.textsize('08053475763, 08137357200', font=smallfnt)
    # d1.rectangle((((MAX_W - w) / 2)-50,1880,((MAX_W + w) / 2)+50,1890), fill=(0,0,0))
    d1.text(((MAX_W - w) / 2, 2200), '08053475763, 08137357200', font=smallfnt, fill=(0,0,0))
    
    out_folder = 'staff/'+dt.now().strftime('%Y-%m-%d')

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    img.save(out_folder+'/'+str(studentID)+'_front.png')
    img2.save(out_folder+'/'+str(studentID)+'_back.png')


def manualCreation(df1):
    for num in range(df1.shape[0]):
        try:
            data = list(df1.iloc[num,:])
            data = [str(x) for x in data]
            if data[-1] == 'Student':
                createID(*data[:-1])
            elif data[-1] == 'Staff':
                createStaffID(*data[:-1])
            elif str(data[-1]).lower() == 'iufp':
                createIUFPID(*data[:-1])
        except Exception as err:
            print(err)

if __name__ == '__main__':
    # createID('Abraham', 'etimbuk', '000001', 'Mass Communication', '202100049.jpg', '500')
    # createIUFPID('Abraham', 'etimbuk', '000001', 'Foundation Programme', '202100049.jpg', '200')
    # createCodes1('AKP/P/CON/496', 'text')
    manualCreation(pd.read_csv('2022-10-28/output/output20221028.csv'))