import os
import sys
import requests
import flask
import json
from flask import Flask, request, jsonify
import flask_cors

app = Flask(__name__)

flask_cors.CORS(app, supports_credentials = True)

@app.route('/kgview', methods = ['POST'])

def kg_view():
	# 获取请求数据
	entity = request.json['entity']

	url = 'https://api.ownthink.com/kg/knowledge?entity=%s'%entity # 知识图谱API
	
	sess = requests.get(url) # 请求
	text = sess.text # 获取返回的数据

	response = eval(text) # 转为字典类型
	knowledge = response['data']
	
	nodes = []
	for avp in knowledge['avp']:
		if avp[1] == knowledge['entity']:
			continue
		node = {'source': knowledge['entity'], 'target': avp[1], 'type': "resolved", 'rela':avp[0]}
		nodes.append(node)
	
	output = ""
	for node in nodes:
		node = str(node)
		node = node.replace("'type'", 'type').replace("'source'", 'source').replace("'target'", 'target')
		output += node+',\n'

	return jsonify("[\n" + output + "]")
	
if __name__ == '__main__':
	# start flask
	app.run(host='127.0.0.1', port=12345)
