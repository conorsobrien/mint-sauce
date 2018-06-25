from pytesseract import image_to_string
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

img=Image.open('test.png')

# Split image into separate images for analysis.
iresult = img.crop((800,105,1140,130))
ip1name = img.crop((281,372,509,393))
ip1faction = img.crop(( 274,107,476,129))
ip2name = img.crop((1472,372,1680,395))
ip2faction = img.crop((1454,105,1650,135))
ip1u1 = img.crop((250,405,300,514))
# Modify certain values like brightness, contract, sharpness, color
enhancer = ImageEnhance.Color(ip2name)
#ip2name = enhancer.enhance(0.0)
#ip2name = ip2name.convert('L')
#ip2name = ip2name.point(lambda x: 0 if x<128 else 255, '1')

ip2faction = ip2faction.convert('L')
ip2faction = ip2faction.point(lambda x: 0 if x<128 else 255, '1')

#ip2name = ImageOps.invert(ip2name)
print(str(img.mode))
text=image_to_string(img,lang="eng")

result = image_to_string(iresult,lang="eng")
p1name = image_to_string(ip1name,lang="eng")
p1faction = image_to_string(ip1faction,lang="eng")
p2name = image_to_string(ip2name, lang="eng")
p2faction = image_to_string(ip2faction, lang="eng")


print(p1name + '(' + p1faction + ')' + ' vs. ' + p2name + ' (' + p2faction + ')' + ' - ' + result)
#ip2name.save('ip2name','png')
ip2name.show()
~
