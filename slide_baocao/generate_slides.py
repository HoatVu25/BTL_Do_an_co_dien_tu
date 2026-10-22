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
IMG_VERCEL  = os.path.join(ASSETS, "vercel_deploy.png")
IMG_PCB     = os.path.join(ASSETS, "pcb_layout_preview.png")

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    NAVY_MAIN   = RGBColor(11, 35, 71)      # #0B2347
    ACCENT_BLUE = RGBColor(16, 85, 154)     # #10559A
    CARD_BG     = RGBColor(246, 248, 251)   # #F6F8FB
    CARD_BORDER = RGBColor(218, 225, 235)   # #DAE1EB
    TEXT_DARK   = RGBColor(20, 28, 40)      # #141C28
    TEXT_MUTED  = RGBColor(95, 108, 125)    # #5F6C7D
    WHITE       = RGBColor(255, 255, 255)
    GREEN_BG    = RGBColor(236, 253, 245)
    GREEN_TEXT  = RGBColor(16, 135, 72)

    def add_header(slide, title_text, slide_no, category_text="BÁO CÁO TIẾN ĐỘ GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ (NHÓM 13)"):
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.11))
        strip.fill.solid()
        strip.fill.fore_color.rgb = ACCENT_BLUE
        strip.line.fill.background()

        cat_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.32), Inches(10.5), Inches(0.3))
        tf_c = cat_box.text_frame
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text
        p_c.font.size = Pt(10.5)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_BLUE

        t_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.62), Inches(11.5), Inches(0.55))
        tf_t = t_box.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_MAIN

        # Footer
        f_box = slide.shapes.add_textbox(Inches(0.65), Inches(7.05), Inches(12.0), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = f"Trường Đại học Công nghệ – ĐHQGHN  |  Nhóm 13: Nguyễn Tuấn Sơn – Vũ Hữu Hoạt                                                                                     Slide {slide_no} / 10"
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, subtitle=None, highlight=False, font_pt=11.5):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE if highlight else CARD_BG
        card.line.color.rgb = ACCENT_BLUE if highlight else CARD_BORDER
        card.line.width = Pt(1.5 if highlight else 1)

        tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(14.5)
        p_title.font.bold = True
        p_title.font.color.rgb = ACCENT_BLUE if highlight else NAVY_MAIN
        p_title.space_after = Pt(3)

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(10.5)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_after = Pt(7)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"•  {it}"
            p_it.font.size = Pt(font_pt)
            p_it.font.color.rgb = TEXT_DARK
            p_it.space_after = Pt(4.5)

    def add_image_frame(slide, img_path, left, top, width, height, caption=None):
        frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        frame.fill.solid()
        frame.fill.fore_color.rgb = WHITE
        frame.line.color.rgb = CARD_BORDER
        frame.line.width = Pt(1.2)

        pad = Inches(0.12)
        cap_h = Inches(0.38) if caption else Inches(0)
        avail_w = width - pad * 2
        avail_h = height - pad * 2 - cap_h

        if os.path.exists(img_path):
            from PIL import Image as PILImage
            with PILImage.open(img_path) as im:
                iw, ih = im.size
            ratio = iw / ih
            box_ratio = avail_w / avail_h
            if ratio > box_ratio:
                pic_w = avail_w
                pic_h = int(avail_w / ratio)
            else:
                pic_h = avail_h
                pic_w = int(avail_h * ratio)
            pic_x = left + pad + int((avail_w - pic_w) / 2)
            pic_y = top + pad + int((avail_h - pic_h) / 2)
            slide.shapes.add_picture(img_path, pic_x, pic_y, width=pic_w, height=pic_h)

        if caption:
            c_box = slide.shapes.add_textbox(left + Inches(0.12), top + height - cap_h - Inches(0.04), width - Inches(0.24), cap_h)
            tf = c_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = caption
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = NAVY_MAIN

    # =========================================================================
    # SLIDE 1: TRANG BÌA (CÓ HÌNH MINI PREVIEW WEB & LINH KIỆN)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_MAIN
    bg1.line.fill.background()

    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(1.0), Inches(0.1), Inches(5.4))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = RGBColor(56, 189, 248)
    dec1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.95), Inches(1.0), Inches(7.2), Inches(5.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ĐẠI HỌC QUỐC GIA HÀ NỘI\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ (UET)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "BÁO CÁO TIẾN ĐỘ GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(251, 191, 36)
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "THIẾT KẾ MÔ HÌNH HỆ THỐNG CỬA BẢO MẬT TÍCH HỢP VÂN TAY AS608, THẺ TỪ RFID RC522, KEYPAD 4x4 & WEB APP"
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "•  Nhóm thực hiện: Nhóm 13\n•  Nguyễn Tuấn Sơn — Phần mềm nhúng ESP32, Web App & Báo cáo\n•  Vũ Hữu Hoạt — Thiết kế phần cứng, Mạch in PCB 2 lớp & Mô hình cơ khí\n\n•  Tiến độ hiện tại: Đã mua đủ 100% linh kiện, hoàn tất vẽ PCB & triển khai Web App trên Vercel"
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(219, 234, 254)

    # Hình preview bên phải trang bìa
    add_image_frame(s1, IMG_WEB, Inches(8.35), Inches(1.05), Inches(4.45), Inches(2.95), "Giao diện Web App đã hoàn thiện")
    add_image_frame(s1, IMG_AS608, Inches(8.35), Inches(4.2), Inches(1.4), Inches(2.15), "Vân tay AS608")
    add_image_frame(s1, IMG_RC522, Inches(9.87), Inches(4.2), Inches(1.4), Inches(2.15), "RFID RC522")
    add_image_frame(s1, IMG_KEYPAD, Inches(11.4), Inches(4.2), Inches(1.4), Inches(2.15), "Keypad 4x4")

    # =========================================================================
    # SLIDE 2: TỔNG QUAN & SƠ ĐỒ KHỐI HỆ THỐNG (NHÚNG IMAGE1.PNG)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Cấu trúc tổng thể hệ thống & Mục tiêu thiết kế", 2)

    add_image_frame(s2, IMG_ARCH, Inches(0.65), Inches(1.35), Inches(6.5), Inches(3.25),
                    "Hình 1.1: Sơ đồ khối tổng thể hệ thống cửa bảo mật tích hợp ESP32 & Web App")

    add_card(s2, Inches(0.65), Inches(4.78), Inches(6.5), Inches(2.1),
             "Điểm cải tiến trong quá trình triển khai thực tế",
             [
                 "Thay thế khối loa thông báo bằng Màn hình tinh thể lỏng LCD 16x2 I2C (0x27) giúp hiển thị trực quan trạng thái khóa, ký tự mật khẩu (*) và hướng dẫn xác thực 2 lớp.",
                 "Nâng cấp bàn phím lên chuẩn Ma trận 4x4 (16 phím vật lý có nắp che bụi) để tận dụng các phím A, B, C, D cho thao tác khóa nhanh và xác nhận."
             ], font_pt=11)

    add_card(s2, Inches(7.35), Inches(1.35), Inches(5.33), Inches(5.53),
             "4 Khối chức năng đồng bộ của đề tài",
             [
                 "Khối Thu thập & Xác thực: Kết hợp 3 phương thức độc lập gồm Cảm biến vân tay quang học AS608 (UART2), Đầu đọc thẻ RFID RC522 (SPI 13.56MHz) và Bàn phím ma trận 4x4.",
                 "Khối Mạch in trung tâm (PCB): Liên kết toàn bộ các module về vi điều khiển ESP32, tích hợp nguồn hạ áp (12V -> 5V/3.3V) và mạch kích khóa chốt kèm Diode chống xung nhiễu.",
                 "Khối Hiển thị & Chấp hành tại cửa: Màn hình LCD 16x2 hiển thị hướng dẫn tại chỗ và Khóa chốt điện từ 12V đóng/mở cửa tự động.",
                 "Khối Giao diện Web App (ESP32 Wi-Fi): Theo dõi trạng thái cửa thời gian thực qua WebSocket, mở khóa từ xa, quản lý danh sách thẻ/vân tay và chuyển đổi bảo mật 1 lớp / 2 lớp (2FA)."
             ],
             subtitle="Sự kết hợp giữa phần cứng cơ điện tử và phần mềm nhúng",
             highlight=True)

    # =========================================================================
    # SLIDE 3: DANH MỤC LINH KIỆN ĐÃ MUA & KHẢO SÁT DATASHEET (NHÚNG 3 ẢNH LINH KIỆN)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Danh mục linh kiện thực tế đã chuẩn bị & Thông số Datasheet", 3)

    # 3 cột có ảnh linh kiện phía trên và thông số kỹ thuật phía dưới
    col_w = Inches(3.85)
    # Cột 1: AS608
    add_image_frame(s3, IMG_AS608, Inches(0.65), Inches(1.35), col_w, Inches(2.55),
                    "Cảm biến vân tay quang học AS608 (Đã mua)")
    add_card(s3, Inches(0.65), Inches(4.02), col_w, Inches(2.85),
             "Thông số Datasheet AS608",
             [
                 "Điện áp cấp: 3.3V – 5.0V DC (Dòng đỉnh < 120mA).",
                 "Giao tiếp: UART TTL (57600 bps) qua Header 6 chân.",
                 "Lưu trữ: Tối đa 127 mẫu vân tay trong Flash nội.",
                 "Thời gian xử lý ảnh & tìm kiếm: < 1.0 giây."
             ], font_pt=11)

    # Cột 2: RFID RC522
    add_image_frame(s3, IMG_RC522, Inches(4.74), Inches(1.35), col_w, Inches(2.55),
                    "Module RFID RC522 13.56MHz + Thẻ S50 (Đã mua)")
    add_card(s3, Inches(4.74), Inches(4.02), col_w, Inches(2.85),
             "Thông số Datasheet RC522",
             [
                 "Nguồn cấp bắt buộc: 3.3V DC (Dòng 13 – 26mA).",
                 "Tần số hoạt động: 13.56 MHz (Đọc thẻ S50 & NFC).",
                 "Giao tiếp: Chuẩn SPI tốc độ cao (10 Mbps).",
                 "Khoảng cách nhận diện thẻ: 0 – 30 mm."
             ], font_pt=11, highlight=True)

    # Cột 3: Keypad 4x4 & Khóa 12V
    add_image_frame(s3, IMG_KEYPAD, Inches(8.83), Inches(1.35), col_w, Inches(2.55),
                    "Bàn phím cứng ma trận có nắp đậy (Đã mua)")
    add_card(s3, Inches(8.83), Inches(4.02), col_w, Inches(2.85),
             "Keypad 4x4, LCD I2C & Khóa 12V",
             [
                 "Bàn phím ma trận 4x4: Phím vật lý độ nảy cao, có nắp che chống bụi, quét 8 chân Hàng – Cột về PCB.",
                 "Màn hình LCD 16x2 I2C: Điện áp 5V, địa chỉ 0x27.",
                 "Khóa chốt điện từ 12V: Dòng kích 0.8A – 1.2A, đóng mở qua Relay/MOSFET có Diode dập xung."
             ], font_pt=11)

    # =========================================================================
    # SLIDE 4: NGHIÊN CỨU GIAO THỨC KẾT NỐI & QUY HOẠCH CHÂN ESP32
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Nghiên cứu giao thức kết nối & Quy hoạch sơ đồ chân ESP32", 4)

    add_card(s4, Inches(0.65), Inches(1.35), Inches(6.2), Inches(5.5),
             "Quy hoạch Sơ đồ chân (Pinout ESP32) đồng bộ PCB",
             [
                 "1. Cảm biến vân tay AS608 (Chuẩn UART2 - 57600 bps):",
                 "    • Chân TX (AS608) -> GPIO 16 (RX2)  |  Chân RX (AS608) -> GPIO 17 (TX2)",
                 "2. Module đọc thẻ RFID RC522 (Chuẩn SPI - Nguồn 3.3V):",
                 "    • SDA(SS): GPIO 5 | SCK: GPIO 18 | MOSI: GPIO 23 | MISO: GPIO 19 | RST: GPIO 4",
                 "3. Màn hình hiển thị LCD 16x2 (Chuẩn I2C - Địa chỉ 0x27):",
                 "    • SDA -> GPIO 21  |  SCL -> GPIO 22",
                 "4. Cơ cấu chấp hành Khóa chốt điện từ 12V:",
                 "    • Tín hiệu kích Relay/MOSFET -> GPIO 2 (Mức HIGH kích mở khóa)",
                 "5. Bàn phím ma trận Keypad 4x4 (8 chân GPIO):",
                 "    • 4 Hàng (R1 -> R4): GPIO 13, 12, 14, 27  |  4 Cột (C1 -> C4): GPIO 26, 25, 33, 32"
             ],
             subtitle="Đã kiểm chứng tránh toàn bộ chân cấm (Strapping Pins & Input-Only Pins)",
             font_pt=11)

    add_card(s4, Inches(7.05), Inches(1.35), Inches(5.63), Inches(5.5),
             "Giải quyết bài toán kỹ thuật khi nghiên cứu Datasheet",
             [
                 "Tránh xung đột chân Input-Only (GPIO 34, 35, 36, 39): Các chân này trên ESP32 không có điện trở kéo lên nội (INPUT_PULLUP). Do đó nhóm quy hoạch Keypad 4x4 vào cụm chân 12..33 để quét ma trận ổn định không cần trở ngoài.",
                 "Bảo vệ mức điện áp 3.3V cho RC522: Datasheet MFRC522 quy định chân VCC tối đa 3.6V. Mạch PCB tách đường nguồn 3.3V riêng cho RC522, tách biệt hoàn toàn với đường 5V của LCD và 12V của khóa chốt.",
                 "Triệt tiêu xung nhiễu cảm ứng từ Khóa chốt 12V: Khi ngắt dòng cuộn hút khóa 12V sẽ sinh ra sức điện động ngược làm treo ESP32. Nhóm bố trí Diode 1N4007 mắc ngược cực song song khóa 12V kết hợp tụ lọc 470uF."
             ],
             subtitle="Đảm bảo tính ổn định công nghiệp khi vận hành thực tế",
             highlight=True, font_pt=11.5)

    # =========================================================================
    # SLIDE 5: KẾT QUẢ THIẾT KẾ MẠCH IN PCB 2 LỚP (NHÚNG ẢNH PCB)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Kết quả thiết kế Sơ đồ nguyên lý & Mạch in PCB (Vũ Hữu Hoạt)", 5)

    add_image_frame(s5, IMG_PCB, Inches(0.65), Inches(1.35), Inches(6.65), Inches(5.5),
                    "Hình 4.1: Sơ đồ bố trí các khối Header kết nối và đường mạch trên PCB trung tâm")

    add_card(s5, Inches(7.5), Inches(1.35), Inches(5.18), Inches(5.5),
             "Chi tiết công việc thiết kế PCB đã hoàn thành",
             [
                 "Khảo sát & Đo đạc chân cắm thực tế: Đã đo chuẩn khoảng cách pitch 2.54mm của các cụm Header 6 chân (AS608), 8 chân (RC522), 8 chân (Keypad 4x4), 4 chân (LCD I2C) và Domino nguồn 12V.",
                 "Hoàn thiện Sơ đồ nguyên lý (Schematic): Liên kết toàn bộ các khối về ESP32, tích hợp khối nguồn hạ áp Buck 12V -> 5V/3.3V và tầng kích khóa chốt.",
                 "Thiết kế Layout PCB 2 lớp:",
                 "    • Đường mạch công suất 12V cấp cho khóa điện được đi dây độ rộng lớn (> 40 mil) chịu dòng 1.5A.",
                 "    • Phủ đồng mặt Mass (GND Copper Pour) cả 2 lớp giúp chống nhiễu sóng Wi-Fi và RFID 13.56MHz.",
                 "    • Đã kiểm tra DRC (Design Rule Check) không còn lỗi và sẵn sàng gia công hàn mạch ở Giai đoạn 3."
             ],
             subtitle="Phụ trách chính: Vũ Hữu Hoạt",
             highlight=True, font_pt=11)

    # =========================================================================
    # SLIDE 6: KIẾN TRÚC FIRMWARE ESP32 & BẢO MẬT ĐA CẤP ĐỘ 1 LỚP / 2FA
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Kiến trúc Firmware ESP32 & Cơ chế Bảo mật 1 Lớp / 2 Lớp (2FA)", 6)

    add_card(s6, Inches(0.65), Inches(1.35), Inches(5.8), Inches(5.5),
             "Kiến trúc Phần mềm nhúng ESP32 (PlatformIO)",
             [
                 "Vòng lặp Non-blocking (Không chặn):",
                 "    • Không sử dụng delay() dài gây đơ phím; dùng millis() quét Keypad 4x4 liên tục (< 5ms) và quét AS608/RC522 mỗi 80ms.",
                 "Hệ thống tệp Flash LittleFS bền vững:",
                 "    • Lưu trữ toàn bộ file giao diện Web (index.html, style.css, app.js) và cơ sở dữ liệu config.json ngay trong bộ nhớ Flash 4MB của ESP32.",
                 "    • Mất điện không bị mất mật khẩu PIN, danh sách thẻ RFID hay ID vân tay.",
                 "Giao thức WebSocket (/ws) & mDNS:",
                 "    • Đồng bộ trạng thái cửa và màn hình LCD 16x2 lên trình duyệt dưới 100ms.",
                 "    • Tích hợp tên miền nội bộ http://smartdoor.local."
             ],
             subtitle="Phụ trách chính: Nguyễn Tuấn Sơn", font_pt=11.5)

    add_card(s6, Inches(6.68), Inches(1.35), Inches(6.0), Inches(5.5),
             "Cơ chế Bảo mật Đa cấp độ (1 Lớp & 2FA) mới phát triển",
             [
                 "Chế độ 1 Lớp (Single-Factor): Quét Vân tay đúng HOẶC Thẻ RFID đúng HOẶC nhập đúng PIN Keypad 4x4 là mở cửa ngay.",
                 "Chế độ 2 Lớp (Two-Factor Authentication - 2FA): Yêu cầu xác thực thành công 2 bước liên tiếp trong thời gian quy định:",
                 "    • Chế độ 2: Vân tay AS608  +  Mã PIN Keypad 4x4",
                 "    • Chế độ 3: Thẻ từ RFID RC522  +  Mã PIN Keypad 4x4",
                 "    • Chế độ 4: Vân tay AS608  +  Thẻ từ RFID RC522",
                 "Cơ chế chống treo phiên (Session Timeout 15 giây):",
                 "    • Khi qua Lớp 1, màn hình LCD hiển thị 'XAC THUC LOP 1 OK - NHAP PIN + #'. Nếu quá 15 giây không hoàn thành Lớp 2 hoặc nhập sai, hệ thống tự hủy phiên và khóa an toàn."
             ],
             subtitle="Nâng cao tính bảo mật cho phòng thí nghiệm & khu vực quan trọng",
             highlight=True, font_pt=11.5)

    # =========================================================================
    # SLIDE 7: KẾT QUẢ XÂY DỰNG GIAO DIỆN WEB APP (NHÚNG ẢNH WEB DASHBOARD)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Kết quả xây dựng Giao diện Web App Quản lý (Nguyễn Tuấn Sơn)", 7)

    add_image_frame(s7, IMG_WEB, Inches(0.65), Inches(1.35), Inches(7.35), Inches(5.5),
                    "Hình 6.1: Giao diện Web App thực tế (Thiết kế tối giản Shadcn UI, rõ ràng, dễ thao tác)")

    add_card(s7, Inches(8.2), Inches(1.35), Inches(4.48), Inches(5.5),
             "Các tính năng đã hoàn thiện trên Web",
             [
                 "1. Bảng điều khiển (Dashboard):",
                 "    • Hiển thị trạng thái khóa 12V trực quan & đếm ngược thời gian tự đóng.",
                 "    • Nút nhấn Mở khóa từ xa & Khóa khẩn cấp qua Wi-Fi.",
                 "    • Màn hình LCD 16x2 Live Mirror phản chiếu chính xác từng dòng chữ tại cửa.",
                 "2. Nhật ký lịch sử ra vào:",
                 "    • Ghi nhận Thời gian thực, Phương thức, Tên người dùng, Trạng thái Hợp lệ/Từ chối.",
                 "    • Hỗ trợ lọc theo phương thức và Xuất file .CSV phục vụ báo cáo.",
                 "3. Quản lý Vân tay & Thẻ RFID:",
                 "    • Đăng ký mẫu vân tay mới và Quét thêm thẻ RFID trực tiếp từ giao diện Web."
             ],
             subtitle="Hoạt động trên cả Điện thoại & Máy tính",
             highlight=True, font_pt=10.8)

    # =========================================================================
    # SLIDE 8: TRIỂN KHAI TÊN MIỀN VERCEL & BỘ GIẢ LẬP PHẦN CỨNG (NHÚNG ẢNH VERCEL)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Triển khai Cloud Vercel & Bộ giả lập phần cứng kiểm thử", 8)

    add_image_frame(s8, IMG_VERCEL, Inches(0.65), Inches(1.35), Inches(7.35), Inches(5.5),
                    "Hình 7.1: Hệ thống mã nguồn trên GitHub đã được triển khai thành công lên tên miền Vercel")

    add_card(s8, Inches(8.2), Inches(1.35), Inches(4.48), Inches(5.5),
             "Kiểm thử độc lập & Tên miền truy cập",
             [
                 "Kho mã nguồn GitHub của nhóm:",
                 "    • github.com/tuansonuet197/smartdoor-nhom13",
                 "Tên miền Web App trực tuyến (Vercel):",
                 "    • smartdoor-nhom13-data.vercel.app",
                 "Tên miền cục bộ khi chạy trên ESP32:",
                 "    • http://smartdoor.local (mDNS)",
                 "Bộ giả lập phần cứng (Draggable Simulator):",
                 "    • Tích hợp sẵn bảng giả lập kéo-thả tự do trên góc màn hình Web.",
                 "    • Cho phép bấm thử Bàn phím 4x4 ảo, giả lập quét Vân tay đúng/sai, quẹt Thẻ RFID đúng/lạ để kiểm chứng toàn bộ luồng logic 1 lớp & 2FA trước khi hàn mạch."
             ],
             subtitle="Sẵn sàng chạy Demo trực tiếp ngay trong buổi báo cáo",
             highlight=True, font_pt=11)

    # =========================================================================
    # SLIDE 9: BẢNG TIẾN ĐỘ THỰC HIỆN & PHÂN CHIA CÔNG VIỆC
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Đánh giá tiến độ thực hiện so với kế hoạch đề ra", 9)

    add_card(s9, Inches(0.65), Inches(1.35), Inches(5.9), Inches(2.6),
             "Giai đoạn 1 (Tuần 1 – 2): Khảo sát & Mua linh kiện  [ĐÃ HOÀN THÀNH 100%]",
             [
                 "Chốt sơ đồ tổng thể hệ thống cửa bảo mật 3 phương thức xác thực + Web App.",
                 "Mua đầy đủ 100% linh kiện: Cảm biến vân tay AS608, RFID RC522 + thẻ S50/NFC, Keypad 4x4 có nắp đậy, màn hình LCD I2C, ESP32, Khóa chốt 12V và linh kiện nguồn."
             ], highlight=True, font_pt=11)

    add_card(s9, Inches(6.78), Inches(1.35), Inches(5.9), Inches(2.6),
             "Giai đoạn 2 (Tuần 3 – 4): Thiết kế PCB & Web App  [ĐÃ HOÀN THÀNH 100%]",
             [
                 "Vũ Hữu Hoạt: Đã nghiên cứu datasheet, đo chân linh kiện, hoàn thành vẽ sơ đồ nguyên lý (Schematic) và Layout mạch in PCB 2 lớp.",
                 "Nguyễn Tuấn Sơn: Đã lập trình xong bộ mã nguồn ESP32 (PlatformIO), hoàn thiện giao diện Web App tích hợp bảo mật 2 lớp (2FA) và đưa lên tên miền Vercel."
             ], highlight=True, font_pt=11)

    add_card(s9, Inches(0.65), Inches(4.2), Inches(5.9), Inches(2.65),
             "Giai đoạn 3 (Tuần 5 – 6): Gia công mạch & Tích hợp  [DỰ KIẾN TIẾP THEO]",
             [
                 "Vũ Hữu Hoạt: Gia công ăn mòn/đặt in mạch PCB, hàn linh kiện, đo kiểm tra khối nguồn hạ áp 12V -> 5V/3.3V và dựng khung mô hình cửa cơ khí.",
                 "Nguyễn Tuấn Sơn: Nạp code và hệ thống file LittleFS lên mạch ESP32 thực tế, hiệu chỉnh độ nhạy cảm biến AS608 và RC522 trên bo mạch."
             ], font_pt=11)

    add_card(s9, Inches(6.78), Inches(4.2), Inches(5.9), Inches(2.65),
             "Giai đoạn 4 (Tuần 7 – 8): Lắp đặt hoàn thiện & Báo cáo  [DỰ KIẾN]",
             [
                 "Lắp đặt toàn bộ bo mạch PCB, khóa chốt 12V, LCD, Keypad 4x4, AS608, RC522 lên khung mô hình cửa hoàn chỉnh.",
                 "Kiểm thử thực nghiệm các kịch bản bảo mật 1 lớp / 2 lớp, trích xuất file CSV lịch sử ra vào và hoàn thiện cuốn Báo cáo đồ án Cơ Điện Tử."
             ], font_pt=11)

    # =========================================================================
    # SLIDE 10: KẾT LUẬN GIỮA KỲ & DEMO TRỰC TIẾP
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Tổng kết báo cáo giữa kỳ & Trình chiếu Demo Web App", 10)

    add_card(s10, Inches(0.65), Inches(1.35), Inches(6.2), Inches(5.5),
             "Tóm tắt các kết quả đạt được tính đến giữa kỳ",
             [
                 "1. Về linh kiện vật tư: Đã chuẩn bị đầy đủ 100% các module cảm biến và cơ cấu chấp hành theo đúng danh mục đề tài.",
                 "2. Về nghiên cứu lý thuyết & mạch điện: Đã làm chủ datasheet, giao thức UART2 / SPI / I2C / Matrix Scanning và hoàn thành bản vẽ mạch in PCB trung tâm.",
                 "3. Về phần mềm & Web App: Đã hoàn thiện sớm hơn tiến độ (vừa có Firmware C++ cho ESP32, vừa có Web App tối giản hỗ trợ bảo mật 1 lớp & 2FA).",
                 "4. Sẵn sàng chuyển sang Giai đoạn 3 (Gia công hàn mạch PCB và lắp dựng cơ khí khung cửa)."
             ],
             subtitle="Đảm bảo 100% tiến độ theo kế hoạch học phần",
             highlight=True, font_pt=12)

    add_image_frame(s10, IMG_WEB, Inches(7.05), Inches(1.35), Inches(5.63), Inches(3.8),
                    "Demo trực tiếp tại: https://smartdoor-nhom13-data.vercel.app")

    add_card(s10, Inches(7.05), Inches(5.3), Inches(5.63), Inches(1.55),
             "Cảm ơn Thầy/Cô và các bạn đã lắng nghe!",
             [
                 "Nhóm 13 xin phép chuyển sang phần Demo trực tiếp giao diện Web App & Chế độ bảo mật 2 lớp trên trình duyệt và nhận ý kiến đóng góp của Thầy/Cô."
             ], font_pt=11.5)

    out_path = r"d:\WORKING PLACE\DoAn\slide_baocao\BaoCao_GiuaKy_Nhom13.pptx"
    prs.save(out_path)
    print("Successfully generated visual PPTX at:", out_path)

if __name__ == "__main__":
    create_presentation()
