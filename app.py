from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build REST API", "done": False}
]

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Tasks API. Use /tasks to interact."})

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# GET a single task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# POST a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        "id": tasks[-1]['id'] + 1 if tasks else 1,
        "title": data.get('title', ''),
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# PUT (update) an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)

# DELETE a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(debug=True)
