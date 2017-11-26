#the following program is supposed to interact with the JSON object
#currently, the program reaches the local host and is able to import the data from it
#however there is an error in converting the JSON to an object that python can interact with
#this lead us to create onymous_static.py which gets data statically and does not update with the JSON object
from urllib.request import urlopen
import json
import codecs
import requests
import json
from collections import namedtuple

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
	 


url  = urlopen('http://localhost:5002/')
webpage = urlopen('http://localhost:5002/').read().decode('utf8')
#print(webpage)
#tr = json.loads(url.decode('utf-8'))
obj = requests.get('http://localhost:5002/')
x = json2obj(url.read()) 


#json syntacx
#response = url.read()
#json = json.load(url)
'''
if json['success']:
     ob = json['response']['ob']
     print ("The current weather in Seattle is %s with a temperature of %d") % (ob['weather'].lower(), ob['tempF'])

else:
     print ("An error occurred: %s") % (json['error']['description'])
'''


'''
response = MyView.as_view()(url) # got response as HttpResponse object
response.render() # call this so we could call response.content after
json_response = json.loads(response.content.decode('utf-8'))
print (url)
print(json_response) # {"your_json_key": "your json value"}
#print(result)
#print '"networkdiff":', result['getpoolstatus']['data']['networkdiff']
'''