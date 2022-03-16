
from datetime import date
import json
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
            parser.add_argument('roomnumber')
            parser.add_argument('status')

            data = parser.parse_args()
            staffid = data['staffid'] 
            roomno = data['roomnumber'] 
            taskid = data['taskid']
            st = data['status']
            if not get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid = "{staffid}"').fetchone():
                message = jsonify(error = 'Staff member of that id does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = "{roomno}"').fetchone():
                message = jsonify(error = 'Room of that number does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = "{taskid}"').fetchone():
                message = jsonify(error = 'Task of that id does not exist.')
                return make_response(message, 404)
            if not st:
                message = jsonify(error = 'Please the status of your assignment')
                return make_response(message, 404)

            get_db().cursor().execute(f'INSERT INTO assignments(staffid, roomnumber, taskid, iscompleted) VALUES({staffid}, "{roomno}", {taskid}, {st})')
            get_db().commit()
            get_db().close()
            message = jsonify(message = 'Assignment successfully added.')
            return make_response(message, 200) 
        except:
            message = jsonify(error = 'Something went wrong when creating the assignment. Please try again later.')
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


    def put(self, assignid):

        try:
            parser.add_argument('staffid')
            parser.add_argument('roomnumber')
            parser.add_argument('taskid')
            parser.add_argument('status')
            data = parser.parse_args()
            stid = data['staffid']
            rmid = data['roomnumber']
            tkid = data['taskid']
            st = data['status']

            if stid:
                stidd = get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid={stid}').fetchone()
                if not stidd[0]:
                    message = jsonify(error = 'staff does not exist. Please provide a valid staff id.')
                    return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET staffid={stid} WHERE id={assignid}')
                get_db().commit()

            if rmid:
                rmidd = get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber= "{rmid}"').fetchone()
                if not rmidd[0]:
                    message = jsonify(error = 'Room does not exist. Please provide a valid Room id.')
                    return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET roomnumber={rmid} WHERE id={assignid}')
                get_db().commit()
            
            if tkid:
                tkidd = get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid={tkid}').fetchone()
                if not tkidd[0]:
                    message = jsonify(error = 'Task does not exist. Please provide a valid Task id.')
                    return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET taskid={tkid} WHERE id={assignid}')
                get_db().commit()

            if st:
                get_db().cursor().execute(f'UPDATE assignments SET iscompleted={st} WHERE id={assignid}')
                get_db().commit()

            result = get_db().cursor().execute(f'SELECT * FROM assignments WHERE id={assignid}')
            row = result.fetchone()
            return dict(zip([c[0] for c in result.description], row))
        except:
            message = jsonify(error = 'Something went wrong when creating the assignment. Please try again later.')
            return make_response(message, 500)
    

    def delete(self, assignid):

        try:
            if not get_db().cursor().execute(f'SELECT * FROM assignments WHERE id={assignid}').fetchone():
                get_db().close()
                message = jsonify(error = 'The assignment does not exist.')
                return make_response(message, 400)

            get_db().cursor().execute(f'DELETE FROM assignments WHERE id = {assignid}')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The assignment has been successfully deleted.')
            return make_response(message, 200) 
        except:
            message = jsonify(error = 'Something went wrong when deleting the assignment. Please try again.')
            return make_response(message, 500)
