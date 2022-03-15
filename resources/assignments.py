
from datetime import date
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, make_response, request
from src.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

parser = reqparse.RequestParser()


class Assignments(Resource):

    def get(self):

        try:

            # TODO: check against user who is logged in. Show them only their assignments. 
            # get current logged in users token
            # curUser = get_db().cursor().execute(f'SELECT id FROM token WHERE tokenid = "{loggedTokenid}"')
            # curStaff = get_db().cursor().execute(f'SELECT staffid FROM staff WHERE id = "{curUser}"')
            # result = get_db().cursor().execute(f'SELECT * FROM assignments WHERE staffid = "{curStaff}"')

            #remove this line once above is implemented.
            result = get_db().cursor().execute(f'SELECT * FROM assignments')
            #remove this line once above is implemented.

            rows = result.fetchall()
            get_db().close()
            response = []
            for row in rows:
                response.append(dict(zip([c[0] for c in result.description], row)))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            message = jsonify(error = 'Something went wrong when getting your assignments. Please try again.')
            return make_response(message, 500)


    def post(self):

        try:
            parser.add_argument('staffid')
            parser.add_argument('taskid')
            parser.add_argument('roomno')
            data = parser.parse_args()
            staffid = data['staffid'] 
            roomno = data['roomno'] 
            taskid = data['taskid']
            if not get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid = "{staffid}"').fetchone():
                message = jsonify(error = 'Staff member of that id does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = "{roomno}"').fetchone():
                message = jsonify(error = 'Room of that number does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = "{taskid}"').fetchone():
                message = jsonify(error = 'Task of that id does not exist.')
                return make_response(message, 404)
            get_db().cursor().execute(f'INSERT INTO assignments(staffid, roomid, taskid) VALUES({staffid}, "{roomno}", "{taskid}")')
            get_db().commit()
            get_db().close()
            message = jsonify(message = 'Assignment successfully added.')
            return make_response(message, 200)            

        except:

            message = jsonify(error = 'Something went wrong when creating the assignment. Please try again.')
            return make_response(message, 500)


class Assignment(Resource):

    def get(self, assignid):

        try:

            if not get_db().cursor().execute(f'SELECT * FROM assignments WHERE id = {assignid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified assignment.')
                return make_response(message, 404)

            result = get_db().cursor().execute(f'SELECT * FROM assignments WHERE id = {assignid}')
            row = result.fetchone()
            get_db().close()
            response = dict(zip([c[0] for c in result.description], row))
            response = jsonify(response)
            return make_response(response, 200)

        except:
            message = jsonify(error = 'Something went wrong when getting the specified assignment. Please try again.')
            return make_response(message, 500)


    # def put(self, taskid):

    #     try:
    #         #nothing yet
    #     except:
    #         message = jsonify(error = 'Something went wrong when editing the assignment. Please try again.')
    #         return make_response(message, 500)
    

    # def delete(self, taskid):

    #     try:
    #         #nothing yet
    #     except:
    #         message = jsonify(error = 'Something went wrong when deleting the assignment. Please try again.')
    #         return make_response(message, 500)
