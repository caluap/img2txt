from PIL import Image
import numpy
import json, codecs
import random
import math
from pprint import pprint

artists_json = 'artists.json'
image_file = 'test_img.png'
font_file = 'LeagueMonoVariable.ttf'
font_size = 10


# reads the artists file and creates a wall of text
artists = []

with open(artists_json, 'rb') as json_data:
    artists = json.load(json_data)['artists']
    json_data.close()
  
random.shuffle(artists)
s = artists[0]
for a in artists[1:]:
    s += ', ' + a

# as each char = 1 pixel, what size image do we need?
area = len(s)
w = math.sqrt(area/math.sqrt(2))
h = w * math.sqrt(2)

w = int(w)
h = int(h)

# opens and resizes image
img = Image.open(image_file)
img.thumbnail((w,h))
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
        m_h = 297 / h
        m_w = 210 / w
        m_x = 2.0
        m_y = m_x*1.3
        txt.append(c)
        text(txt, (x * m_w * m_x, y * m_h * m_y))
        #textBox(txt, (x * m_w * m, y * m_h * m))
        
      
#textBox(txt, (0, 297))
uninstallFont(font_file)


