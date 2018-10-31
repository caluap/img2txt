from PIL import Image
import numpy
import json, codecs
import random
import math
from pprint import pprint

artists_json = 'artists.json'
image = 'test_img.png'

# reads the artists file and creates a wall of text
artists = []

with open(artists_json, 'rb') as json_data:
    artists = json.load(json_data)['artists']
    json_data.close()
  
random.shuffle(artists)
s = artists[0]
for a in artists[1:]:
    s += ' & ' + a

# as each char = 1 pixel, what size image do we need?
area = len(s)
w = math.sqrt(area/math.sqrt(2))
h = w * math.sqrt(2)

