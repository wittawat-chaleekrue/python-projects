# ==========================================================
# โปรแกรมตรวจความแข็งแรงของรหัสผ่าน (Password Strength Checker)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter
# ==========================================================

import tkinter as tk      # เครื่องมือสร้างหน้าต่างโปรแกรม (GUI)
import string             # มีชุดตัวอักษรสำเร็จรูป เช่น a-z, A-Z, 0-9
import secrets            # ใช้สุ่มแบบปลอดภัย เหมาะกับงานรหัสผ่าน

# ---------- ข้อมูลตั้งต้น ----------

# รหัสผ่านยอดฮิตที่คนใช้บ่อย (แฮกเกอร์จะลองพวกนี้ก่อนเสมอ)
COMMON_PASSWORDS = [
    "123456", "12345678", "123456789", "password", "qwerty",
    "111111", "abc123", "iloveyou", "admin", "000000",
]

# ชุดตัวอักษรแต่ละประเภท
LOWER = string.ascii_lowercase    # "abcdefghijklmnopqrstuvwxyz"
UPPER = string.ascii_uppercase    # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = string.digits            # "0123456789"
SYMBOLS = "!@#$%^&*()-_=+?"       # สัญลักษณ์ที่เราเลือกใช้


# ---------- ส่วนที่ 1: ตรรกะ (สมองของโปรแกรม) ----------

def has_char(password, char_set):
    """ตรวจว่าใน password มีตัวอักษรจาก char_set อย่างน้อย 1 ตัวไหม"""
    for ch in password:
        if ch in char_set:
            return True
    return False


def check_password(password):
    """ให้คะแนนรหัสผ่าน 0-6 และคืนค่า (คะแนน, รายการคำแนะนำ)"""
    score = 0
    tips = []

    # ถ้าเป็นรหัสยอดฮิต ได้ 0 คะแนนทันที
    if password.lower() in COMMON_PASSWORDS:
        return 0, ["รหัสนี้เป็นรหัสยอดฮิต ถูกเดาได้ภายในไม่กี่วินาที!"]

    # เกณฑ์ที่ 1-2: ความยาว
    if len(password) >= 8:
        score = score + 1
    else:
        tips.append("ควรยาวอย่างน้อย 8 ตัวอักษร")

    if len(password) >= 12:
        score = score + 1
    else:
        tips.append("ถ้ายาว 12 ตัวขึ้นไปจะปลอดภัยกว่ามาก")

    # เกณฑ์ที่ 3-6: มีตัวอักษรหลายประเภท
    if has_char(password, LOWER):
        score = score + 1
    else:
        tips.append("เพิ่มตัวพิมพ์เล็ก (a-z)")

    if has_char(password, UPPER):
        score = score + 1
    else:
        tips.append("เพิ่มตัวพิมพ์ใหญ่ (A-Z)")

    if has_char(password, DIGITS):
        score = score + 1
    else:
        tips.append("เพิ่มตัวเลข (0-9)")

    if has_char(password, SYMBOLS):
        score = score + 1
    else:
        tips.append("เพิ่มสัญลักษณ์ เช่น ! @ # $")

    return score, tips


def get_level(score):
    """แปลงคะแนนเป็น (ชื่อระดับ, สี)"""
    if score <= 2:
        return "อ่อน", "red"
    elif score <= 4:
        return "ปานกลาง", "orange"
    else:
        return "แข็งแรง", "green"


def generate_password(length=16):
    """สุ่มรหัสผ่านใหม่ วนสุ่มไปเรื่อย ๆ จนกว่าจะได้คะแนนเต็ม 6"""
    all_chars = LOWER + UPPER + DIGITS + SYMBOLS
    while True:
        password = ""
        for i in range(length):
            password = password + secrets.choice(all_chars)
        score, tips = check_password(password)
        if score == 6:
            return password


# ---------- ส่วนที่ 2: ฟังก์ชันที่ทำงานเมื่อผู้ใช้กด/พิมพ์ ----------

def update_result(event=None):
    """เรียกทุกครั้งที่ผู้ใช้พิมพ์ เพื่ออัปเดตผลทันที"""
    password = password_entry.get()

    # ถ้ายังไม่ได้พิมพ์อะไร ให้ล้างหน้าจอ
    if password == "":
        level_label.config(text="ระดับ: -", fg="black")
        tips_label.config(text="")
        bar_canvas.coords(bar, 0, 0, 0, 20)
        return

    score, tips = check_password(password)
    level, color = get_level(score)

    level_label.config(text=f"ระดับ: {level}  ({score}/6 คะแนน)", fg=color)

    # วาดแถบความแข็งแรง: ความกว้างตามคะแนน (เต็ม 300 พิกเซล)
    bar_width = score / 6 * 300
    bar_canvas.coords(bar, 0, 0, bar_width, 20)
    bar_canvas.itemconfig(bar, fill=color)

    # แสดงคำแนะนำ
    if len(tips) == 0:
        tips_label.config(text="✔ ยอดเยี่ยม! รหัสผ่านนี้ปลอดภัย")
    else:
        text = ""
        for tip in tips:
            text = text + "• " + tip + "\n"
        tips_label.config(text=text)


def toggle_show():
    """สลับระหว่างแสดง/ซ่อนรหัสผ่าน"""
    if show_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def on_generate():
    """กดปุ่มสุ่ม: สร้างรหัสใหม่ใส่ในช่อง แล้วตรวจทันที"""
    new_password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, new_password)
    update_result()


def on_copy():
    """คัดลอกรหัสผ่านไปที่คลิปบอร์ด (เอาไปวางที่อื่นได้)"""
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    copy_button.config(text="คัดลอกแล้ว ✔")
    root.after(1500, lambda: copy_button.config(text="คัดลอก"))


# ---------- ส่วนที่ 3: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("ตรวจความแข็งแรงของรหัสผ่าน")
root.geometry("420x460")
root.resizable(False, False)

title_label = tk.Label(root, text="🔐 ตรวจความแข็งแรงของรหัสผ่าน",
                       font=("Helvetica", 18, "bold"))
title_label.pack(pady=15)

tk.Label(root, text="พิมพ์รหัสผ่าน:").pack()

password_entry = tk.Entry(root, show="*", width=30, font=("Helvetica", 16))
password_entry.pack(pady=5)
password_entry.bind("<KeyRelease>", update_result)

show_var = tk.IntVar()
tk.Checkbutton(root, text="แสดงรหัสผ่าน", variable=show_var,
               command=toggle_show).pack()

bar_canvas = tk.Canvas(root, width=300, height=20, bg="#dddddd",
                       highlightthickness=0)
bar_canvas.pack(pady=10)
bar = bar_canvas.create_rectangle(0, 0, 0, 20, fill="red", width=0)

level_label = tk.Label(root, text="ระดับ: -", font=("Helvetica", 14, "bold"))
level_label.pack()

tips_label = tk.Label(root, text="", justify="left")
tips_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="สุ่มรหัสผ่านที่ปลอดภัย",
          command=on_generate).pack(side="left", padx=5)
copy_button = tk.Button(button_frame, text="คัดลอก", command=on_copy)
copy_button.pack(side="left", padx=5)

root.mainloop()
