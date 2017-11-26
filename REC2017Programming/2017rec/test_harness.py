from flask import Flask, request, render_template
from flask_restful import Api
from flask_jsonpify import jsonify

from math import sin, pi
from time import sleep
from random import seed, randint

import socketio
import eventlet
import eventlet.wsgi

import sys
import hashlib
from time import strftime, time, gmtime

sio = socketio.Server(logger=True, async_mode=None)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'


if len(sys.argv) < 3:
	print (f"Usage: python {sys.argv[0]} <port> <filename>")
	exit()
port = sys.argv[1]
data_file = sys.argv[2]

# edge fields
FROM_NODE = 0
TO_NODE = 1
AVG_KMH = 2
DIST_METRES = 3

timestamp = 0
edge_wts = {}

class Session():
	def __init__(self, team_id):
		self.team_id = team_id
		self.graph = []
		self.journey = []
		self.elapsed_time = 0

sessions = {}

# home page
#
#
@app.route('/')
def root():
    return render_template('index.html', timestamp=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())) 

def push_update(data):
    # push data to client (browser)
    sio.emit('my response', data, namespace='/test')

@sio.on('disconnect request', namespace='/test')
def disconnect_request(sid):
    sio.disconnect(sid, namespace='/test')


@sio.on('connect', namespace='/test')
def test_connect(sid, environ):
    sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
             namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')

# reset & start
# refesh the graph from scratch
#
@app.route('/start')
def reset_and_start():
	global timestamp
	global sessions
	global edge_wts

	timestamp = int(time())

	team_id = request.args.get('team_id')
	t = str(time())
	key = str(hash_me(f"{team_id}{t}"))

	sessions[key] = Session(team_id)
	graph = sessions[key].graph

	print(f"team: {team_id}, key: {key}")
	
	with open(data_file) as f:
		lines = f.read().splitlines()

	# compute the weights (elapsed time) for each edge
	for line in lines:
		edge = line.split(',')
		et_sec = 3600.0*int(edge[DIST_METRES])*1000.0/float(edge[AVG_KMH])
		edge_wts[edge[FROM_NODE],edge[TO_NODE]] = et_sec
	
		# add the edge to the graph
		graph.append(edge)

	start_node = 0
	end_node = 24

	response = f"{{\"key\":{key}, \"start_node\": {start_node}, \"end_node\": {end_node}}}"
	print(response)
	return response

#
#
#
@app.route('/getNext')
def get_next():
	global sessions
	global edge_wts

	key = request.args.get('key')
	node_id = request.args.get('node_id')
	print("key", key, "node_id", node_id)

    # append coordinates to journey
	sessions[key].journey.append(node_id)
	j = sessions[key].journey

	# only accumulate weight and update display if more than one node
	if len(j) > 1:
		try:
			et = float(edge_wts[j[-2],j[-1]])
		except:
			et = 0

		sleep(et/10)

		# accumulate the elapsed time
		sessions[key].elapsed_time += et

		# push the new graph for redraw
		#u pdate_display(sessions[key].elapsed_time, sessions[key].journey)
		update_display(sessions[key])

	# return evolved graph
	evolve(sessions[key].graph)
	json = jsonify(sessions[key].graph)

	print("---")
	return json

# ------------------------------------------------------------------------------

def update_display(session):
	et = float("{:.4f}".format(session.elapsed_time))
	push_update({'elapsed_time':et,'journey':[session.journey]})
	print('update', 'elapsed_time', et, 'journey', session.journey)


# wrap the python hashing algorithm with something easier
def hash_me(msg=""):
    hash = int(hashlib.sha1(str(msg).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    return int(hash + int(time())) % 30011

# evolve the graph's weights in time
def evolve(graph):
	global edge_wts
	s = str(time()).split(".")[1]
	seed(int(s) % 3)
	c = clocktick()
	t = next(c)

	for edge in graph:
		avg_kmh = float(edge[AVG_KMH]) - randint(0, 5)  # randomly lower the average speed
		avg_kmh = max(5, avg_kmh)
		edge[AVG_KMH] = avg_kmh
		edge_wts[edge[FROM_NODE],edge[TO_NODE]] = 3600.0*float(edge[DIST_METRES])/1000.0/avg_kmh
	x = randint(1, len(graph)-2)
	del graph[x]


def clocktick(n = 0):
	while True:
		yield n
		n += 1

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5002)), app)
