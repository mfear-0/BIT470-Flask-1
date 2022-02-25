import re
from flask_restful import Resource
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, reqparse
from functools import wraps
from src.db import get_db
import sqlite3
import jwt
import datetime
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from resources.user import Users

parser = reqparse.RequestParser()

class Signup(Resource):
    def post(self, credentials):
        return 'signing up'

class Login(Resource):
    def post(self):
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()
        un = data['username']
        pw = data['password']
        if not data['username']:
            return jsonify({'error': 'enter username'})

        if not data['password']:
            return jsonify({'error': 'enter your password'})

        if not get_db().cursor().execute(f'SELECT id FROM users WHERE username = "{un}"').fetchone():
            return {'error': f'User {un} does not exist'}

        hpw = generate_password_hash(data['password'], method='sha256')

        
        res = get_db().cursor().execute(f'SELECT id FROM users WHERE username = "{un}"').fetchone()
        respw = get_db().cursor().execute(f'SELECT password FROM users WHERE username = "{un}"').fetchone()
        # respwtext = respw.fetchone()
        # restext = res.fetchone()


        con = sqlite3.connect('example.db')
        cur = con.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS token(id INTEGER NOT NULL, tokenid text PRIMARY KEY)')
        con.commit()
        con.close()

        if check_password_hash(respw[0], pw):
            token = jwt.encode({'id' : res[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, "somesecretkeything", "HS256")
            get_db().cursor().execute(f'INSERT INTO token(id, tokenid) VALUES({res[0]},"{token}")')
            get_db().commit()
            return jsonify({'token': token}, 201)
            # access_token = create_access_token(identity=un)
            # return jsonify({'token': access_token}, 200)

        get_db().close()

        return make_response(f'could not verify. stored: "{respw}"  typed: "{hpw}"',  401, {'Authentication': '"login required"'})

class Logout(Resource):
    def delete(self):
        parser.add_argument('username')
        data = parser.parse_args()
        un = data['username']

        res = get_db().cursor().execute(f'SELECT id FROM users WHERE username = "{un}"').fetchone()
        validToken = get_db().cursor().execute(f'SELECT tokenid FROM token WHERE id = {res[0]}').fetchone()
        if validToken:
            get_db().cursor().execute(f'DELETE FROM token WHERE id = {res[0]}')
            get_db().commit()
            return jsonify({'message': 'You successfully logged out'}, 201)
        get_db().close()

        return make_response(f'was not able to log you out with id: "{res[0]}"', 400, {'info': '"you might have log out already"'})

class Token(Resource):
    def get(self):
        result = get_db().cursor().execute('SELECT * FROM token')
        rows = result.fetchall()
        get_db().close()
        response = []
        for row in rows:
            response.append(dict(zip([c[0] for c in result.description], row)))
        return response


