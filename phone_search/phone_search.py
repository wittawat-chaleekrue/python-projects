# โปรแกรมสมุดเบอร์โทรหมู่บ้าน (เปรียบเทียบ Linear Search กับ Binary Search)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: ค้นหาแบบไล่ทีละคน vs แบบแบ่งครึ่ง แบบไหนใช้ขั้นตอนน้อยกว่า

import tkinter as tk
from tkinter import messagebox

# รายชื่อตัวอย่าง [ชื่อ, เบอร์โทร]  (เบอร์สมมติ ไม่ใช่เบอร์จริง)
contacts = [
    ["ผู้ใหญ่บ้าน", "081-000-0001"],
    ["อสม.หมู่ 1", "081-000-0002"],
    ["รพ.สต.", "081-000-0003"],
    ["ร้านค้าชุมชน", "081-000-0004"],
    ["ช่างไฟ", "081-000-0005"],
    ["ช่างประปา", "081-000-0006"],
    ["วินมอเตอร์ไซค์", "081-000-0007"],
    ["โรงเรียน", "081-000-0008"],
    ["วัด", "081-000-0009"],
    ["ร้านซ่อมรถ", "081-000-0010"],
    ["ร้านข้าวมันไก่", "081-000-0011"],
    ["ตลาดนัด", "081-000-0012"],
    ["กู้ภัย", "081-000-0013"],
    ["ไปรษณีย์", "081-000-0014"],
    ["ร้านยา", "081-000-0015"],
    ["ปั๊มน้ำมัน", "081-000-0016"],
]
contacts.sort()   # Binary Search ใช้ได้กับข้อมูลที่เรียงแล้วเท่านั้น!


# ---------- ส่วนที่ 1: การค้นหา 2 แบบ ----------

def linear_search(name):
    # แบบที่ 1: ไล่ดูทีละคนตั้งแต่คนแรก จนกว่าจะเจอ
    steps = 0
    for person in contacts:
        steps = steps + 1
        if person[0] == name:
            return person[1], steps
    return None, steps   # None = ไม่เจอ


def binary_search(name):
    # แบบที่ 2: เปิดตรงกลาง แล้วตัดทิ้งทีละครึ่ง (เหมือนเปิดพจนานุกรม)
    low = 0                    # ขอบซ้ายของช่วงที่ยังต้องหา
    high = len(contacts) - 1   # ขอบขวาของช่วงที่ยังต้องหา
    steps = 0

    while low <= high:
        steps = steps + 1
        mid = (low + high) // 2        # ตำแหน่งตรงกลาง
        mid_name = contacts[mid][0]

        if mid_name == name:
            return contacts[mid][1], steps
        elif mid_name < name:
            low = mid + 1              # ชื่อที่หาอยู่ "หลัง" ตรงกลาง → ตัดครึ่งซ้ายทิ้ง
        else:
            high = mid - 1             # ชื่อที่หาอยู่ "ก่อน" ตรงกลาง → ตัดครึ่งขวาทิ้ง

    return None, steps


# ---------- ส่วนที่ 2: ฟังก์ชันของปุ่ม ----------

def search():
    name = entry_search.get().strip()
    if name == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณาพิมพ์ชื่อที่ต้องการค้นหา")
        return

    phone1, steps1 = linear_search(name)
    phone2, steps2 = binary_search(name)

    if phone1 is None:
        label_result.config(text=f"ไม่พบ \"{name}\" ในสมุด", fg="red")
    else:
        label_result.config(text=f"📞 {name} : {phone1}", fg="blue")

    label_compare.config(
        text=f"Linear Search (ไล่ทีละคน) ใช้ {steps1} ขั้น\n"
             f"Binary Search (แบ่งครึ่ง) ใช้ {steps2} ขั้น"
    )


def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    if name == "" or phone == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกทั้งชื่อและเบอร์")
        return

    found, steps = binary_search(name)
    if found is not None:
        messagebox.showwarning("แจ้งเตือน", f"มีชื่อ {name} อยู่แล้ว")
        return

    contacts.append([name, phone])
    contacts.sort()   # เพิ่มแล้วต้องเรียงใหม่ทุกครั้ง ไม่งั้น Binary Search จะหาผิด
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    refresh_list()


def pick_from_list(event):
    # คลิกชื่อในรายการ → ใส่ชื่อนั้นลงช่องค้นหาให้อัตโนมัติ
    selected = listbox.curselection()
    if len(selected) > 0:
        entry_search.delete(0, tk.END)
        entry_search.insert(0, contacts[selected[0]][0])


def refresh_list():
    listbox.delete(0, tk.END)
    for person in contacts:
        listbox.insert(tk.END, f"{person[0]}  |  {person[1]}")
    label_count.config(text=f"ทั้งหมด {len(contacts)} รายชื่อ (เรียงแล้ว)")


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("สมุดเบอร์โทรหมู่บ้าน")
window.geometry("480x640")

frame_search = tk.LabelFrame(window, text="ค้นหาเบอร์", padx=10, pady=10)
frame_search.pack(fill="x", padx=10, pady=10)
entry_search = tk.Entry(frame_search, font=("Arial", 14))
entry_search.pack(fill="x")
tk.Button(frame_search, text="🔍 ค้นหา", command=search).pack(pady=5)
label_result = tk.Label(frame_search, text="", font=("Arial", 16))
label_result.pack()
label_compare = tk.Label(frame_search, text="", justify="left")
label_compare.pack()

listbox = tk.Listbox(window, height=10, font=("Arial", 13))
listbox.pack(fill="both", expand=True, padx=10)
listbox.bind("<<ListboxSelect>>", pick_from_list)
label_count = tk.Label(window, text="")
label_count.pack()

frame_add = tk.LabelFrame(window, text="เพิ่มรายชื่อ", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=10)
tk.Label(frame_add, text="ชื่อ").pack(anchor="w")
entry_name = tk.Entry(frame_add)
entry_name.pack(fill="x")
tk.Label(frame_add, text="เบอร์โทร").pack(anchor="w")
entry_phone = tk.Entry(frame_add)
entry_phone.pack(fill="x")
tk.Button(frame_add, text="เพิ่ม", command=add_contact).pack(pady=5)

refresh_list()
window.mainloop()
