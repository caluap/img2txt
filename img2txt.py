from PIL import Image
import numpy
import json, codecs
import random
import math
from pprint import pprint

artists_json = 'artists.json'
image_file = 'test_img.png'
font_file = 'LeagueMonoVariable.ttf'
g = 1.2
font_size = 4 * g
line_adj = 1.15 * g
m_x = 3.5 * g
m_y = m_x * line_adj

separator = '·'


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
random.shuffle(artists)
s+= separator
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

installed_font = installFont('fonts/'+font_file)
f = font(installed_font)


axes_list = {}
for axis, data in listFontVariations().items():
    a = {
            'name': axis,
            'min': data['minValue'],
            'max': data['maxValue'],
            'default': data['defaultValue']
        }
    axes_list[axis] = a    
#pprint(axes_list)

pprint((w,h))
pprint((len(img_array), len(img_array[0])))

m_h = 297 / h
m_w = 210 / w

for y in range(len(img_array)):
    for x in range(len(img_array[y])):

        txt = FormattedString()
        txt.font(f)
        txt.fontSize(font_size)
        
        args = {}
        axis = 'wght'
        
        # finds gray value and axis equivalent
        v = 1 - img_array[y][x][0] / 255.0
        max_axis = axes_list[axis]['max']
        min_axis = axes_list[axis]['min']
        delta = max_axis - min_axis
        n_v = int(v * delta + min_axis)
        
        args[axis] = n_v
        txt.fontVariations(**args)
        c = s[x + y*w]

        #txt.append(c)
        if c == ' ':
            continue

        txt.append(c)
        n_y = h - y # this is because drawbot starts from the bottom
        text(txt, (x * m_x, n_y * m_y))
        
      
#textBox(txt, (0, 297))
uninstallFont(font_file)


