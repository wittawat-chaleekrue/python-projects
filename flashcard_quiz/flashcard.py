# โปรแกรมบัตรคำศัพท์ภาษาอังกฤษ + แบบทดสอบ (Flashcard Quiz)
# ผู้พัฒนา: วิทวัส ชาลีเครือ

import tkinter as tk
from tkinter import messagebox
import random
import json
import os

FILE_NAME = "words.json"   # ชื่อไฟล์ที่ใช้เก็บคำศัพท์


# ---------- ส่วนที่ 1: อ่าน/บันทึกไฟล์ ----------

def load_words():
    # ถ้ามีไฟล์อยู่แล้ว ให้อ่านคำศัพท์จากไฟล์
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    # ถ้ายังไม่มีไฟล์ ให้เริ่มจากรายการว่าง
    return []


def save_words():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)


# ---------- ส่วนที่ 2: ตัวแปรเก็บข้อมูล ----------

words = load_words()   # รายการคำศัพท์ทั้งหมด
current_word = None    # คำที่กำลังถามอยู่ (ตอนเริ่มยังไม่มี)
score = 0              # จำนวนข้อที่ตอบถูก
total = 0              # จำนวนข้อที่ตอบทั้งหมด


# ---------- ส่วนที่ 3: ฟังก์ชันที่ทำงานเมื่อกดปุ่ม ----------

def add_word():
    word = entry_word.get().strip()
    read = entry_read.get().strip()
    meaning = entry_meaning.get().strip()

    if word == "" or meaning == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกคำศัพท์และคำแปล")
        return

    new_word = {"word": word, "read": read, "meaning": meaning, "wrong": 0}
    words.append(new_word)
    save_words()

    # ล้างช่องกรอกให้ว่าง พร้อมกรอกคำต่อไป
    entry_word.delete(0, tk.END)
    entry_read.delete(0, tk.END)
    entry_meaning.delete(0, tk.END)
    label_count.config(text=f"มีคำศัพท์ทั้งหมด {len(words)} คำ")


def next_question():
    global current_word

    if len(words) == 0:
        messagebox.showinfo("แจ้งเตือน", "ยังไม่มีคำศัพท์ กรุณาเพิ่มคำก่อน")
        return

    current_word = random.choice(words)
    label_question.config(text=current_word["word"])
    label_result.config(text="")
    entry_answer.delete(0, tk.END)


def check_answer():
    global current_word, score, total

    if current_word is None:
        messagebox.showinfo("แจ้งเตือน", "กดปุ่ม 'สุ่มคำถาม' ก่อน")
        return

    answer = entry_answer.get().strip()
    total = total + 1

    if answer == current_word["meaning"]:
        score = score + 1
        label_result.config(text="ถูกต้อง!", fg="green")
    else:
        current_word["wrong"] = current_word["wrong"] + 1
        save_words()
        label_result.config(
            text=f"ผิด คำตอบคือ {current_word['meaning']} (อ่านว่า {current_word['read']})",
            fg="red",
        )

    label_score.config(text=f"คะแนน {score} / {total}")
    current_word = None   # กันไม่ให้กดตรวจคำเดิมซ้ำเพื่อปั๊มคะแนน


def show_hard_words():
    text = ""
    for w in words:
        if w["wrong"] > 0:
            text = text + f"{w['word']} = {w['meaning']}  (ผิด {w['wrong']} ครั้ง)\n"

    if text == "":
        text = "ยังไม่มีคำที่ตอบผิดเลย เก่งมาก!"

    messagebox.showinfo("คำที่ตอบผิดบ่อย", text)


# ---------- ส่วนที่ 4: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("Flashcard Quiz - บัตรคำศัพท์")
window.geometry("450x520")

# --- กรอบเพิ่มคำศัพท์ ---
frame_add = tk.LabelFrame(window, text="เพิ่มคำศัพท์", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=10)

tk.Label(frame_add, text="คำศัพท์ (อังกฤษ)").pack(anchor="w")
entry_word = tk.Entry(frame_add)
entry_word.pack(fill="x")

tk.Label(frame_add, text="คำอ่าน (ภาษาไทย)").pack(anchor="w")
entry_read = tk.Entry(frame_add)
entry_read.pack(fill="x")

tk.Label(frame_add, text="คำแปล").pack(anchor="w")
entry_meaning = tk.Entry(frame_add)
entry_meaning.pack(fill="x")

tk.Button(frame_add, text="เพิ่มคำศัพท์", command=add_word).pack(pady=5)
label_count = tk.Label(frame_add, text=f"มีคำศัพท์ทั้งหมด {len(words)} คำ")
label_count.pack()

# --- กรอบแบบทดสอบ ---
frame_quiz = tk.LabelFrame(window, text="แบบทดสอบ", padx=10, pady=10)
frame_quiz.pack(fill="x", padx=10, pady=10)

tk.Button(frame_quiz, text="สุ่มคำถาม", command=next_question).pack()
label_question = tk.Label(frame_quiz, text="-", font=("Arial", 24, "bold"))
label_question.pack(pady=10)

tk.Label(frame_quiz, text="คำแปลคือ?").pack(anchor="w")
entry_answer = tk.Entry(frame_quiz)
entry_answer.pack(fill="x")

tk.Button(frame_quiz, text="ตรวจคำตอบ", command=check_answer).pack(pady=5)
label_result = tk.Label(frame_quiz, text="")
label_result.pack()
label_score = tk.Label(frame_quiz, text="คะแนน 0 / 0")
label_score.pack()

tk.Button(window, text="ดูคำที่ตอบผิดบ่อย", command=show_hard_words).pack(pady=5)

window.mainloop()
