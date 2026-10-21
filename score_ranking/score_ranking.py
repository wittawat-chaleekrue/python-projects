# โปรแกรมจัดอันดับคะแนนนักเรียน (เรียงด้วย Bubble Sort)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: เขียนอัลกอริทึมเรียงข้อมูลเอง ไม่ใช้ sort() สำเร็จรูป

import tkinter as tk
from tkinter import messagebox

students = []   # รายชื่อนักเรียน แต่ละคนเป็น dictionary เช่น {"name": "เอ", "score": 80}


# ---------- ส่วนที่ 1: หัวใจของโปรแกรม (Bubble Sort) ----------

def bubble_sort(data):
    items = data.copy()   # ก๊อปไว้ก่อน จะได้ไม่ยุ่งกับลำดับเดิม
    n = len(items)
    swaps = 0             # นับว่าสลับไปกี่ครั้ง

    for i in range(n - 1):              # ทำทั้งหมด n-1 รอบ
        for j in range(n - 1 - i):      # เทียบคู่ที่อยู่ติดกัน (รอบหลัง ๆ เทียบน้อยลง)
            if items[j]["score"] < items[j + 1]["score"]:
                # ตัวซ้ายน้อยกว่าตัวขวา → สลับ (เพราะเราต้องการมากไปน้อย)
                items[j], items[j + 1] = items[j + 1], items[j]
                swaps = swaps + 1

    return items, swaps


# ---------- ส่วนที่ 2: ฟังก์ชันของปุ่ม ----------

def add_student():
    name = entry_name.get().strip()
    score_text = entry_score.get().strip()

    if name == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อนักเรียน")
        return

    try:
        score = int(score_text)
    except ValueError:
        messagebox.showwarning("แจ้งเตือน", "คะแนนต้องเป็นตัวเลขจำนวนเต็ม เช่น 75")
        return

    if score < 0 or score > 100:
        messagebox.showwarning("แจ้งเตือน", "คะแนนต้องอยู่ระหว่าง 0 ถึง 100")
        return

    students.append({"name": name, "score": score})
    entry_name.delete(0, tk.END)
    entry_score.delete(0, tk.END)
    entry_name.focus()   # ย้ายเคอร์เซอร์กลับไปช่องชื่อ พิมพ์คนต่อไปได้เลย
    show_original()


def show_original():
    # แสดงตามลำดับที่กรอก (ยังไม่เรียง)
    listbox.delete(0, tk.END)
    for student in students:
        listbox.insert(tk.END, f"{student['name']}  |  {student['score']} คะแนน")
    label_info.config(text=f"มีนักเรียน {len(students)} คน (ยังไม่เรียง)")


def show_ranking():
    if len(students) < 2:
        messagebox.showwarning("แจ้งเตือน", "ต้องมีนักเรียนอย่างน้อย 2 คนถึงจะเรียงได้")
        return

    ranked, swaps = bubble_sort(students)

    listbox.delete(0, tk.END)
    rank = 1
    for student in ranked:
        listbox.insert(tk.END, f"อันดับ {rank}  |  {student['name']}  |  {student['score']} คะแนน")
        rank = rank + 1

    label_info.config(text=f"เรียงเสร็จ! Bubble Sort สลับไปทั้งหมด {swaps} ครั้ง")


def clear_all():
    if len(students) == 0:
        return
    sure = messagebox.askyesno("ยืนยัน", "ลบรายชื่อทั้งหมดใช่ไหม?")
    if sure:
        students.clear()
        show_original()


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("จัดอันดับคะแนนนักเรียน")
window.geometry("460x500")

frame_add = tk.LabelFrame(window, text="เพิ่มนักเรียน", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=10)

tk.Label(frame_add, text="ชื่อ").pack(anchor="w")
entry_name = tk.Entry(frame_add)
entry_name.pack(fill="x")

tk.Label(frame_add, text="คะแนน (0-100)").pack(anchor="w")
entry_score = tk.Entry(frame_add)
entry_score.pack(fill="x")

tk.Button(frame_add, text="เพิ่ม", command=add_student).pack(pady=5)

listbox = tk.Listbox(window, height=10, font=("Arial", 14))
listbox.pack(fill="both", expand=True, padx=10)

label_info = tk.Label(window, text="มีนักเรียน 0 คน")
label_info.pack(pady=5)

frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="🏆 จัดอันดับ", command=show_ranking).pack(side="left", padx=5)
tk.Button(frame_buttons, text="ดูลำดับที่กรอก", command=show_original).pack(side="left", padx=5)
tk.Button(frame_buttons, text="ลบทั้งหมด", command=clear_all).pack(side="left", padx=5)

window.mainloop()
