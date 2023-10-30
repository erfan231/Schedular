from flask import Flask, render_template, request, redirect, url_for, flash
import json
from operations import addPoints, DetermineType, point, taskList, getType, schedule_tasks

app = Flask(__name__)
app.secret_key = "SECRET_KEY"



# Load questions from the JSON file
with open("Dataset.json", encoding="utf8", mode= "r") as json_file:
    questions = json.load(json_file)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process user's selected answer for the current question
        current_question_index = request.form["current_question"]
        print("current" + current_question_index)

        user_answer = request.form.get("user_answer")  # Use request.form.get to safely retrieve the answer

        # Check if the user_answer is provided
        if user_answer is None:
            # Display a message to provide an answer and redirect back to the current question
            flash("Please provide an answer.")
            return redirect(url_for("question", index=current_question_index))

        dictvalue = eval(user_answer)
        # print the answer value
        print(f"User selected answer for question {dictvalue['text']}")

        #  ADD THE POINTS
        addPoints(dictvalue["code"])
        print(point)

        # Check if there are more questions or redirect to a completion page
        if int(current_question_index) < len(questions["questions"]) - 1:
            next_question_index = int(current_question_index) + 1
            return redirect(url_for("question", index=next_question_index))
        else:
            # THE LOGIC FOR DETERMINING THE USER TYPE
            return redirect(url_for("todo"))

    return redirect(url_for("question", index=0))

@app.route("/question/<int:index>", methods=["GET", "POST"])
def question(index):
    if index < 0 or index >= len(questions["questions"]):
        return "Invalid question index"

    question_data = questions["questions"][index]
    return render_template("home.html", question=question_data, current_index=index)


@app.route("/todolist", methods=["GET", "POST"])
def todo():
    return render_template("todo.html")



@app.route("/tasks", methods=["GET", "POST"])
def tasks():

    print(taskList)
    return render_template("todo.html", tasks=taskList)



@app.route("/save", methods=["GET", "POST"])
def save():
    #save the tasks to a file, db, etc
    #not doing it here - to keep it simple

    
    
    if request.method == "POST":
        task_name = request.form['new-task']
        task_category = request.form['task-category']

        task = {
        "task": task_name,
        "category":task_category   
        } # Dictionary to store the tasks


        print("Task name is {}", task_name)
        print("task category is {}", task_category)


        #if there is a taks
        if task_name:
            taskList.append(task) # add to the list
            print(len(taskList))

    return redirect(url_for("tasks"))



@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    most_productive_time = getType(point, 0)  # Get the most productive time
    second_most_productive_time = getType(point, 1)  # Get the 2nd most productive time
    third_most_productive_time = getType(point, 2)  # Get the 3rd most productive time (resting)

    most_productive_tasks = [task for task in taskList if task['category'] == 'work/study']
    second_most_productive_tasks = [task for task in taskList if task['category'] == 'leisure']
    third_most_productive_tasks = [task for task in taskList if task['category'] == 'sleep']

    scheduled_most_productive_tasks = schedule_tasks(most_productive_tasks, most_productive_time)
    scheduled_second_most_productive_tasks = schedule_tasks(second_most_productive_tasks, second_most_productive_time)
    scheduled_third_most_productive_tasks = schedule_tasks(third_most_productive_tasks, third_most_productive_time)

    print(taskList)
    print(most_productive_tasks)
    return render_template("tasks.html",
                       most_productive_tasks=scheduled_most_productive_tasks,
                       second_most_productive_tasks=scheduled_second_most_productive_tasks,
                       third_most_productive_tasks=scheduled_third_most_productive_tasks)

if __name__ == "__main__":
    app.run(debug=True)
