import os
from os import walk
import webbrowser
import random as r

def open_random():
	filenames = next(walk("bin/filtered_songs"), (None, None, []))[2]
	rand = filenames[int(r.random()*len(filenames))]
	print(rand)
	g = open("bin/filtered_songs/"+rand, "r")
	result = g.read()
	g.close()
	f = open("bin/TEMPLATE.txt", "r")
	html = f.read().replace("@@@", "["+rand.replace(".txt","").replace("-"," ")+"]\n" + result)
	path = os.path.abspath('bin/temp.html')
	url = 'file://' + path
	with open(path, 'w') as f:
	    f.write(html)
	webbrowser.open(url)

if __name__ == "__main__":
	open_random()
