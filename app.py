import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tasks = [
    {
        "id": 0,
        "task": "Send Email",
        "status": "Undone",
        "responsible": "Jorge"
    }
]

class Tasks(Resource):
    def get(self, id):
        try:
            response = {"status": "OK", "message": tasks[id]}
            return response
        except IndexError:
            response = {"status": "ERROR", "message": "No task found with the ID {}".format(id)}
            return response
        except Exception as e:
            response = {"status": "ERROR", "message": "An unknown error occurred. Please try again."}
            print("Exception: {}".format(e))
            return response
    def put(self, id):
        try:
            data = json.loads(request.data)
            if "status" in data and data["status"] != tasks[id]["status"]:
                tasks[id]["status"] = data["status"]
                response = {"status": "OK", "message": tasks[id]}
                return response
            else:
                response = {"status": "ERROR", "message": "No change in key \"status\" found."}
                return response
        except IndexError:
            response = {"status": "ERROR", "message": "No task found with the ID {}".format(id)}
            return response
        except Exception as e:
            response = {"status": "ERROR", "message": "An unknown error occurred. Please try again."}
            print("Exception: {}".format(e))
            return response
    def delete(self, id):
        try:
            tasks.pop(id)
            response = {"status": "OK", "message": "Task deleted."}
            return response
        except IndexError:
            response = {"status": "ERROR", "message": "No task found with the ID {}".format(id)}
            return response
        except Exception as e:
            response = {"status": "ERROR", "message": "An unknown error occurred. Please try again."}
            print("Exception: {}".format(e))
            return response

class TasksList(Resource):
    def get(self):
        try:
            response = {"status": "OK", "message": tasks}
            return response
        except Exception as e:
            response = {"status": "ERROR", "message": "An unknown error occurred. Please try again."}
            print("Exception: {}".format(e))
            return response
    def post(self):
        try:
            id = len(tasks)
            data = json.loads(request.data)
            data["id"] = id
            tasks.append(data)
            response = {"status": "OK", "message": data}
            return response
        except Exception as e:
            response = {"status": "ERROR", "message": "An unknown error occurred. Please try again."}
            print("Exception: {}".format(e))
            return response

api.add_resource(Tasks, '/task/<int:id>')
api.add_resource(TasksList, '/task')

if __name__ == '__main__':
    app.run(debug=True)