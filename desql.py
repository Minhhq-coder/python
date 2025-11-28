import mysql.connector
import tkinter as tk
from tkinter import messagebox

# --- Kết nối MySQL ---
# Thay thông tin user, password, host, database phù hợp
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="taskmanager"
)
cursor = conn.cursor()

# Tạo database nếu chưa tồn tại (chỉ chạy lần đầu)
cursor.execute("CREATE DATABASE IF NOT EXISTS taskmanager")
conn.database = "taskmanager"

# Tạo bảng nếu chưa tồn tại
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description VARCHAR(255),
    status VARCHAR(50)
)
""")
conn.commit()

# --- Hàm thêm task ---
def add():
    if name.get().strip() == "" or des.get().strip() == "":
        messagebox.showerror("Error", "Please fill in all fields")
        return
    try:
        cursor.execute(
            "INSERT INTO Tasks (name, description, status) VALUES (%s, %s, %s)",
            (name.get().strip(), des.get().strip(), status.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "Task added successfully!")
        clear_entries()
        display()
    except mysql.connector.errors.IntegrityError:
        messagebox.showwarning("Warning", "Task with this name already exists!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Hàm cập nhật task ---
def update():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a task to update")
        return
    try:
        n = name.get().strip()
        cursor.execute(
            "UPDATE Tasks SET description=%s, status=%s WHERE name=%s",
            (des.get().strip(), status.get(), n)
        )
        if cursor.rowcount == 0:
            messagebox.showwarning("Warning", "Task not found!")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Task updated successfully!")
            clear_entries()
            display()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Hàm xóa task ---
def delete():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a task to delete")
        return
    try:
        n = name.get().strip()
        cursor.execute("DELETE FROM Tasks WHERE name=%s", (n,))
        if cursor.rowcount == 0:
            messagebox.showwarning("Warning", "Task not found!")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Task deleted successfully!")
            clear_entries()
            display()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Hiển thị task ---
def display():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT name, description, status FROM Tasks")
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"Name: {row[0]}, Description: {row[1]}, Status: {row[2]}")

# --- Khi chọn task từ listbox ---
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

# --- Xóa dữ liệu trong entry ---
def clear_entries():
    name.set("")
    des.set("")
    status.set("Chưa hoàn thành")

# --- GUI ---
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
