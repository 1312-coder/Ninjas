# Add tasks - The user can add tasks with a title, description,due date, and priority level.
# Edit tasks - The user can modify the details of an existing task.
# Delete tasks - The user can delete a task from the list.
# View tasks - The user can view all tasks or filter tasks based on different criteria 
#              such as due date,priority level, or category.
# Mark tasks as complete - The user can mark a task as complete or pending.
# Save tasks - The application can save tasks to a file or database so that they can be retrieved later.
# Load tasks - The application can load previously saved tasks from a file or database.
# Reminders - The application can send reminders to the user when a task is due.
import json

MAIN_MENU = """
To-Do List Application:
What would you like to do?
1. ADD task
2. Edit task 
3. view task 
4. exit task """

def Load_task():
    try:
        with open('TASK_FILE', 'r') as f:
            todo_list = json.load(f)
    except FileNotFoundError:
        todo_list = []
    return todo_list  

def save_task(todo_list):
    with open("TASK_FILE", "w") as f: 
            json.dump(todo_list, f)   
    print("Task saved successfully!")
             
def add_task(todo_list):
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter task due date(mm-dd-yyyy): ")
    priority = input("Enter task priority(low,medium,high): ")
    task = {"title": title.title(),"description": description.title() ,"due_date": due_date.title() ,"priority": priority.title()}
    todo_list.append(task)
    save_task(todo_list)
    print("Task added successfully!")
  
def edit_task(todo_list):
    task_index = int(input('Enter task index to edit: '))   
    title = input('Enter new task title: ')
    description = input('Enter new task description: ')
    due_date = input('Enter new task due_date(mm-dd-yyyy): ')
    priority = input('Enter new task priority(low,medium,high): ')
    todo_list[task_index]['title'] = title
    todo_list[task_index]['description'] = description
    todo_list[task_index]['due_date'] = due_date
    todo_list[task_index]['priority'] = priority
    save_task(todo_list)
    print('Task edited successfully.')

def display_task(todo_list):
    
    for i, task in enumerate(todo_list): #enumarte ---takes an iterable(a sequence of values) as its argument and returns an iterator that yields pairs of the form (index, value) 
        print(f'{i}. (title: {task["title"]}), (description: {task["description"]}), (due_date: {task["due_date"]}), (priority: {task["priority"]})')

def main():
    todo_list = Load_task()
    while True:
        print(MAIN_MENU)
        choice = int(input("Enter you'r choice(1:4): "))
        if choice == 1:
            add_task(todo_list)    
        elif choice == 2:
            edit_task(todo_list)
        elif choice == 3:
            display_task(todo_list)
        elif choice == 4:
            break         
        else: 
            print("You have to make atleast one choice from above MAIN-MENU")  
        
main()
    
                              
               