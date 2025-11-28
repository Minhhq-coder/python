from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox

# --- Kết nối MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["TaskManager"]
task = db["Tasks"]

def add():
    if name.get().strip() == "" or des.get().strip() == "":
        messagebox.showerror("Error", "Please fill in all fields")
        return
    try:
        task_data = {
            "name": name.get().strip(),
            "description": des.get().strip(),
            "status": status.get()
        }
        task.insert_one(task_data)
        messagebox.showinfo("Success", "Task added successfully!")
        clear_entries()
        display()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a task to update")
        return
    try:
        n = name.get().strip()
        result = task.update_one(
            {"name": n},
            {"$set": {
                "description": des.get().strip(),
                "status": status.get()
            }}
        )
        if result.matched_count == 0:
            messagebox.showwarning("Warning", "Task not found!")
        else:
            messagebox.showinfo("Success", "Task updated successfully!")
            clear_entries()
            display()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a task to delete")
        return
    try:
        n = name.get().strip()
        result = task.delete_one({"name": n})
        if result.deleted_count == 0:
            messagebox.showwarning("Warning", "Task not found!")
        else:
            messagebox.showinfo("Success", "Task deleted successfully!")
            clear_entries()
            display()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display():
    listbox.delete(0, tk.END)
    all_tasks = task.find()
    for t in all_tasks:
        name_val = t.get('name', 'N/A')
        des_val = t.get('description', 'N/A')
        status_val = t.get('status', 'N/A')
        listbox.insert(tk.END, f"Name: {name_val}, Description: {des_val}, Status: {status_val}")

def on_select(event):
    selection = listbox.curselection()
    if not selection:
        return
    index = selection[0]
    selected_task = listbox.get(index)
    parts = selected_task.split(", ")
    name.set(parts[0].split(": ")[1])
    des.set(parts[1].split(": ")[1])
    status.set(parts[2].split(": ")[1])

def clear_entries():
    name.set("")
    des.set("")
    status.set("Chưa hoàn thành")

root = tk.Tk()
root.geometry("550x550")
root.title("Task Manager")

name = tk.StringVar()
des = tk.StringVar()
status = tk.StringVar(value="Chưa hoàn thành")
options = ["Chưa hoàn thành", "Hoàn thành"]

tk.Label(root, text="Task Manager", font=("Arial", 20), width=30).grid(row=0, column=0, columnspan=4, pady=10)
tk.Label(root, text="Task Name:", font=("Arial", 14)).grid(row=1, column=0, pady=5)
tk.Entry(root, textvariable=name, width=30).grid(row=1, column=1)
tk.Label(root, text="Task Des:", font=("Arial", 14)).grid(row=2, column=0, pady=5)
tk.Entry(root, textvariable=des, width=30).grid(row=2, column=1)
tk.Label(root, text="Task Status:", font=("Arial", 14)).grid(row=3, column=0, pady=5)
tk.OptionMenu(root, status, *options).grid(row=3, column=1, sticky="w")

button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=4, pady=10)
tk.Button(button_frame, text="Add Task", font=("Arial", 10), width=12, command=add).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Task", font=("Arial", 10), width=12, command=update).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Task", font=("Arial", 10), width=12, command=delete).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Display Task", font=("Arial", 10), width=12, command=display).grid(row=0, column=3, padx=5)

listbox = tk.Listbox(root, width=70, height=20)
listbox.grid(row=5, column=0, columnspan=4, pady=10)
listbox.bind("<<ListboxSelect>>", on_select)

display()
root.mainloop()
