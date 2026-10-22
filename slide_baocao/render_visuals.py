"""
Script vẽ ảnh chụp giao diện Web App (Dashboard + Cấu hình 2FA + Màn hình LCD 16x2)
và sơ đồ PCB 2 lớp độ phân giải cao để nhúng vào cả PowerPoint (.pptx) và Slide HTML.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = r"d:\WORKING PLACE\DoAn\slide_baocao\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def load_font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = [r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf"]
    else:
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
        ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_padlock(draw, cx, cy, color, unlocked=False):
    # Vẽ thân ổ khóa vector sạch đẹp
    draw.rounded_rectangle([cx-18, cy-2, cx+18, cy+24], radius=5, outline=color, width=3)
    if unlocked:
        draw.arc([cx-12, cy-22, cx+12, cy+4], start=180, end=330, fill=color, width=3)
    else:
        draw.arc([cx-12, cy-22, cx+12, cy+4], start=180, end=0, fill=color, width=3)
    draw.ellipse([cx-3, cy+8, cx+3, cy+14], fill=color)

def generate_web_dashboard_mockup():
    W, H = 1400, 880
    img = Image.new("RGB", (W, H), (250, 250, 250))
    draw = ImageDraw.Draw(img)

    f_title = load_font(20, True)
    f_bold  = load_font(16, True)
    f_reg   = load_font(15, False)
    f_sm    = load_font(13, False)
    f_kpi   = load_font(28, True)
    f_lcd   = load_font(22, True, mono=True)
    f_mono  = load_font(14, False, mono=True)

    # Browser Window Header
    draw.rectangle([0, 0, W, 46], fill=(24, 24, 27))
    for i, col in enumerate([(239, 68, 68), (245, 158, 11), (16, 185, 129)]):
        draw.ellipse([20 + i*24, 15, 34 + i*24, 29], fill=col)
    draw.rounded_rectangle([120, 9, 860, 37], radius=6, fill=(39, 39, 42))
    draw.text((140, 14), "https://smartdoor-nhom13-data.vercel.app   (hoặc http://smartdoor.local)", fill=(212, 212, 216), font=f_sm)

    # Topbar
    draw.rectangle([0, 46, W, 112], fill=(255, 255, 255), outline=(228, 228, 231))
    draw.rounded_rectangle([36, 61, 72, 97], radius=8, fill=(24, 24, 27))
    draw.rounded_rectangle([46, 77, 62, 90], radius=2, outline=(255, 255, 255), width=2)
    draw.arc([49, 68, 59, 80], start=180, end=0, fill=(255, 255, 255), width=2)

    draw.text((86, 59), "Smart Door Access", fill=(9, 9, 11), font=f_title)
    draw.text((86, 83), "Nhóm 13 • Nguyễn Tuấn Sơn & Vũ Hữu Hoạt", fill=(113, 113, 122), font=f_sm)

    # Right badges
    draw.rounded_rectangle([940, 65, 1085, 95], radius=15, fill=(240, 253, 244), outline=(187, 247, 208))
    draw.text((958, 71), "● ESP32 Wi-Fi", fill=(22, 163, 74), font=f_sm)
    draw.rounded_rectangle([1100, 65, 1220, 95], radius=15, fill=(255, 255, 255), outline=(228, 228, 231))
    draw.text((1118, 71), "Trực tuyến", fill=(82, 82, 91), font=f_sm)
    draw.rounded_rectangle([1235, 65, 1364, 95], radius=6, fill=(24, 24, 27))
    draw.text((1252, 71), "Test giả lập", fill=(255, 255, 255), font=f_sm)

    # Segmented Tabs
    draw.rounded_rectangle([36, 130, 660, 172], radius=8, fill=(244, 244, 245), outline=(228, 228, 231))
    draw.rounded_rectangle([42, 135, 160, 167], radius=6, fill=(255, 255, 255))
    draw.text((62, 142), "Tổng quan", fill=(9, 9, 11), font=f_bold)
    draw.text((185, 143), "Nhật ký ra vào (12)", fill=(82, 82, 91), font=f_reg)
    draw.text((355, 143), "Vân tay & Thẻ RFID", fill=(82, 82, 91), font=f_reg)
    draw.text((515, 143), "Cấu hình hệ thống", fill=(82, 82, 91), font=f_reg)

    # 4 KPI Cards
    kpis = [
        ("Trạng thái khóa 12V", "Đang mở", "Chế độ: 2 Lớp (Vân tay + PIN)", (22, 163, 74)),
        ("Truy cập hợp lệ", "28", "Lượt mở cửa thành công", (9, 9, 11)),
        ("Cảnh báo sai", "2", "Vân tay / Thẻ lạ / Sai PIN", (220, 38, 38)),
        ("Định danh đã lưu", "4 Vân tay • 4 Thẻ", "Lưu trong Flash LittleFS", (9, 9, 11))
    ]
    card_w = 316
    for i, (label, val, sub, col) in enumerate(kpis):
        x0 = 36 + i * (card_w + 21)
        y0 = 190
        draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + 112], radius=10, fill=(255, 255, 255), outline=(228, 228, 231))
        draw.text((x0 + 20, y0 + 16), label, fill=(113, 113, 122), font=f_sm)
        draw.text((x0 + 20, y0 + 42), val, fill=col, font=f_kpi)
        draw.text((x0 + 20, y0 + 80), sub, fill=(113, 113, 122), font=f_sm)

    # Left Main Card: Door Control
    draw.rounded_rectangle([36, 322, 490, 845], radius=10, fill=(255, 255, 255), outline=(228, 228, 231))
    draw.text((60, 344), "Điều khiển khóa cửa trung tâm", fill=(9, 9, 11), font=f_title)
    draw.text((60, 370), "Điều khiển trực tiếp khóa chốt điện từ 12V qua Wi-Fi", fill=(113, 113, 122), font=f_sm)

    # Inner Lock Box
    draw.rounded_rectangle([60, 405, 466, 700], radius=10, fill=(250, 250, 250), outline=(228, 228, 231))
    draw.ellipse([218, 430, 308, 520], fill=(240, 253, 244), outline=(134, 239, 172), width=3)
    draw_padlock(draw, 263, 475, (22, 163, 74), unlocked=True)
    draw.text((185, 540), "CỬA ĐANG MỞ", fill=(22, 163, 74), font=f_title)
    draw.text((135, 570), "Tự động đóng khóa chốt 12V sau 4 giây...", fill=(113, 113, 122), font=f_reg)
    draw.rounded_rectangle([84, 618, 442, 668], radius=8, fill=(24, 24, 27))
    draw.text((178, 633), "Mở khóa từ xa (Web)", fill=(255, 255, 255), font=f_bold)

    draw.text((60, 725), "SỰ KIỆN GẦN NHẤT", fill=(113, 113, 122), font=f_sm)
    draw.text((60, 750), "2FA (Vân tay + Mã PIN) — Nguyễn Tuấn Sơn (ID #1)", fill=(9, 9, 11), font=f_bold)
    draw.text((60, 778), "22/10/2026 14:35:10 • Xác thực 2 lớp hợp lệ", fill=(22, 163, 74), font=f_sm)

    # Right Main Card: LCD 16x2 Live Mirror + Logs Table
    draw.rounded_rectangle([512, 322, 1364, 845], radius=10, fill=(255, 255, 255), outline=(228, 228, 231))
    draw.text((538, 344), "Màn hình hiển thị tại cửa (LCD 16x2 Live Mirror)", fill=(9, 9, 11), font=f_title)
    draw.text((538, 370), "Đồng bộ thời gian thực qua WebSocket với màn hình I2C 0x27", fill=(113, 113, 122), font=f_sm)

    # LCD Screen Box
    draw.rounded_rectangle([538, 405, 1338, 515], radius=8, fill=(24, 24, 27), outline=(63, 63, 70), width=2)
    draw.text((570, 424), "XAC THUC 2 LOP OK", fill=(163, 230, 53), font=f_lcd)
    draw.text((570, 464), "XIN MOI VAO!    ", fill=(163, 230, 53), font=f_lcd)

    # Recent Logs Table
    draw.text((538, 535), "Nhật ký truy cập thời gian thực", fill=(82, 82, 91), font=f_bold)
    draw.rounded_rectangle([538, 565, 1338, 820], radius=8, fill=(255, 255, 255), outline=(228, 228, 231))
    draw.rectangle([539, 566, 1337, 606], fill=(248, 250, 252))
    draw.text((556, 577), "Thời gian", fill=(113, 113, 122), font=f_sm)
    draw.text((735, 577), "Phương thức", fill=(113, 113, 122), font=f_sm)
    draw.text((925, 577), "Người dùng / Chi tiết", fill=(113, 113, 122), font=f_sm)
    draw.text((1225, 577), "Trạng thái", fill=(113, 113, 122), font=f_sm)

    rows = [
        ("22/10/2026 14:35:10", "2FA (FP+PIN)", "Nguyễn Tuấn Sơn (ID #1) + PIN", True),
        ("22/10/2026 14:20:05", "Thẻ RFID", "Vũ Hữu Hoạt (9B:11:C4:7E)", True),
        ("22/10/2026 14:12:44", "Vân tay AS608", "Nguyễn Tuấn Sơn (ID #1)", True),
        ("22/10/2026 13:58:19", "Keypad 4x4", "Nhập sai PIN (4 số)", False),
    ]
    for idx, (t, m, u, ok) in enumerate(rows):
        ry = 610 + idx * 50
        draw.line([538, ry, 1338, ry], fill=(228, 228, 231))
        draw.text((556, ry + 15), t, fill=(113, 113, 122), font=f_mono)
        draw.rounded_rectangle([735, ry + 11, 880, ry + 39], radius=5, fill=(244, 244, 245), outline=(228, 228, 231))
        draw.text((748, ry + 16), m, fill=(63, 63, 70), font=f_sm)
        draw.text((925, ry + 15), u, fill=(9, 9, 11), font=f_reg)
        if ok:
            draw.rounded_rectangle([1225, ry + 11, 1315, ry + 39], radius=12, fill=(240, 253, 244), outline=(187, 247, 208))
            draw.text((1245, ry + 16), "Hợp lệ", fill=(22, 163, 74), font=f_sm)
        else:
            draw.rounded_rectangle([1225, ry + 11, 1315, ry + 39], radius=12, fill=(254, 242, 242), outline=(254, 202, 202))
            draw.text((1242, ry + 16), "Từ chối", fill=(220, 38, 38), font=f_sm)

    out_file = os.path.join(ASSETS_DIR, "web_dashboard.png")
    img.save(out_file)
    print("Saved:", out_file)

def generate_pcb_diagram():
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), (14, 42, 28)) # Dark green solder mask PCB
    draw = ImageDraw.Draw(img)

    f_title = load_font(22, True)
    f_bold  = load_font(15, True)
    f_sm    = load_font(13, False)
    f_mono  = load_font(12, True, mono=True)

    # Outer PCB Board Yellow Silkscreen Border
    draw.rounded_rectangle([24, 24, W-24, H-24], radius=18, outline=(234, 179, 8), width=3)
    for cx, cy in [(56, 56), (W-56, 56), (56, H-56), (W-56, H-56)]:
        draw.ellipse([cx-16, cy-16, cx+16, cy+16], fill=(217, 119, 6), outline=(254, 240, 138), width=2)
        draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(15, 23, 42))

    draw.text((90, 42), "SMART DOOR CONTROLLER PCB V1.0 — NHOM 13 (HOAT & SON)", fill=(254, 240, 138), font=f_title)
    draw.text((90, 72), "2-Layer FR4 • GND Copper Pour • Flyback Diode Protection", fill=(167, 243, 208), font=f_sm)

    # Copper traces
    traces = [
        [(350, 220), (450, 220)],
        [(350, 400), (450, 400)],
        [(350, 580), (450, 580)],
        [(750, 230), (850, 230)],
        [(750, 420), (850, 420)],
        [(750, 590), (850, 590)],
    ]
    for p0, p1 in traces:
        draw.line([p0, p1], fill=(22, 163, 74), width=8)
        draw.line([p0, p1], fill=(134, 239, 172), width=2)

    # Central ESP32 Module Footprint
    draw.rounded_rectangle([450, 160, 750, 645], radius=8, fill=(20, 30, 48), outline=(255, 255, 255), width=2)
    draw.rectangle([500, 175, 700, 275], fill=(148, 163, 184), outline=(226, 232, 240))
    draw.text((532, 215), "ESP32-WROOM-32", fill=(15, 23, 42), font=f_bold)
    draw.text((495, 310), "VI ĐIỀU KHIỂN TRUNG TÂM", fill=(254, 240, 138), font=f_bold)
    draw.text((480, 345), "• UART2: GPIO 16, 17 (AS608)", fill=(226, 232, 240), font=f_mono)
    draw.text((480, 375), "• SPI: GPIO 5,18,19,23,4 (RC522)", fill=(226, 232, 240), font=f_mono)
    draw.text((480, 405), "• I2C: GPIO 21, 22 (LCD 16x2)", fill=(226, 232, 240), font=f_mono)
    draw.text((480, 435), "• R1-R4: 13, 12, 14, 27", fill=(226, 232, 240), font=f_mono)
    draw.text((480, 465), "• C1-C4: 26, 25, 33, 32", fill=(226, 232, 240), font=f_mono)
    draw.text((480, 495), "• RELAY OUT: GPIO 2", fill=(253, 224, 71), font=f_mono)

    # Left Headers (widened to 350)
    blocks_left = [
        (160, "J1: HEADER AS608 (6P)", "VCC(5V) | TX | RX | GND", "Giao tiếp UART2 TTL 57600"),
        (340, "J2: HEADER RC522 (8P)", "3.3V | RST | GND | MISO | MOSI | SCK | SS", "Chuẩn SPI - Tuyệt đối cấp 3.3V DC"),
        (520, "J3: HEADER KEYPAD 4x4 (8P)", "R1 R2 R3 R4 | C1 C2 C3 C4", "Quét ma trận 8 chân GPIO")
    ]
    for y, title, pins, note in blocks_left:
        draw.rounded_rectangle([55, y, 355, y+125], radius=6, fill=(18, 58, 38), outline=(254, 240, 138), width=2)
        draw.text((70, y+14), title, fill=(254, 240, 138), font=f_bold)
        draw.text((70, y+46), pins, fill=(255, 255, 255), font=f_mono)
        draw.text((70, y+82), note, fill=(167, 243, 208), font=f_sm)

    # Right Blocks
    blocks_right = [
        (160, "PWR: KHỐI NGUỒN HẠ ÁP", "12V DC IN -> Buck 5V & LDO 3.3V", "Tụ lọc 470uF + 100nF chống sụt áp"),
        (340, "J4: HEADER LCD I2C (4P)", "GND | VCC(5V) | SDA(21) | SCL(22)", "Hiển thị trạng thái & mật mã"),
        (520, "K1: CÔNG SUẤT KHÓA 12V", "Opto + MOSFET/Relay + Diode 1N4007", "Đường mạch rộng >40mil chịu dòng 1.5A")
    ]
    for y, title, pins, note in blocks_right:
        draw.rounded_rectangle([845, y, 1145, y+125], radius=6, fill=(18, 58, 38), outline=(254, 240, 138), width=2)
        draw.text((860, y+14), title, fill=(254, 240, 138), font=f_bold)
        draw.text((860, y+46), pins, fill=(255, 255, 255), font=f_mono)
        draw.text((860, y+82), note, fill=(167, 243, 208), font=f_sm)

    out_file = os.path.join(ASSETS_DIR, "pcb_layout_preview.png")
    img.save(out_file)
    print("Saved:", out_file)

if __name__ == "__main__":
    generate_web_dashboard_mockup()
    generate_pcb_diagram()
