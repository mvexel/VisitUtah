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
		discarded = []
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
					discarded.append('<img width=160 height=120 src="' + base + entry['href'] + '">')
		return """<html>
	<head>
		<title>traffic in utah</title>
		<script language=javascript>
		function toggle(id) {
			elem = document.getElementById(id);
			linkelem = document.getElementById(id + '_link')
			if(!elem) return false;
			elem.style.display = (elem.style.display=='block') ? 'none' : 'block'
			linkelem.innerHTML = (elem.style.display=='block') ? 'hide' : 'show'
		}
		</script>
	</head>
	<body>
		<h1>visit utah!</h1>'
""" + "\n".join(images) + """
		<div id=discarded style='display:none'>
			<hr>
			<em>discarded images: </em>
""" + "\n".join(discarded) + """
		</div>
		<hr>
		<p>What this does:
			<ol>
				<li>Grab random images from http://commuterlink.utah.gov/
				<li>Using <a href="http://www.pythonware.com/products/pil/">PIL</a>, throw out the ones that are just text, black or white (<a id='discarded_link' href="#" onClick=toggle('discarded')>show</a>)
				<li>Once we have 10 good ones, show the Utah goodness!
			</ol>
		</p>
		<p>Python source <a href="https://github.com/mvexel/VisitUtah">here</a>.
		<hr>
		<em>A <a href="http://oegeo.wordpress.com/">Very Furry</a> Procrastination Project done on 11/18/11</em>
	</body>
</html>"""
