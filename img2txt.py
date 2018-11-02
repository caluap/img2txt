from PIL import Image
import numpy
import json, codecs
import random
import math
from pprint import pprint
import time

start = time.time()

artists_json = 'artists.json'
image_file = 'inputs/burle.5.png'

font_file = 'LeagueMonoVariable.ttf'
font_file = 'SourceCodeVariable-Italic.ttf'
font_file_2 = 'SourceCodeVariable-Roman.ttf'
font_size = 4.4

onhb_pink = 0.18, 1, 0.16, 0.0
white = 0.0, 0.0, 0.0, 0.0
rgb = 203/255.0, 7/255.0, 114/255.0

min_a = 0.0
max_a = 1.0

use_alpha = False
cmyk = white

m_x = 4.2  # this separates letters on the x axis
line_adj = 1.2 # this separates lines (beyond what m_x already does)
m_y = m_x * line_adj

separator = ' '
space = ' '
up = True


# reads the artists file and creates a wall of text
artists = []

with open(artists_json, 'rb') as json_data:
    artists = json.load(json_data)['artists']
    json_data.close()
  

random.shuffle(artists)
s = artists[0]
for a in artists[1:]:
    s += separator + a

#more density!
for i in range(2):
    random.shuffle(artists)
    for a in artists:
        s += separator + a



# as each char = 1 pixel, what size image do we need?
area = len(s)
w = math.sqrt(area/math.sqrt(2))
h = w * math.sqrt(2)

w = int(w)
h = int(h)

# opens and resizes image
img = Image.open(image_file)
img.thumbnail((w,h))
#img.resize((w,h))
img_array = numpy.array(img)


size('A4')

installed_font = []
installed_font.append(installFont('fonts/'+font_file))
installed_font.append(installFont('fonts/'+font_file_2))
f = []
for ins_f in installed_font:
    f.append(font(ins_f))

axes_list = {}
for axis, data in listFontVariations().items():
    a = {
            'name': axis,
            'min': data['minValue'],
            'max': data['maxValue'],
            'default': data['defaultValue']
        }
    axes_list[axis] = a    
pprint(axes_list)


pprint((w,h))
pprint((len(img_array), len(img_array[0])))

m_h = 297 / h
m_w = 210 / w

for y in range(len(img_array)):
    for x in range(len(img_array[y])):
        
        txt = FormattedString()

        args = {}
        axis = 'wght'
        
        # finds gray value and axis equivalent
        v = 1 - img_array[y][x][0] / 255.0
        
        # normalizes between range defined in max_a and min_a
        delta_a = max_a - min_a
        v = v*delta_a + min_a

        
        max_axis = axes_list[axis]['max']
        min_axis = axes_list[axis]['min']
        delta = max_axis - min_axis
        n_v = int(v * delta + min_axis)
        
        args[axis] = n_v
        
        
        if v < 0.5:
            txt.font(f[0])
        else:
            txt.font(f[1])
            
        txt.fontSize(font_size)
        txt.fontVariations(**args)
        c = s[x + y*w]

        if c == ' ':
            txt.append(space)
        else:
            if up:
                c = c.upper()

            n_c = cmyk                
            if use_alpha:
                alpha = 0.5 + 0.5*v
            else:
                alpha = 1.0

            cmyk_fill = (n_c[0], n_c[1], n_c[2], n_c[3], alpha)
            txt.append(c, cmykFill=cmyk_fill)
        n_y = h - y # this is because drawbot starts from the bottom
        text(txt, (x * m_x, n_y * m_y))
        
      
#textBox(txt, (0, 297))
uninstallFont(font_file)


print(int(time.time()-start))


