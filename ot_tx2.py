import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager - MySQL")
        self.root.geometry("700x500")

        self.connect_mysql()
        self.create_table()
        self.build_ui()

    # ==============================
    # KẾT NỐI MYSQL
    # ==============================
    def connect_mysql(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # đổi nếu cần
                password="123456",  # đổi nếu cần
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS studentsdb")
            self.cursor.execute("USE studentsdb")
        except Exception as e:
            messagebox.showerror("Lỗi MySQL", str(e))

    # ==============================
    # TẠO BẢNG
    # ==============================
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            age INT,
            major VARCHAR(255)
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    # ==============================
    # GIAO DIỆN
    # ==============================
    def build_ui(self):
        form = ttk.LabelFrame(self.root, text="Nhập thông tin")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Tên: ").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(form, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Tuổi: ").grid(row=1, column=0, padx=5, pady=5)
        self.entry_age = ttk.Entry(form, width=30)
        self.entry_age.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Ngành học: ").grid(row=2, column=0, padx=5, pady=5)
        self.entry_major = ttk.Entry(form, width=30)
        self.entry_major.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Thêm sinh viên", width=18, command=self.add_student).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Hiển thị tất cả", width=18, command=self.get_students).grid(row=0, column=1,
                                                                                                padx=10)
        ttk.Button(btn_frame, text="Tìm theo ngành", width=18, command=self.search_students).grid(row=0, column=2,
                                                                                                  padx=10)
        ttk.Button(btn_frame, text="XÓA sinh viên", width=18, command=self.delete_student).grid(row=1, column=1,
                                                                                                pady=10)
        ttk.Button(btn_frame, text="Tuổi > 20", width=18, command=self.search_age_over_20).grid(row=1, column=2,
                                                                                                padx=10)

        # Bảng hiển thị
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "age", "major"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Tên")
        self.tree.heading("age", text="Tuổi")
        self.tree.heading("major", text="Ngành")

        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ==============================
    # HÀM THÊM SINH VIÊN
    # ==============================

    def add_student(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        major = self.entry_major.get().strip()

        if not name or not age or not major:
            messagebox.showwarning("Thiếu dữ liệu", "Hãy nhập đủ thông tin")
            return

        try:
            query = "INSERT INTO students(name, age, major) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (name, age, major))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm sinh viên!")
            self.get_students()
        except Exception as e:
            messagebox.showerror("Lỗi MySQL", str(e))

        self.clear()

    # ==============================
    # HIỂN THỊ TẤT CẢ SINH VIÊN
    # ==============================
    def get_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM students")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    # ==============================
    # TÌM THEO NGÀNH
    # ==============================
    def search_students(self):
        major = self.entry_major.get().strip()
        if not major:
            messagebox.showwarning("Thông báo", "Hãy nhập ngành học!")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM students WHERE major LIKE %s"
        self.cursor.execute(query, ("%" + major + "%",))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

        self.clear()

    # ==============================
    # XÓA SINH VIÊN
    # ==============================
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Hãy chọn sinh viên để xóa!")
            return

        item = self.tree.item(selected[0])
        student_id = item["values"][0]

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa ID {student_id}?")
        if confirm:
            query = "DELETE FROM students WHERE id = %s"
            self.cursor.execute(query, (student_id,))
            self.conn.commit()
            messagebox.showinfo("Đã xóa", "Sinh viên đã bị xóa.")
            self.get_students()

    # ==============================
    # TÌM SINH VIÊN CÓ TUỔI > 20
    # ==============================
    def search_age_over_20(self):
        # Xóa ô nhập
        self.clear()

        # Xóa bảng
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = "SELECT * FROM students WHERE age > 20"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Lỗi MySQL", str(e))

    def clear(self):
        self.entry_name.delete(0, "end")
        self.entry_age.delete(0, "end")
        self.entry_major.delete(0, "end")


# ==============================
# CHẠY CHƯƠNG TRÌNH
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
