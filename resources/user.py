# Arica: I followed this tutorial for comments and error trapping:
# https://dev.to/imdhruv99/flask-user-authentication-with-jwt-2788

from datetime import date
from tkinter import INSERT
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, make_response, request
from src.db import get_db
from werkzeug.security import generate_password_hash,check_password_hash
#from passlib.apps import custom_app_context as pwd_context
#from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

parser = reqparse.RequestParser()

#TODO: Do the User and Users need PUT and DELETE methods?

class User(Resource): 

    def get(self, user_name):

        #TODO: Check for empty input and an input that does not exist. Finalize the error messages.

        result = get_db().cursor().execute(f'SELECT * FROM users WHERE username="{user_name}"')
        row = result.fetchone()
        return dict(zip([c[0] for c in result.description], row))

    def post(self):

        #TODO: This is the signup. Check for empty input, possibly unique values too. Finalize the error messages.

        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('staffname')
        parser.add_argument('phonenumber')
        parser.add_argument('email')
        parser.add_argument('address')
        data = parser.parse_args()
        un = data['username']
        stn = data['staffname']
        phn = data['phonenumber']
        em = data['email']
        ad = data['address']
        #pw = data['password']
        if get_db().cursor().execute(f'SELECT id FROM users WHERE username = "{un}"').fetchone():
            return {'message': f'User {un} already exists'}
        hpw = generate_password_hash(data['password'], method='sha256')
        get_db().cursor().execute(f'INSERT INTO users(id, username, password) VALUES({hash(un)}, "{un}", "{hpw}")')
        get_db().commit()
        loginid = get_db().cursor().execute(f'SELECT id FROM users WHERE username = "{un}"').fetchone()
        get_db().cursor().execute(f'INSERT INTO staff(id, staffname, phonenumber, email, address) VALUES({loginid[0]}, "{stn}" ,"{phn}", "{em}", "{ad}")')
        get_db().commit()
        get_db().close()
        return jsonify({'message': 'successfully signed up'})

class Users(Resource):

    def get(self):
        
        #TODO: Like everything else, use a try-except block for server errors.

        result = get_db().cursor().execute('SELECT * FROM users')
        rows = result.fetchall()
        get_db().close()
        response = []
        for row in rows:
            response.append(dict(zip([c[0] for c in result.description], row)))
        return response


#TODO: Same as everything else. Error trapping, empty input, invalid input, and finalize error messages.

class Staff(Resource): 

    def get(self, staffid):

        result = get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid={staffid}')
        row = result.fetchone()
        return dict(zip([c[0] for c in result.description], row))

    def put(self, staffid):
        parser.add_argument('staffname')
        parser.add_argument('phonenumber')
        parser.add_argument('email')
        parser.add_argument('address')
        data = parser.parse_args()
        stn = data['staffname']
        phn = data['phonenumber']
        em = data['email']
        ad = data['address']
        stname = get_db().cursor().execute(f'SELECT staffname FROM staff WHERE staffid={staffid}').fetchone()
        if not stname[0] == stn and stn:
            get_db().cursor().execute(f'UPDATE staff SET staffname="{stn}" WHERE staffid={staffid}')
            get_db().commit()

        phnumber = get_db().cursor().execute(f'SELECT phonenumber FROM staff WHERE staffid={staffid}').fetchone()
        if not phnumber[0] == phn and phn:
            get_db().cursor().execute(f'UPDATE staff SET phonenumber="{phn}" WHERE staffid={staffid}')
            get_db().commit()

        email = get_db().cursor().execute(f'SELECT email FROM staff WHERE staffid={staffid}').fetchone()
        if not email[0] == em and em:
            get_db().cursor().execute(f'UPDATE staff SET email="{em}" WHERE staffid={staffid}')
            get_db().commit()

        address = get_db().cursor().execute(f'SELECT address FROM staff WHERE staffid={staffid}').fetchone()
        if not address[0] == ad and ad:
            get_db().cursor().execute(f'UPDATE staff SET address="{ad}" WHERE staffid={staffid}')
            get_db().commit()
        result = get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid={staffid}')
        row = result.fetchone()
        return dict(zip([c[0] for c in result.description], row))

    def delete(self, staffid):

        try:
            if not get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid={staffid}').fetchone():
                get_db().close()
                message = jsonify(error = 'This staff member does not exist.')
                return make_response(message, 400)

            get_db().cursor().execute(f'DELETE FROM staff WHERE id = {staffid}')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'Staff has been successfully deleted.')
            return make_response(message, 200) 
        except:
            message = jsonify(error = 'Something went wrong when deleting the staff. Please try again.')
            return make_response(message, 500)

# Arica: It sounds like no POST method is needed here because a staff member is automatically created when going through the signup process (POSTing a User).

class AllStaff(Resource):

    def get(self):
        
        result = get_db().cursor().execute('SELECT * FROM staff')
        rows = result.fetchall()
        get_db().close()
        response = []
        for row in rows:
            response.append(dict(zip([c[0] for c in result.description], row)))
        return response