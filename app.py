#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/json_form/<uuid>', methods=['GET', 'POST'])
def json_form(uuid):
    content = request.json
    # content = request.form

    print content['mytext']
    return jsonify({"uuid":uuid})


@app.route('/api/urlencoded_form/<uuid>', methods=['GET', 'POST'])
def urlencoded_form(uuid):
    # content = request.json
    content = request.form

    print content['mytext']
    return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)