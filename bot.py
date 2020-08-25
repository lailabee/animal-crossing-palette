import tweepy #for tweeting
import secrets #twitter keys
import math
from PIL import Image
import numpy as np
import pandas as pd
import random
import os
import cv2

# returns the euclidean distance of two triples aka color values of two pixels
def dist(t1,t2):
    a = (t1[0] - t2[0]) ** 2
    b = (t1[1] - t2[1]) ** 2
    c = (t1[2] - t2[2]) ** 2
    return math.sqrt(a + b + c)

# returns the average of a list of triples aka color values of pixels

def avg(tlist):
    a = 0
    b = 0
    c = 0
    tot = len(tlist)
    for x in tlist:
        a += x[0]
        b += x[1]
        c += x[2]
    return (a//tot,b//tot,c//tot)

def genrandomcolor():

    return list(np.random.choice(range(256), size=3))

def get_palette(name,path):

	# turn image into numpy array
	image = Image.open(path)
	im = np.array(image)
	rows = im.shape[0]
	cols = im.shape[1]
	loops = 25 #iterations to convergence
	k = 5 #clusters

	# dict of clusters {c1,c2,c3,c4,c5}
	# key = name
	# value = tuple (currcolor, list of pixels in the cluster)

	clusters = {
	    "c1" : [genrandomcolor(), []],

	    "c2" : [genrandomcolor(), []],

	    "c3" : [genrandomcolor(), []],

	    "c4" : [genrandomcolor(), []],

	    "c5" : [genrandomcolor(), []]

	    }

	pixels = {}

	for i in range(loops): #max iterations
	    for x in range(rows):
	        for y in range(cols): #together will iterate over each pixel value
	            dim = (x,y)
	            minD = ("c", math.inf) #min euc distance from a given pixel
	            pix = im[x][y] #get color value at a given pixel
	            for c in clusters: #for each center
	                d = dist(pix,clusters[c][0]) #compute euclidean distance of pix to c's color val
	                minD = (c,d) if d < minD[1] else minD #replace minD with new value if its lower
	            clusters[minD[0]][1].append(pix) #append pix to the list for the cluster of min value in d
	            if i == (loops - 1):
	                pixels.update({dim : clusters[minD[0]][0]})
	                #save each dim in a dictionary with key = dim, value = minD[0][0]
	    for c in clusters: #for each center
	        clist = clusters[c][1]
	        if len(clist) != 0 and i != (loops - 1):
	            clusters[c][0] = avg(clist) #move c to the average of the points in its cluster
	            clusters[c][1] = [] #clear out list for next iteration

	# palette of 5 colors as a numpy array for visualization

	l=[]
	for c in clusters:
	    l.append(clusters[c][0])

	#palette = np.array([l])
	palette = []
	for colorlist in l:
		palette.append((colorlist[0],colorlist[1],colorlist[2]))

	hexcodes = ""
	l = sorted(l, key=lambda x: sum(x))
	for color in l:
		hexcodes += "%02x%02x%02x" % (color[0],color[1],color[2])
		if color is not l[4]:
			hexcodes += ", "

	def plot_colors(palette):
	    # initialize the bar chart representing the relative frequency
	    # of each of the colors
	    bar = np.zeros((85, 256, 3), dtype="uint8")
	    startX = 0
	    margin = 13

	    # Sort the centroids to form a gradient color look
	    centroids = sorted(palette, key=lambda x: sum(x))
	    
	    new_length = 256 - 10 * 5

	    # loop over the percentage of each cluster and the color of
	    # each cluster
	    for color in centroids:
	        endX = startX + new_length/5
	        cv2.rectangle(bar, (int(startX), 0), (int(endX), 85), (int(color[0]),int(color[1]),int(color[2])), -1)
	        cv2.rectangle(bar, (int(endX), 0), (int(endX + margin), 85),
	                      (255, 255, 255), -1)
	        startX = endX + margin

	    # return the bar chart
	    return bar

	# Let's plot the retrieved colors. See the plot_colors function
	    # for more details
	bar = plot_colors(palette)

	im = np.zeros((10, int(rows), 3), np.uint8)
	cv2.rectangle(im, (0, 0), (int(rows), 10),
	              (255, 255, 255), -1)

	icon_path = name+ ".png"
	# Now we combine the video frame and the color bar into one image
	im2 = Image.open(icon_path)
	im2 = im2.convert('RGB')

	final_path = name + "full.png"
	newImg = np.concatenate([im2, im, bar, im], axis=0)
	cv2.imwrite(final_path, newImg)

	return final_path,hexcodes

def get_villager():
	ac = pd.read_csv("data/acnh_characters.csv")
	line = random.randint(1,445)
	name = ac['Name'][line]
	url = "" + ac['URL'][line]
	filename = name + ".png"
	os.system("wget -O {0} {1}".format(filename,url))

	return name,filename

def tweet(img,name,hexcodes):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Currently Tweeting.......")
  message = "A palette for " + name + "!\nHexcodes: " + hexcodes
  api.update_with_media(img,status=message)

if __name__ == '__main__':
	name,icon = get_villager()
	img,hexcodes = get_palette(name,icon)
	tweet(img,name,hexcodes)