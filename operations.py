
from datetime import datetime, timedelta#store the points in
point = {
    
        "Morning": 0,
        "Afternoon": 0,
        "Evening": 0
         
    }


taskList = []

def DetermineType():
   
   #by default the first one
    first_key = list(point.keys())[0]
    first_value = point[first_key]

    userType = {first_key: first_value}

    for i in point:
        if(point[i]) > list(userType.values())[0]:
            userType =  {i: point[i]}


    #key = list(userType.keys())[0]
    return list(userType.keys())[0]



def addPoints(data):
    for i in range(len(data)):
        if data[i].lower() == "morning":
            point["Morning"] =  point["Morning"] + 1
        elif data[i].lower() == "afternoon":
            point["Afternoon"] =  point["Afternoon"] + 1
        elif data[i].lower() == "evening":
            point["Evening"] =  point["Evening"] + 1
        else:
            pass # do nothing




def getType(personPoints, position):

    newDict = point
    sorted(newDict)

    return list(personPoints.keys())[position]
    


def schedule_tasks(tasks, productivity_time):
    # Define time slots for morning, afternoon, and night
    time_slots = {
        "Morning": (7, 10),
        "Afternoon": (12, 15),
        "Evening": (20, 24),
    }
    
    # Initialize start time for the productivity time
    start_time = datetime.now().replace(hour=time_slots[productivity_time][0], minute=0, second=0)
    
    scheduled_tasks = []

    for task in tasks:
        category = task['category']
        if category == 'work/study':
            # Work/study tasks follow the Pomodoro technique
            task_duration = 50  # 40 minutes work + 10 minutes break
        elif category == 'leisure':
            # Leisure tasks are allocated 1 hour each
            task_duration = 60
        else:
            # Other categories can have a default duration (e.g., 40 minutes)
            task_duration = 60*7

        end_time = start_time + timedelta(minutes=task_duration)
        
        # Format the start and end times as HH:MM:SS
        start_time_str = start_time.strftime("%H:%M:%S")
        end_time_str = end_time.strftime("%H:%M:%S")
        
        scheduled_task = {
            "Task": task["task"],
            "Start Time": start_time_str,
            "End Time": end_time_str
        }
        
        scheduled_tasks.append(scheduled_task)
        
        # Update the start time for the next task
        start_time = end_time
    
    return scheduled_tasks

# Example usage:
personPoints = {
    "Morning": 3,
    "Afternoon": 2,
    "Evening": 1
}

most_productive_time = getType(personPoints, 0)  # Get the most productive time
second_most_productive_time = getType(personPoints, 1)  # Get the 2nd most productive time
third_most_productive_time = getType(personPoints, 2)  # Get the 3rd most productive time (resting)

tasks = [
    {'task': 'sdsd', 'category': 'work/study'},
    {'task': 'adad', 'category': 'work/study'},
    {'task': 'work on Assignment2', 'category': 'work/study'},
    {'task': 'hang out', 'category': 'leisure'},
    {'task': 'sleep', 'category': 'sleep'},
]

most_productive_tasks = [task for task in tasks if task['category'] == 'work/study']
second_most_productive_tasks = [task for task in tasks if task['category'] == 'leisure']
third_most_productive_tasks = [task for task in tasks if task['category'] == 'sleep']

scheduled_most_productive_tasks = schedule_tasks(most_productive_tasks, most_productive_time)
scheduled_second_most_productive_tasks = schedule_tasks(second_most_productive_tasks, second_most_productive_time)
scheduled_third_most_productive_tasks = schedule_tasks(third_most_productive_tasks, third_most_productive_time)

for task in scheduled_most_productive_tasks:
    print(f"Task: {task['Task']}")
    print(f"Start Time: {task['Start Time']}")
    print(f"End Time: {task['End Time']}")
    print()

for task in scheduled_second_most_productive_tasks:
    print(f"Task: {task['Task']}")
    print(f"Start Time: {task['Start Time']}")
    print(f"End Time: {task['End Time']}")
    print()

for task in scheduled_third_most_productive_tasks:
    print(f"Task: {task['Task']}")
    print(f"Start Time: {task['Start Time']}")
    print(f"End Time: {task['End Time']}")
    print()