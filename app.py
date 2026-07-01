from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tasks = []


class Task:
    def __init__(self, name, urgent, important, priority):
        self.name = name
        self.urgent = urgent
        self.important = important
        self.priority = priority

    def to_dict(self):
        return {
            "name": self.name,
            "urgent": self.urgent,
            "important": self.important,
            "priority": self.priority
        }


def insertion_sort(task_list):
    for i in range(1, len(task_list)):
        key = task_list[i]
        j = i - 1

        while j >= 0 and task_list[j].priority < key.priority:
            task_list[j + 1] = task_list[j]
            j -= 1

        task_list[j + 1] = key

    return task_list


def bucket_tasks(task_list):
    buckets = {
        "bucket1": [],
        "bucket2": [],
        "bucket3": [],
        "bucket4": []
    }

    for task in task_list:
        if task.urgent and task.important:
            buckets["bucket1"].append(task)
        elif not task.urgent and task.important:
            buckets["bucket2"].append(task)
        elif task.urgent and not task.important:
            buckets["bucket3"].append(task)
        else:
            buckets["bucket4"].append(task)

    for bucket in buckets:
        buckets[bucket] = insertion_sort(buckets[bucket])

    return {
        bucket: [task.to_dict() for task in buckets[bucket]]
        for bucket in buckets
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()

    name = data["name"]
    urgent = data["urgent"]
    important = data["important"]
    priority = int(data["priority"])

    new_task = Task(name, urgent, important, priority)
    tasks.append(new_task)

    sorted_buckets = bucket_tasks(tasks)

    return jsonify(sorted_buckets)


@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    return jsonify(bucket_tasks(tasks))


@app.route("/clear_tasks", methods=["POST"])
def clear_tasks():
    tasks.clear()
    return jsonify(bucket_tasks(tasks))


if __name__ == "__main__":
    app.run(debug=True)