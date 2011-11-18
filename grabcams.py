import sys, urllib2, urlparse, glob, re, web, StringIO
from BeautifulSoup import BeautifulSoup
from PIL import Image,ImageStat
from random import choice

urls = (
    '/(.*)', 'cams'
)

application = web.application(urls, globals()).wsgifunc()

class cams:
	def GET(self,name):
		base = 'http://commuterlink.utah.gov'
		dir = '1_devices'
		images = []
		i = 0
		page = urllib2.urlopen('/'.join((base,dir)))
		soup = BeautifulSoup(page)
		while i < 10:
			entry = choice(soup('a'))
			if re.search('jpe*g',entry['href'],re.IGNORECASE):
				imageio = StringIO.StringIO(urllib2.urlopen(''.join((base,entry['href']))).read())
				im = Image.open(imageio)
				stats = ImageStat.Stat(im);
				if 50 < (float(sum(stats.mean)) / len(stats.mean)) < 200:
					images.append('<img width=320 height=240 src="' + base + entry['href'] + '">')
					i += 1
				else:
					print >> sys.stderr, entry['href'] + ' was discarded with mean pixel values of ' + ', '.join(map(str,stats.mean))
		return """<html>
	<head>
		<title>traffic in utah</title>
	</head>
	<body>
		<h1>visit utah!</h1>'
""" + "\n".join(images) + """
		<hr>
		<p>What this does:
			<ol>
				<li>Grab random images from http://commuterlink.utah.gov/
				<li>Throw out the ones that are just text, black or white
				<li>Once we have 10 good ones, show the Utah goodness!
			</ol>
		</p>
		<p>Python source <a href="https://github.com/mvexel/VisitUtah">here</a>.
		<hr>
		<em>A <a href="http://oegeo.wordpress.com/">Very Furry</a> Procrastination Project done on 11/18/11</em>
	</body>
</html>"""
#	print urls
