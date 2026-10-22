import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ASSETS = r"d:\WORKING PLACE\DoAn\slide_baocao\assets"
IMG_ARCH    = os.path.join(ASSETS, "image1.png")
IMG_AS608   = os.path.join(ASSETS, "image2.jpg")
IMG_RC522   = os.path.join(ASSETS, "image3.jpg")
IMG_KEYPAD  = os.path.join(ASSETS, "image4.jpg")
IMG_WEB     = os.path.join(ASSETS, "web_dashboard.png")
IMG_PCB     = os.path.join(ASSETS, "pcb_layout_preview.png")

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Màu sắc tối giản chuẩn sinh viên kỹ thuật
    BG_WHITE    = RGBColor(255, 255, 255)
    TEXT_BLACK  = RGBColor(20, 24, 33)      # Gần như đen, sắc nét
    TEXT_MUTED  = RGBColor(100, 110, 125)   # Xám đậm phụ đề
    ACCENT_BLUE = RGBColor(14, 82, 160)     # Xanh kỹ thuật UET
    BOX_BG      = RGBColor(248, 249, 251)   # Xám rất nhạt
    BOX_BORDER  = RGBColor(226, 232, 240)   # Viền mảnh
    FONT_NAME   = "Arial"

    def add_slide_header(slide, title, category="BÁO CÁO GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ (NHÓM 13)", slide_num=None):
        # Category nhỏ
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.3))
        tf_cat = tb_cat.text_frame
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_c = tf_cat.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.name = FONT_NAME
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_BLUE

        # Tiêu đề slide to rõ ràng
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.6))
        tf_title = tb_title.text_frame
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_t = tf_title.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_BLACK

        # Footer trang
        if slide_num:
            tb_f = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.3))
            tf_f = tb_f.text_frame
            tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
            p_f = tf_f.paragraphs[0]
            p_f.text = f"Đề tài Cửa bảo mật — Nguyễn Tuấn Sơn, Vũ Hữu Hoạt (UET)                                                                     Trang {slide_num} / 8"
            p_f.font.name = FONT_NAME
            p_f.font.size = Pt(10)
            p_f.font.color.rgb = TEXT_MUTED

    def add_image(slide, img_path, left, top, width, height, caption=None):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_WHITE
        card.line.color.rgb = BOX_BORDER
        card.line.width = Pt(1)

        cap_h = Inches(0.35) if caption else Inches(0)
        pad = Inches(0.08)
        avail_w = width - pad * 2
        avail_h = height - pad * 2 - cap_h

        if os.path.exists(img_path):
            from PIL import Image as PILImage
            with PILImage.open(img_path) as im:
                iw, ih = im.size
            ratio = iw / ih
            box_ratio = avail_w / avail_h
            if ratio > box_ratio:
                pw = avail_w
                ph = int(avail_w / ratio)
            else:
                ph = avail_h
                pw = int(avail_h * ratio)
            px = left + pad + int((avail_w - pw) / 2)
            py = top + pad + int((avail_h - ph) / 2)
            slide.shapes.add_picture(img_path, px, py, width=pw, height=ph)

        if caption:
            tb_c = slide.shapes.add_textbox(left, top + height - cap_h, width, cap_h)
            tf_c = tb_c.text_frame
            tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
            p = tf_c.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = caption
            p.font.name = FONT_NAME
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_WHITE
    bg1.line.fill.background()

    # Dải xanh trên cùng
    strip1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    strip1.fill.solid()
    strip1.fill.fore_color.rgb = ACCENT_BLUE
    strip1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(7.5), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ – ĐHQGHN\nKHOA CƠ HỌC KỸ THUẬT VÀ TỰ ĐỘNG HÓA"
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "BÁO CÁO TIẾN ĐỘ ĐỒ ÁN GIỮA KỲ"
    p.font.name = FONT_NAME
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Mô hình Hệ thống Cửa Bảo Mật"
    p.font.name = FONT_NAME
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_BLACK

    p = tf1.add_paragraph()
    p.text = "Tích hợp Vân tay AS608, Thẻ RFID RC522, Keypad 4x4 & Web App"
    p.font.name = FONT_NAME
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(32)

    p = tf1.add_paragraph()
    p.text = "Sinh viên thực hiện (Nhóm 13):\n• Nguyễn Tuấn Sơn  —  Lập trình ESP32, Giao diện Web App & Báo cáo\n• Vũ Hữu Hoạt        —  Thiết kế phần cứng, Vẽ mạch PCB & Mô hình"
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_BLACK
    p.space_after = Pt(8)

    # Ảnh bên phải trang bìa
    add_image(s1, IMG_WEB, Inches(8.8), Inches(1.5), Inches(3.8), Inches(4.5), "Giao diện Web App đã hoàn thiện")

    # =========================================================================
    # SLIDE 2: TỔNG QUAN HỆ THỐNG (CÓ SƠ ĐỒ KHỐI IMAGE1.PNG)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "1. Sơ đồ khối & Cấu trúc hệ thống", slide_num=2)

    add_image(s2, IMG_ARCH, Inches(0.8), Inches(1.5), Inches(6.8), Inches(3.5), "Hình 1: Sơ đồ kết nối các khối chức năng")

    # Text giải thích bên phải
    tb2 = s2.shapes.add_textbox(Inches(8.0), Inches(1.5), Inches(4.5), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    items2 = [
        ("Khối Xác thực tại cửa:", "Cảm biến vân tay quang học AS608, Module đọc thẻ RFID RC522 (13.56 MHz) và Bàn phím ma trận 4x4."),
        ("Khối Xử lý trung tâm:", "Vi điều khiển ESP32 nhận dữ liệu, kiểm tra quyền truy cập và điều khiển các ngoại vi."),
        ("Khối Hiển thị & Chấp hành:", "Màn hình LCD 16x2 I2C hiển thị thông báo hướng dẫn và Khóa chốt điện từ 12V thực hiện mở/đóng cửa."),
        ("Khối Giám sát Web App:", "ESP32 kết nối Wi-Fi, chạy Web Server cục bộ giúp theo dõi trạng thái, xem lịch sử ra vào và mở khóa từ xa.")
    ]
    for i, (title, desc) in enumerate(items2):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

        p2 = tf2.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_NAME
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_BLACK
        p2.space_after = Pt(10)

    # Box lưu ý bên dưới hình
    tb_note = s2.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(6.8), Inches(1.2))
    tf_n = tb_note.text_frame
    tf_n.word_wrap = True
    p = tf_n.paragraphs[0]
    p.text = "Điều chỉnh thực tế trong quá trình làm:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_BLACK
    p_sub = tf_n.add_paragraph()
    p_sub.text = "• Dùng Màn hình LCD 16x2 I2C thay cho loa để người dùng dễ theo dõi trạng thái, ký tự mật khẩu và thời gian đếm ngược.\n• Dùng Bàn phím ma trận 4x4 (16 phím) để có thêm các phím chức năng (Xóa *, Xác nhận #/D, Khóa C)."
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: LINH KIỆN ĐÃ CHUẨN BỊ (CÓ ẢNH THỰC TẾ)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "2. Linh kiện thực tế nhóm đã mua và khảo sát", slide_num=3)

    col_w = Inches(3.64)
    # Cột 1: AS608
    add_image(s3, IMG_AS608, Inches(0.8), Inches(1.5), col_w, Inches(2.4), "Cảm biến vân tay AS608")
    tb3_1 = s3.shapes.add_textbox(Inches(0.8), Inches(4.1), col_w, Inches(2.5))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    p = tf3_1.paragraphs[0]
    p.text = "Cảm biến vân tay AS608"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_BLUE
    p_it = tf3_1.add_paragraph()
    p_it.text = "• Điện áp: 3.3V – 5.0V DC\n• Giao tiếp: UART TTL (baudrate 57600)\n• Bộ nhớ: Lưu 127 mẫu vân tay trực tiếp trong cảm biến\n• Tốc độ nhận dạng: < 1 giây\n• Trạng thái: Đã mua, test tốt"
    p_it.font.size = Pt(13)
    p_it.font.color.rgb = TEXT_BLACK

    # Cột 2: RC522
    add_image(s3, IMG_RC522, Inches(4.84), Inches(1.5), col_w, Inches(2.4), "Module RFID-RC522 & Thẻ từ")
    tb3_2 = s3.shapes.add_textbox(Inches(4.84), Inches(4.1), col_w, Inches(2.5))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    p = tf3_2.paragraphs[0]
    p.text = "Module đọc thẻ RFID RC522"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_BLUE
    p_it = tf3_2.add_paragraph()
    p_it.text = "• Điện áp cấp: 3.3V DC (không cấp 5V)\n• Tần số: 13.56 MHz (chuẩn SPI)\n• Đọc thẻ trắng S50 và móc khóa NFC\n• Khoảng cách nhận thẻ: 0 – 30 mm\n• Trạng thái: Đã mua, test đọc UID tốt"
    p_it.font.size = Pt(13)
    p_it.font.color.rgb = TEXT_BLACK

    # Cột 3: Keypad 4x4
    add_image(s3, IMG_KEYPAD, Inches(8.88), Inches(1.5), col_w, Inches(2.4), "Bàn phím ma trận 4x4 có nắp")
    tb3_3 = s3.shapes.add_textbox(Inches(8.88), Inches(4.1), col_w, Inches(2.5))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True
    p = tf3_3.paragraphs[0]
    p.text = "Bàn phím 4x4 & Khóa chốt 12V"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_BLUE
    p_it = tf3_3.add_paragraph()
    p_it.text = "• Bàn phím 4x4: Phím cứng có nắp đậy, quét 8 chân Hàng - Cột\n• Màn hình: LCD 16x2 giao tiếp I2C 2 dây (SDA/SCL)\n• Khóa chốt 12V: Kích mở qua Relay/MOSFET\n• Trạng thái: Đã có đủ linh kiện"
    p_it.font.size = Pt(13)
    p_it.font.color.rgb = TEXT_BLACK

    # =========================================================================
    # SLIDE 4: PHÂN BỔ CHÂN ESP32 & CHỐNG NHIỄU PHẦN CỨNG
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "3. Sơ đồ kết nối chân ESP32 & Giải pháp chống nhiễu", slide_num=4)

    # Bảng phân bổ chân bên trái
    tb4_l = s4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.0))
    tf4_l = tb4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "Phân bổ chân GPIO trên ESP32:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    pins_info = [
        "Vân tay AS608 (UART2): RX -> GPIO 16, TX -> GPIO 17",
        "RFID RC522 (SPI): SS:5, SCK:18, MOSI:23, MISO:19, RST:4",
        "Màn hình LCD 16x2 (I2C): SDA -> GPIO 21, SCL -> GPIO 22",
        "Khóa chốt điện từ 12V: Điều khiển kích qua GPIO 2",
        "Bàn phím ma trận 4x4 (8 chân GPIO):\n   • 4 Hàng (R1-R4): GPIO 13, 12, 14, 27\n   • 4 Cột (C1-C4): GPIO 26, 25, 33, 32"
    ]
    for p_txt in pins_info:
        p_it = tf4_l.add_paragraph()
        p_it.text = f"• {p_txt}"
        p_it.font.size = Pt(13.5)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(8)

    # Giải pháp chống nhiễu bên phải
    tb4_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.0))
    tf4_r = tb4_r.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "Lưu ý kỹ thuật khi thiết kế mạch:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    circuit_notes = [
        ("Tránh chân Input-Only của ESP32:", "Các chân GPIO 34-39 không có trở kéo lên nội (pull-up). Nhóm đã chọn các chân GPIO 12..33 cho Keypad để quét phím ổn định, không cần hàn thêm trở ngoài."),
        ("Bảo vệ điện áp 3.3V cho RC522:", "Module RC522 dùng nguồn 3.3V, cấp 5V sẽ cháy chip. Mạch PCB thiết kế đường nguồn 3.3V riêng biệt."),
        ("Chống xung ngược từ khóa 12V:", "Cuộn hút khóa 12V khi ngắt điện sinh ra xung áp ngược làm reset ESP32. Nhóm dùng Diode 1N4007 mắc song song ngược cực khóa kèm tụ lọc 470uF.")
    ]
    for title, desc in circuit_notes:
        p_t = tf4_r.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = TEXT_BLACK
        p_d = tf4_r.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: THIẾT KẾ MẠCH IN PCB (CÓ ẢNH PCB)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "4. Kết quả thiết kế Mạch in PCB (Vũ Hữu Hoạt)", slide_num=5)

    add_image(s5, IMG_PCB, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.0), "Hình 2: Sơ đồ bố trí các khối trên bo mạch PCB")

    tb5 = s5.shapes.add_textbox(Inches(7.7), Inches(1.5), Inches(4.8), Inches(5.0))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "Nội dung Hoạt đã thực hiện:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    pcb_items = [
        "Đo đạc chân cắm thực tế: Đo đúng kích thước header của AS608, RC522, Keypad 4x4, LCD và Domino nguồn 12V.",
        "Vẽ Sơ đồ nguyên lý (Schematic): Liên kết toàn bộ linh kiện về ESP32, thêm khối nguồn hạ áp (12V -> 5V và 3.3V) và khối kích khóa 12V.",
        "Thiết kế Layout mạch in 2 lớp:\n  • Đường nguồn 12V cấp khóa chốt được vẽ to (> 40 mil) để chịu dòng 1.5A an toàn.\n  • Phủ đồng Mass (GND) cả 2 mặt để chống nhiễu Wi-Fi và sóng RFID 13.56 MHz.",
        "Trạng thái: Đã xuất file Gerber và sẵn sàng gửi gia công ở Giai đoạn 3."
    ]
    for it in pcb_items:
        p_it = tf5.add_paragraph()
        p_it.text = f"• {it}"
        p_it.font.size = Pt(13.5)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(10)

    # =========================================================================
    # SLIDE 6: PHẦN MỀM ESP32 & BẢO MẬT 2FA
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "5. Lập trình Firmware ESP32 & Chế độ Bảo mật 2 lớp", slide_num=6)

    # 2 Cột
    tb6_l = s6.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0))
    tf6_l = tb6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "Lập trình ESP32 (Nguyễn Tuấn Sơn):"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    firmware_items = [
        "Code chạy không chặn (Non-blocking): Không dùng delay(), dùng millis() quét Keypad 4x4 liên tục và đọc RFID/Vân tay mỗi 80ms, không làm đơ kết nối Web.",
        "Lưu trữ dữ liệu trong LittleFS: Lưu thẳng file giao diện Web và file config.json vào bộ nhớ Flash ESP32. Mất điện không mất mật khẩu hay danh sách thẻ.",
        "Giao thức WebSocket: Đẩy sự kiện quẹt thẻ/vân tay và phản chiếu dòng chữ LCD lên Web tức thì (< 100ms).",
        "Tên miền cục bộ: Dùng mDNS mở trang web bằng http://smartdoor.local."
    ]
    for it in firmware_items:
        p_it = tf6_l.add_paragraph()
        p_it.text = f"• {it}"
        p_it.font.size = Pt(13.5)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(10)

    tb6_r = s6.shapes.add_textbox(Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.0))
    tf6_r = tb6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "Chế độ Bảo mật 1 lớp & 2 lớp (2FA):"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    security_items = [
        ("Chế độ 1 Lớp (Mở nhanh):", "Dùng 1 trong 3 cách: quét Vân tay HOẶC Thẻ RFID HOẶC nhập mã PIN là mở cửa ngay."),
        ("Chế độ 2 Lớp (Bảo mật cao):", "Cần xác thực 2 bước liên tiếp:\n  1. Vân tay AS608 + Mã PIN Keypad 4x4\n  2. Thẻ từ RFID + Mã PIN Keypad 4x4\n  3. Vân tay AS608 + Thẻ từ RFID"),
        ("Tự hủy phiên sau 15 giây:", "Xác thực bước 1 thành công -> LCD hiện thông báo chờ bước 2. Nếu quá 15 giây không hoàn thành hoặc nhập sai, hệ thống tự khóa lại để bảo vệ.")
    ]
    for title, desc in security_items:
        p_t = tf6_r.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = TEXT_BLACK
        p_d = tf6_r.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: GIAO DIỆN WEB APP ĐÃ LÀM XONG (CÓ ẢNH CHỤP WEB)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "6. Giao diện Web App Quản lý & Triển khai Vercel", slide_num=7)

    add_image(s7, IMG_WEB, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.0), "Hình 3: Giao diện Web App thực tế (Đang chạy tại smartdoor-nhom13-data.vercel.app)")

    tb7 = s7.shapes.add_textbox(Inches(8.6), Inches(1.5), Inches(4.0), Inches(5.0))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "Tính năng trên Web App:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    web_items = [
        "Giao diện tối giản: Nền sáng, font chữ Inter rõ ràng, dùng tốt trên cả điện thoại và máy tính.",
        "Bảng điều khiển: Bấm nút mở khóa từ xa, xem trạng thái cửa và màn hình LCD 16x2 ảo theo thời gian thực.",
        "Nhật ký ra vào: Ghi nhận giờ, phương thức (Vân tay/RFID/PIN) và kết quả mở cửa; hỗ trợ xuất file CSV.",
        "Cấu hình hệ thống: Đổi mật khẩu Keypad, chỉnh chế độ 1 lớp / 2 lớp.",
        "Đã deploy Vercel: Có đường link online để thầy cô và nhóm test thử mọi lúc."
    ]
    for it in web_items:
        p_it = tf7.add_paragraph()
        p_it.text = f"• {it}"
        p_it.font.size = Pt(13)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: TIẾN ĐỘ THỰC HIỆN & KẾ HOẠCH TIẾP THEO
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "7. Tổng kết tiến độ giữa kỳ & Kế hoạch tiếp theo", slide_num=8)

    col_w8 = Inches(5.6)
    # Cột Trái: Đã xong
    tb8_l = s8.shapes.add_textbox(Inches(0.8), Inches(1.5), col_w8, Inches(5.0))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "Kết quả đạt được (Giai đoạn 1 & 2):"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    done_items = [
        "Linh kiện: Đã mua đủ 100% linh kiện chính và phụ kiện (AS608, RC522, Keypad 4x4, LCD I2C, ESP32, Khóa 12V).",
        "Nghiên cứu kỹ thuật: Hiểu rõ datasheet các module, giao thức UART/SPI/I2C và cách quét phím ma trận.",
        "Phần cứng: Hoàn thành sơ đồ nguyên lý và layout PCB 2 lớp, đã đo chuẩn chân cắm linh kiện.",
        "Phần mềm: Hoàn thành code ESP32 Non-blocking, làm xong Web App quản lý có bảo mật 2 lớp và đưa lên Vercel."
    ]
    for it in done_items:
        p_it = tf8_l.add_paragraph()
        p_it.text = f"✔ {it}"
        p_it.font.size = Pt(13.5)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(10)

    # Cột Phải: Tiếp theo
    tb8_r = s8.shapes.add_textbox(Inches(6.9), Inches(1.5), col_w8, Inches(5.0))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True

    p = tf8_r.paragraphs[0]
    p.text = "Kế hoạch nửa cuối học kỳ (Giai đoạn 3 & 4):"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    next_items = [
        "Gia công mạch in: Nhận bo mạch PCB, hàn linh kiện và đo kiểm tra các mức điện áp nguồn (12V, 5V, 3.3V).",
        "Lắp ráp cơ khí: Làm khung mô hình cửa gỗ/mica, gắn khóa chốt 12V, cảm biến vân tay, thẻ từ và bàn phím.",
        "Ghép nối & Thử nghiệm: Nạp code lên mạch thật, kiểm tra độ nhạy quét thẻ/vân tay và thời gian đáp ứng mở cửa.",
        "Hoàn thiện báo cáo: Thu thập số liệu thực nghiệm và viết cuốn báo cáo đồ án Cơ Điện Tử hoàn chỉnh."
    ]
    for it in next_items:
        p_it = tf8_r.add_paragraph()
        p_it.text = f"➔ {it}"
        p_it.font.size = Pt(13.5)
        p_it.font.color.rgb = TEXT_BLACK
        p_it.space_after = Pt(10)

    out_path = r"d:\WORKING PLACE\DoAn\slide_baocao\BaoCao_GiuaKy_Nhom13.pptx"
    prs.save(out_path)
    print("Successfully generated clean PPTX at:", out_path)

if __name__ == "__main__":
    create_presentation()
