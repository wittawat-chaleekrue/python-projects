# โปรแกรมนำทางในโรงเรียน (Graph + BFS หาเส้นทางที่ผ่านจุดน้อยที่สุด)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: สถานที่ = จุด (node) / ทางเดิน = เส้นเชื่อม (edge) / ค้นหาแบบกระจายทีละชั้น (BFS)

import tkinter as tk
from tkinter import messagebox

# ตำแหน่งของแต่ละสถานที่บนจอ (x, y) — แก้ชื่อเป็นอาคารจริงของโรงเรียนได้
positions = {
    "ประตูหน้า": (70, 340),
    "ลานจอดรถ": (70, 190),
    "เสาธง": (210, 340),
    "อาคาร 1": (210, 190),
    "ห้องสมุด": (210, 60),
    "อาคาร 2": (350, 340),
    "หอประชุม": (350, 220),
    "โรงอาหาร": (480, 270),
    "อาคาร 3": (400, 60),
    "สนามฟุตบอล": (580, 340),
    "ประตูหลัง": (580, 60),
}

# ทางเดินที่เชื่อมกัน (เดินได้ทั้งไปและกลับ)
paths = [
    ("ประตูหน้า", "ลานจอดรถ"), ("ประตูหน้า", "เสาธง"),
    ("ลานจอดรถ", "อาคาร 1"), ("เสาธง", "อาคาร 1"),
    ("เสาธง", "อาคาร 2"), ("เสาธง", "หอประชุม"),
    ("อาคาร 1", "ห้องสมุด"), ("อาคาร 2", "โรงอาหาร"),
    ("หอประชุม", "โรงอาหาร"), ("ห้องสมุด", "อาคาร 3"),
    ("โรงอาหาร", "อาคาร 3"), ("โรงอาหาร", "สนามฟุตบอล"),
    ("อาคาร 3", "ประตูหลัง"), ("สนามฟุตบอล", "ประตูหลัง"),
]

# สร้าง Graph แบบ "รายชื่อเพื่อนบ้าน": สถานที่ → [สถานที่ที่เดินไปถึงได้ทันที]
school_map = {}
for place in positions:
    school_map[place] = []
for a, b in paths:
    school_map[a].append(b)   # เดินจาก a ไป b ได้
    school_map[b].append(a)   # และเดินจาก b กลับ a ได้


# ---------- ส่วนที่ 1: BFS (Breadth-First Search) ----------

def bfs(start, goal):
    queue = [start]               # คิวของจุดที่รอสำรวจ (เข้าก่อน-ออกก่อน)
    came_from = {start: None}     # จำว่ามาถึงจุดนี้จากจุดไหน (และใช้เช็คว่าเคยมาแล้ว)

    while len(queue) > 0:
        current = queue.pop(0)    # หยิบจุดที่รอนานที่สุดออกมาสำรวจ
        if current == goal:
            break
        for neighbor in school_map[current]:
            if neighbor not in came_from:       # ยังไม่เคยไปจุดนี้
                came_from[neighbor] = current   # จดว่ามาจาก current
                queue.append(neighbor)          # ต่อท้ายคิวไว้สำรวจทีหลัง

    if goal not in came_from:
        return None               # ไม่มีทางไปถึง

    # ย้อนรอยจากปลายทางกลับไปต้นทาง แล้วกลับลำดับ
    route = []
    place = goal
    while place is not None:
        route.append(place)
        place = came_from[place]
    route.reverse()
    return route


# ---------- ส่วนที่ 2: วาดแผนที่ + ปุ่มหาเส้นทาง ----------

def draw_map(route):
    canvas.delete("all")
    # วาดทางเดินทั้งหมดเป็นเส้นสีเทา
    for a, b in paths:
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        canvas.create_line(x1, y1, x2, y2, fill="#bbbbbb", width=3)
    # วาดเส้นทางที่หาได้ทับเป็นสีแดงหนา
    for i in range(len(route) - 1):
        x1, y1 = positions[route[i]]
        x2, y2 = positions[route[i + 1]]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=6)
    # วาดจุดสถานที่ (ต้นทางสีเขียว ปลายทางสีแดง ทางผ่านสีส้ม)
    for place in positions:
        x, y = positions[place]
        color = "#d6eaf8"
        if place in route:
            color = "orange"
        if len(route) > 0 and place == route[0]:
            color = "#2ecc71"
        if len(route) > 0 and place == route[-1]:
            color = "#e74c3c"
        canvas.create_oval(x - 14, y - 14, x + 14, y + 14, fill=color)
        canvas.create_text(x, y + 26, text=place, font=("Arial", 11, "bold"))


def find_route():
    start = var_start.get()
    goal = var_goal.get()
    if start == goal:
        messagebox.showinfo("แจ้งเตือน", "ต้นทางกับปลายทางเป็นที่เดียวกัน")
        return
    route = bfs(start, goal)
    if route is None:
        label_result.config(text="ไม่มีทางเดินไปถึง", fg="red")
        draw_map([])
        return
    draw_map(route)
    label_result.config(text=" → ".join(route) +
                        f"\n(เดินผ่าน {len(route) - 1} ช่วงทาง)", fg="blue")


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("นำทางในโรงเรียน")
window.geometry("680x560")

frame_top = tk.Frame(window, pady=10)
frame_top.pack()
place_names = list(positions.keys())
var_start = tk.StringVar(value="ประตูหน้า")
var_goal = tk.StringVar(value="ประตูหลัง")
tk.Label(frame_top, text="จาก").pack(side="left")
tk.OptionMenu(frame_top, var_start, *place_names).pack(side="left", padx=5)
tk.Label(frame_top, text="ไป").pack(side="left")
tk.OptionMenu(frame_top, var_goal, *place_names).pack(side="left", padx=5)
tk.Button(frame_top, text="🧭 หาเส้นทาง", command=find_route).pack(side="left", padx=10)

canvas = tk.Canvas(window, width=650, height=400, bg="#fdfefe")
canvas.pack()
label_result = tk.Label(window, text="เลือกต้นทาง-ปลายทาง แล้วกด \"หาเส้นทาง\"",
                        font=("Arial", 13), wraplength=640)
label_result.pack(pady=10)

draw_map([])
window.mainloop()
