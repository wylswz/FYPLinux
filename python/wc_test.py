from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'wiki/1')).read()

# read the mask / color image
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = imread(path.join(d, "250px.jpg"))

wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
               stopwords=STOPWORDS.add("said"),
               max_font_size=40, random_state=42)
wc = WordCloud()
print text
# generate word cloud
a = [('asd',0.3),('aaa',0.2)]
wc.generate_from_frequencies(a)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc)
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()