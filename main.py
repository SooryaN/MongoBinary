from flask import *
from pymongo import MongoClient
import gridfs
import base64
import urllib
import simplejson
app = Flask(__name__)
db = MongoClient().Images

@app.route('/')
def index():
	id=[]
	def getProfilePicUrl(url):
		api_query = urllib.urlopen(url)
		dict = simplejson.loads(api_query.read())
		for i in dict['data']:
			id.append(i['id']);
		if dict['paging']['next'] in dict['paging']:
			getProfilePicUrl(dict['paging']['next'])
	access_token=''#include access_token here
	getProfilePicUrl('https://graph.facebook.com/me/friends?access_token='+access_token)
	i=0
	for ids in id:
		print i
		pic = urllib.urlopen('https://graph.facebook.com/'+ids+'/picture') # retrieve the picture
		thedata = pic.read()
		fs = gridfs.GridFS(db)
		stored = fs.put(thedata, filename='image'+str(i))
		i+=1

	a=[]
	fs = gridfs.GridFS(db)
	for j in range(i):
		try:
			image = fs.get_last_version("image"+str(j))
			a.append(base64.b64encode(image.read()))
		except:
			pass
	return render_template('image.html',image=a)

if __name__ == '__main__':
	app.run(debug=True)
