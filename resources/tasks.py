# Arica: This file contains the resources for the /tasks and /tasks/<taskid> endpoints.
# Sources I used:
# https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
# https://pythonexamples.org/python-tuple-to-string/

from datetime import date
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, make_response, request
from src.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

parser = reqparse.RequestParser()


# Arica: 
# TODO: Will want to make some (or all) of these endpoints protected
# so that only staff members who are logged in can view and edit the tasks.
# The last step would be to add roles so that all nurses can perform GET
# requests, but only the head nurse can perform POST, PUT, and DELETE requests.


# Arica: This resource is for all the tasks.

class Tasks(Resource):

    def get(self):

        try:

            # Arica: Returns a list of all the tasks and the HTTP code 200 OK.            
            result = get_db().cursor().execute('SELECT * FROM tasks')
            rows = result.fetchall()
            get_db().close()
            response = []
            for row in rows:
                response.append(dict(zip([c[0] for c in result.description], row)))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            # Arica: Returns an error message for any problems that occurred during the GET all tasks process.
            message = jsonify(error = 'Something went wrong when getting all the tasks. Please try again.')
            return make_response(message, 500)


    def post(self):

        try:

            # Arica: The Task Name is the only field the user would provide since the Task ID is autoincremented.
            parser.add_argument('taskname')
            data = parser.parse_args()
            taskname = data['taskname']     

            # Arica: Checks to see if a task name was provided.
            if not data['taskname']:
                message = jsonify(error = 'The task name is required to add a new task. Please add a task name.')
                return make_response(message, 400)

            # Arica: Checks to see if the task the client wants to add already exists.
            # I have been debating about whether this should be included or not. On the one hand, this could prevent
            # inserting multiples of the same task, particularly since I did not set a UNIQUE constraint on the
            # Task Name field when setting up the Tasks table. On the other hand, if the user runs a PUT request, 
            # there is currently nothing to stop them from editing the task to be exactly the same as another one. 
            # I chose to leave this section of code for now and see what the group thinks.
            if get_db().cursor().execute(f'SELECT taskid FROM tasks WHERE taskname = "{taskname}"').fetchone():
                get_db().close()
                message = jsonify(error = f'The task \'{taskname}\' already exists. Please add a different task.')
                return make_response(message, 400)

            # Arica: Adds the task to the database and returns the HTTP code 201 Created. 
            # Note that the Task ID is not needed because it is autoincremented.
            get_db().cursor().execute(f'INSERT INTO tasks(taskname) VALUES("{taskname}")')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The task \'{taskname}\' has been successfully added.')
            return make_response(message, 201)
        
        except:

            # Arica: Returns an error message for any problems that occurred during the POST one task process.
            message = jsonify(error = 'Something went wrong when adding the task. Please try again.')
            return make_response(message, 500)


# Arica: This resource is for one task.

class Task(Resource):

    def get(self, taskid):

        try:

            # Arica: Checks to see if the provided Task ID matches an existing task in the Tasks table.
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = {taskid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified task. Please check if the Task ID is typed correctly.')
                return make_response(message, 404)

            # Arica: Returns the specified tasks and the HTTP code 200 OK.
            result = get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = {taskid}')
            row = result.fetchone()
            get_db().close()
            response = dict(zip([c[0] for c in result.description], row))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            # Arica: Returns an error message for any problems that occurred during the GET one task process.
            message = jsonify(error = 'Something went wrong when getting the specified task. Please try again.')
            return make_response(message, 500)


    def put(self, taskid):

        try:

            # Arica: The Task Name is the only field the user would provide since the id is autoincremented.
            parser.add_argument('taskname')
            data = parser.parse_args()
            taskname = data['taskname'] 

            # Arica: Checks to see if a Task Name was provided.
            if not data['taskname']:
                message = jsonify(error = 'The task name is required to update a task. Please add a task name.')
                return make_response(message, 400)

            # Arica: Checks to see if the provided Task ID matches an existing task in the Tasks table.
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = {taskid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified task. Please check if the Task ID is typed correctly.')
                return make_response(message, 404)      

            # Arica: I thought about testing to see if the original task name and the new provided task name match,
            # but I thought it might not be needed. Do I care if the user wants to update the name to exactly what 
            # it was before? Maybe not. It might be odd, but it is probably not harmful. 
            # As long as a valid task name is provided, which I tested for above, it should be okay.

            # Arica: Updates the Task Name of the task that matches the provided Task ID and returns the HTTP code 200 OK.
            get_db().cursor().execute(f'UPDATE tasks SET taskname = "{taskname}" WHERE taskid = {taskid}')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The task \'{taskname}\' has been successfully updated.')
            return make_response(message, 200)

        except:

            # Arica: Returns an error message for any problems that occurred during the PUT one task process.
            message = jsonify(error = 'Something went wrong when editing the task. Please try again.')
            return make_response(message, 500)
    

    def delete(self, taskid):

        try:

            # Arica: Checks to see if the provided Task ID matches an existing task in the Tasks table.
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = {taskid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified task. Please check if the Task ID is typed correctly.')
                return make_response(message, 404)

            # Arica: Deletes the task that matches the provided Task ID and returns the HTTP code 200 OK.
            # The following two lines of code are to save the Task Name from the database and then convert that result's tuple into a string,
            # so that when the task is deleted, the return message displays the name of the task for clarity to the user.
            taskname = get_db().cursor().execute(f'SELECT taskname FROM tasks WHERE taskid = {taskid}').fetchone()
            taskname = ''.join(taskname)
            get_db().cursor().execute(f'DELETE FROM tasks WHERE taskid = {taskid}')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The task \'{taskname}\' has been successfully deleted.')
            return make_response(message, 200)       

        except:

            # Arica: Returns an error message for any problems that occurred during the DELETE one task process.
            message = jsonify(error = 'Something went wrong when deleting the task. Please try again.')
            return make_response(message, 500)
