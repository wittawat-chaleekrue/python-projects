# โปรแกรมเลือกตั้งประธานนักเรียน (ใช้ set กันโหวตซ้ำ + dict นับคะแนน)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: set เก็บรหัสนักเรียนที่โหวตแล้ว (ค่าซ้ำเข้าไม่ได้) / dict นับคะแนนแต่ละเบอร์

import tkinter as tk
from tkinter import messagebox

# รายชื่อผู้สมัคร (ชื่อพรรคสมมติ) ช่องสุดท้ายคือ "งดออกเสียง"
candidates = ["เบอร์ 1 พรรคใส่ใจ", "เบอร์ 2 พรรคก้าวหน้า", "เบอร์ 3 พรรครักษ์โลก", "งดออกเสียง"]
colors = ["#e74c3c", "#3498db", "#2ecc71", "#95a5a6"]   # สีแท่งกราฟของแต่ละช่อง

# dict: ชื่อผู้สมัคร → จำนวนคะแนน (เริ่มที่ 0 ทุกคน)
scores = {}
for name in candidates:
    scores[name] = 0

# set: รหัสนักเรียนที่ใช้สิทธิ์แล้ว (set ไม่เก็บค่าซ้ำ และเช็คว่ามีหรือยังได้เร็วมาก)
voted_ids = set()


# ---------- ส่วนที่ 1: ลงคะแนน ----------

def vote():
    student_id = entry_id.get().strip()
    choice = selected.get()

    # ตรวจที่ 1: รหัสต้องเป็นตัวเลข 5 หลัก
    if len(student_id) != 5 or not student_id.isdigit():
        messagebox.showwarning("แจ้งเตือน", "รหัสนักเรียนต้องเป็นตัวเลข 5 หลัก")
        return

    # ตรวจที่ 2: รหัสนี้โหวตไปแล้วหรือยัง (หัวใจของโปรแกรม)
    if student_id in voted_ids:
        messagebox.showerror("โหวตซ้ำ!", f"รหัส {student_id} ใช้สิทธิ์ไปแล้ว ห้ามโหวตซ้ำ")
        entry_id.delete(0, tk.END)
        return

    # ตรวจที่ 3: ต้องเลือกผู้สมัคร
    if choice == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกผู้สมัคร 1 ช่อง")
        return

    voted_ids.add(student_id)       # จดว่ารหัสนี้ใช้สิทธิ์แล้ว
    scores[choice] = scores[choice] + 1   # บวกคะแนนให้ช่องที่เลือก

    # ล้างหน้าจอให้คนต่อไป (ไม่โชว์ว่าเลือกใคร เพราะเป็นการลงคะแนนลับ)
    entry_id.delete(0, tk.END)
    selected.set("")
    label_count.config(text=f"มาใช้สิทธิ์แล้ว {len(voted_ids)} คน")
    messagebox.showinfo("สำเร็จ", "บันทึกคะแนนเรียบร้อย ขอบคุณที่มาใช้สิทธิ์")


# ---------- ส่วนที่ 2: นับคะแนน + วาดกราฟแท่ง ----------

def count_votes():
    total = len(voted_ids)
    if total == 0:
        messagebox.showwarning("แจ้งเตือน", "ยังไม่มีใครมาใช้สิทธิ์")
        return

    canvas.delete("all")              # ลบกราฟเก่าทิ้งก่อนวาดใหม่
    max_score = max(scores.values())  # คะแนนสูงสุด ใช้กำหนดว่าแท่งสูงสุดสูงเท่าไร
    base_y = 190       # เส้นฐานของกราฟ (ยิ่งค่ามาก ยิ่งอยู่ล่าง)
    max_height = 140   # แท่งที่คะแนนสูงสุดจะสูง 140 จุด
    bar_width = 70

    for i in range(len(candidates)):
        name = candidates[i]
        score = scores[name]
        height = score / max_score * max_height   # เทียบบัญญัติไตรยางศ์
        x = 30 + i * 105                           # แท่งถัดไปขยับขวาทีละ 105 จุด

        canvas.create_rectangle(x, base_y - height, x + bar_width, base_y, fill=colors[i])
        percent = score * 100 / total
        canvas.create_text(x + bar_width / 2, base_y - height - 12,
                           text=f"{score} ({percent:.0f}%)")
        canvas.create_text(x + bar_width / 2, base_y + 20, text=name,
                           width=bar_width + 25, font=("Arial", 10))

    # หาผู้ชนะ (ไม่นับช่องงดออกเสียง) และรองรับกรณีคะแนนเท่ากัน
    best = 0
    winners = []
    for name in candidates[:-1]:      # [:-1] = ทุกตัวยกเว้นตัวสุดท้าย
        if scores[name] > best:
            best = scores[name]
            winners = [name]
        elif scores[name] == best and best > 0:
            winners.append(name)

    if len(winners) == 0:
        label_winner.config(text="ยังไม่มีผู้ชนะ (ทุกคนงดออกเสียง)", fg="gray")
    elif len(winners) == 1:
        label_winner.config(text=f"🏆 ผู้ชนะ: {winners[0]} ({best} คะแนน)", fg="green")
    else:
        label_winner.config(text=f"⚖️ คะแนนเท่ากัน: {', '.join(winners)}", fg="orange")


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("เลือกตั้งประธานนักเรียน")
window.geometry("480x640")

tk.Label(window, text="🗳️ เลือกตั้งประธานนักเรียน", font=("Arial", 20, "bold")).pack(pady=10)

frame_vote = tk.LabelFrame(window, text="ลงคะแนน", padx=10, pady=10)
frame_vote.pack(fill="x", padx=10)
tk.Label(frame_vote, text="รหัสนักเรียน (5 หลัก)").pack(anchor="w")
entry_id = tk.Entry(frame_vote, font=("Arial", 14))
entry_id.pack(fill="x")

selected = tk.StringVar(value="")   # ตัวแปรพิเศษของ tkinter เก็บว่าเลือกช่องไหน
for name in candidates:
    tk.Radiobutton(frame_vote, text=name, variable=selected, value=name,
                   font=("Arial", 13)).pack(anchor="w")
tk.Button(frame_vote, text="✅ ลงคะแนน", command=vote).pack(pady=5)
label_count = tk.Label(frame_vote, text="มาใช้สิทธิ์แล้ว 0 คน")
label_count.pack()

tk.Button(window, text="📊 ปิดหีบ นับคะแนน", command=count_votes).pack(pady=10)
canvas = tk.Canvas(window, width=440, height=230, bg="white")
canvas.pack()
label_winner = tk.Label(window, text="", font=("Arial", 15, "bold"))
label_winner.pack(pady=10)

window.mainloop()
