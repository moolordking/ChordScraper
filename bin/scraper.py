import requests
import os
import webbrowser
from bs4 import BeautifulSoup

def get_content(url):
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	}
	 
	response = requests.get(url, headers=headers)
	 
	if response.status_code == 200:
	    return response.text
	else:
	    print(f'Request failed with status code: {response.status_code}')

def ultimate_filter(html):
	punc = [",", ".", ":"]
	if not('&quot;content&quot;:' in html):
		return None
	html = html.split('&quot;content&quot;:')[1].split('revision_id')[0]
	html = html.replace("\\r", "").replace("[tab]", "").replace("[/tab","").replace("[ch]", "<<").replace("[/ch]", ">>").replace("&quot;", "").replace("&#039;","'").replace("&rsquo;","'").replace("\u0435", "").replace("\u0421", "")
	html = html.split("\\n")
	combined = ""
	for i, line in enumerate(html):
		if len(line) < 3 or '">' in line:
			continue
		if "<<" in line:
			one = 0
			two = 0
			while True:
				if i+1<len(html) and two < len(html[i+1]) and html[i+1][two] in punc:
					combined += html[i+1][two]
					two+=1
				if one < len(line) and line[one] != " ":
					combined += line[one]
					one+=1
				elif i+1<len(html) and  two < len(html[i+1]):
					combined += html[i+1][two]
					one+=1
					two+=1
				else:
					break
			combined += "\n"


	return combined

def filter_out(html):
	punc = [",", ".", ":"]
	if not('<pre id="core"' in html):
		return None
	html = html.split('<pre id="core"')[1].split('</pre>')[0]
	html = html.replace("<u>","<<").replace("</u>",">>").replace("\r","").replace("\t","")
	html = html.split("\n")
	combined = ""
	for i, line in enumerate(html):
		if len(line) < 3 or '">' in line:
			continue
		if "<<" in line:
			one = 0
			two = 0
			while True:
				if two < len(html[i+1]) and html[i+1][two] in punc:
					combined += html[i+1][two]
					two+=1
				if one < len(line) and line[one] != " ":
					combined += line[one]
					one+=1
				elif two < len(html[i+1]):
					combined += html[i+1][two]
					one+=1
					two+=1
				else:
					break
			combined += "\n"


	return combined

def process(file, folder="filtered_songs"):
	if not(os.path.exists(folder)):
		os.makedirs(folder)
	with open(file) as f:
		lines = f.readlines()
		for l in lines:
			song_artist = l.split(" - ")
			song = song_artist[0].replace(" ", "-").replace("\n", "").replace(",","").replace("?","")
			artist = song_artist[1].replace(" ", "-").replace("\n", "")
			my_url = "https://www.e-chords.com/chords/" + artist + "/" + song
			print(my_url)
			urled = get_content(my_url)
			if urled == None:
				print("x")
				continue
			result = filter_out(urled)
			if result == None or len(result) < 10:
				print("x")
				continue
			g = open(folder + "/" + song + " by " + artist + ".txt", "w")
			g.write(result)
			g.close()
			print("y")

def ultimate_process(url, s=True, folder="filtered_songs"):
	if not(os.path.exists(folder)):
		os.makedirs(folder)
	print(url)
	urled = get_content(url)
	if urled == None:
		return
	result = ultimate_filter(urled)
	if result == None:
		return
	root = url.split("/tab/")[1].split("/")
	artist = root[0]
	song = root[1].split("-chords")[0]
	g = open(folder + "/" + song + " by " + artist + ".txt", "w")
	g.write(result)
	g.close()
	if s:
		print(result)
	return result
	# input("")

# process("SONGS.txt")
def scrape_chords(artist_and_song, o=False, s=True):
	try:
		search = artist_and_song + ' chords ug'
		url = 'https://www.google.com/search'

		headers = {
			'Accept' : '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
		}
		parameters = {'q': search}

		content = requests.get(url, headers = headers, params = parameters).text
		soup = BeautifulSoup(content, 'html.parser')

		search = soup.find(id = 'search')
		first_link = search.find('a')
		if len(first_link['href'].split("/")) < 6 or len(first_link['href'].split("/")) > 6:
			return

		result = ultimate_process(first_link['href'], s)
		if o:
			f = open("bin/TEMPLATE.txt", "r")
			root = first_link['href'].split("/tab/")[1].split("/")
			artist = root[0].replace("-"," ")
			song = root[1].split("-chords")[0].replace("-"," ")
			html = f.read().replace("@@@", "["+song+" by "+artist+"]\n"+result)
			path = os.path.abspath('bin/temp.html')
			url = 'file://' + path
			with open(path, 'w') as f:
			    f.write(html)
			webbrowser.open(url)
		else:
			return result
	except:
		return False


if __name__ == "__main__":
	scrape_chords(input("Artist and Song: "), True)
