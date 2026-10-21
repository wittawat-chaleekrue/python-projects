# ==========================================================
# โปรแกรมคำนวณเกรดเฉลี่ย (GPA Calculator)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter
# ==========================================================

import tkinter as tk      # เครื่องมือสร้างหน้าต่างโปรแกรม (GUI)

# ---------- ข้อมูลตั้งต้น ----------

GRADES = ["4", "3.5", "3", "2.5", "2", "1.5", "1", "0"]   # เกรดที่เลือกได้
CREDITS = ["0.5", "1", "1.5", "2", "3"]                     # หน่วยกิตที่เลือกได้

# เก็บทุกวิชาที่เพิ่มเข้ามา แต่ละวิชาเป็น (ชื่อวิชา, หน่วยกิต, เกรด)
subjects = []


# ---------- ส่วนที่ 1: ตรรกะ (สมองของโปรแกรม) ----------

def calculate_gpa(subject_list):
    """GPA = ผลรวม(หน่วยกิต x เกรด) ÷ ผลรวมหน่วยกิต"""
    total_points = 0
    total_credits = 0
    for name, credit, grade in subject_list:
        total_points = total_points + credit * grade
        total_credits = total_credits + credit
    if total_credits == 0:          # ยังไม่มีวิชา ห้ามหารด้วย 0
        return 0
    return total_points / total_credits


# ---------- ส่วนที่ 2: ฟังก์ชันที่ทำงานเมื่อผู้ใช้กดปุ่ม ----------

def refresh_screen():
    """วาดรายการวิชาในกล่องใหม่ทั้งหมด แล้วคำนวณ GPA ใหม่"""
    subject_listbox.delete(0, tk.END)
    for name, credit, grade in subjects:
        subject_listbox.insert(tk.END, f"{name}   |   {credit} หน่วยกิต   |   เกรด {grade}")

    gpa = calculate_gpa(subjects)
    gpa_label.config(text=f"GPA = {gpa:.2f}")


def on_add(event=None):
    """กดปุ่ม 'เพิ่มวิชา'"""
    name = name_entry.get().strip()
    if name == "":
        message_label.config(text="กรุณาพิมพ์ชื่อวิชาก่อน", fg="red")
        return

    credit = float(credit_var.get())
    grade = float(grade_var.get())
    subjects.append((name, credit, grade))

    name_entry.delete(0, tk.END)
    message_label.config(text=f"เพิ่มวิชา {name} แล้ว ✔", fg="green")
    refresh_screen()


def on_delete():
    """ลบวิชาที่คลิกเลือกไว้ในรายการ"""
    selected = subject_listbox.curselection()
    if len(selected) == 0:
        message_label.config(text="คลิกเลือกวิชาที่จะลบก่อน", fg="red")
        return
    index = selected[0]
    removed = subjects.pop(index)
    message_label.config(text=f"ลบวิชา {removed[0]} แล้ว", fg="black")
    refresh_screen()


# ---------- ส่วนที่ 3: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("คำนวณเกรดเฉลี่ย GPA")
root.geometry("460x520")
root.resizable(False, False)

tk.Label(root, text="🎓 คำนวณเกรดเฉลี่ย GPA",
         font=("Helvetica", 18, "bold")).pack(pady=15)

# แถวกรอกข้อมูล: ชื่อวิชา / หน่วยกิต / เกรด
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

tk.Label(input_frame, text="ชื่อวิชา").grid(row=0, column=0)
tk.Label(input_frame, text="หน่วยกิต").grid(row=0, column=1)
tk.Label(input_frame, text="เกรด").grid(row=0, column=2)

name_entry = tk.Entry(input_frame, width=16)
name_entry.grid(row=1, column=0, padx=5)

credit_var = tk.StringVar(value="1")
tk.OptionMenu(input_frame, credit_var, *CREDITS).grid(row=1, column=1, padx=5)

grade_var = tk.StringVar(value="4")
tk.OptionMenu(input_frame, grade_var, *GRADES).grid(row=1, column=2, padx=5)

tk.Button(root, text="เพิ่มวิชา", command=on_add).pack(pady=8)

message_label = tk.Label(root, text="")
message_label.pack()

subject_listbox = tk.Listbox(root, width=45, height=10)
subject_listbox.pack(pady=5)

tk.Button(root, text="ลบวิชาที่เลือก", command=on_delete).pack(pady=5)

gpa_label = tk.Label(root, text="GPA = 0.00", font=("Helvetica", 20, "bold"), fg="blue")
gpa_label.pack(pady=10)

root.bind("<Return>", on_add)    # กด Enter = เพิ่มวิชา
name_entry.focus()

root.mainloop()
