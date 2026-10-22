import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Bảng màu UET Academic / Minimalist
    NAVY_MAIN   = RGBColor(11, 35, 71)      # #0B2347 - Xanh Navy UET
    ACCENT_BLUE = RGBColor(16, 85, 154)     # #10559A - Xanh đậm điểm nhấn
    CARD_BG     = RGBColor(245, 247, 250)   # #F5F7FA - Xám nhạt nền thẻ
    CARD_BORDER = RGBColor(220, 226, 235)   # #DCE2EB - Viền thẻ
    TEXT_DARK   = RGBColor(24, 30, 42)      # #181E2A - Chữ chính
    TEXT_MUTED  = RGBColor(100, 110, 125)   # #646E7D - Chữ phụ
    WHITE       = RGBColor(255, 255, 255)
    GREEN_OK    = RGBColor(16, 140, 78)     # #108C4E - Điểm nhấn thành công
    AMBER_WARN  = RGBColor(190, 110, 10)    # #BE6E0A - Điểm nhấn tiến độ

    def add_header(slide, title_text, category_text="BÁO CÁO TIẾN ĐỘ GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ"):
        # Dải màu trang trí phía trên
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = ACCENT_BLUE
        strip.line.fill.background()

        # Category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_BLUE

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_MAIN

    def add_card(slide, left, top, width, height, title, items, subtitle=None, highlight=False):
        # Card Background Box
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE if highlight else CARD_BG
        card.line.color.rgb = ACCENT_BLUE if highlight else CARD_BORDER
        card.line.width = Pt(1.5 if highlight else 1)

        # Text Frame
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = ACCENT_BLUE if highlight else NAVY_MAIN
        p_title.space_after = Pt(4)

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_after = Pt(8)

        # Items
        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"•  {it}"
            p_it.font.size = Pt(12)
            p_it.font.color.rgb = TEXT_DARK
            p_it.space_after = Pt(5)

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_MAIN
    bg1.line.fill.background()

    # Dải màu trang trí
    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = RGBColor(60, 160, 240)
    dec1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.2), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ – ĐHQGHN  |  KHOA CƠ HỌC KỸ THUẬT VÀ TỰ ĐỘNG HÓA"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 210, 245)
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "BÁO CÁO TIẾN ĐỘ GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 200, 80)
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "THIẾT KẾ MÔ HÌNH HỆ THỐNG CỬA BẢO MẬT ĐA PHƯƠNG THỨC XÁC THỰC"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "Tích hợp Sinh trắc học Vân tay AS608, Thẻ từ RFID RC522, Keypad 4x4 & Giám sát Web App ESP32"
    p.font.size = Pt(17)
    p.font.color.rgb = RGBColor(220, 235, 255)
    p.space_after = Pt(36)

    p = tf1.add_paragraph()
    p.text = "Nhóm thực hiện: Nhóm 13\n•  Nguyễn Tuấn Sơn  —  Phần mềm nhúng ESP32, Giao diện Web App & Báo cáo kỹ thuật\n•  Vũ Hữu Hoạt        —  Thiết kế phần cứng, Vẽ mạch in PCB & Mô hình Cơ khí"
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(200, 220, 245)

    # =========================================================================
    # SLIDE 2: TỔNG QUAN & MỤC TIÊU
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Tổng quan đề tài & Mục tiêu nghiên cứu")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Đặt vấn đề thực tế",
             [
                 "Hệ thống khóa cơ học truyền thống tiềm ẩn nguy cơ sao chép chìa khóa và thiếu hoàn toàn khả năng ghi vết nhật ký ra vào.",
                 "Các hệ thống cửa chỉ dùng 1 phương thức (chỉ thẻ hoặc chỉ mật mã) dễ gặp rủi ro khi rơi thẻ, lộ mật mã hoặc ngón tay bị trầy xước.",
                 "Giải pháp đề xuất: Xây dựng hệ thống bảo mật đa phương thức tại chỗ (Local Authentication) kết hợp đồng bộ Web App thời gian thực qua mạng Wi-Fi cục bộ."
             ],
             subtitle="Lý do lựa chọn đề tài nghiên cứu")

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Mục tiêu kỹ thuật cốt lõi",
             [
                 "Tích hợp đồng bộ 3 phương thức xác thực: Vân tay quang học (AS608), Thẻ từ RFID (RC522) và Bàn phím ma trận 4x4.",
                 "Linh hoạt 2 cấp độ bảo mật: Chế độ 1 lớp (mở nhanh) và chế độ 2 lớp (2FA: Vân tay + PIN, Thẻ + PIN, Vân tay + Thẻ).",
                 "Thiết kế mạch in PCB 2 lớp: Tối ưu chống nhiễu nguồn và tích hợp mạch điều khiển kích khóa chốt 12V an toàn.",
                 "Nhúng Web App quản lý trực tiếp lên ESP32: Không cần máy chủ trung gian, cập nhật trạng thái cửa và nhật ký dưới 100ms qua WebSocket."
             ],
             subtitle="Chỉ tiêu kỹ thuật cần đạt được",
             highlight=True)

    # =========================================================================
    # SLIDE 3: CẤU TRÚC HỆ THỐNG
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Cấu trúc tổng thể hệ thống (System Architecture)")

    w3 = Inches(3.65)
    h3 = Inches(5.2)
    add_card(s3, Inches(0.8), Inches(1.6), w3, h3,
             "Khối Thu thập & Xác thực",
             [
                 "Cảm biến vân tay quang học AS608: Giao tiếp UART TTL (57600 bps), lưu 127 vân tay.",
                 "Đầu đọc thẻ RFID RC522: Tần số 13.56 MHz, giao tiếp bus SPI, đọc thẻ S50 và móc khóa NFC.",
                 "Bàn phím ma trận cơ 4x4: Quét ma trận 4 hàng x 4 cột (8 GPIO), hỗ trợ phím chức năng A, B, C, D, *, #."
             ],
             subtitle="Thiết bị ngoại vi tại cửa")

    add_card(s3, Inches(4.8), Inches(1.6), w3, h3,
             "Khối Xử lý & Phản hồi",
             [
                 "Vi điều khiển trung tâm ESP32: Dual-core 240 MHz, xử lý State Machine không chặn (Non-blocking).",
                 "Màn hình LCD 16x2 (I2C 0x27): Hiển thị phản hồi tức thì cho người dùng tại cửa.",
                 "Cơ cấu chấp hành Khóa chốt 12V: Kích mở qua Relay/MOSFET kèm Diode 1N4007 dập xung ngược."
             ],
             subtitle="Xử lý trung tâm & Chấp hành",
             highlight=True)

    add_card(s3, Inches(8.8), Inches(1.6), w3, h3,
             "Khối Giám sát & Quản trị",
             [
                 "Web Server & WebSocket Server: Nhúng trực tiếp trong Flash LittleFS của ESP32.",
                 "Tên miền nội bộ mDNS (smartdoor.local): Truy cập nhanh không cần nhớ địa chỉ IP.",
                 "Đám mây demo Vercel: Triển khai giao diện trực tuyến phục vụ kiểm thử và báo cáo từ xa."
             ],
             subtitle="Mạng & Ứng dụng điều khiển")

    # =========================================================================
    # SLIDE 4: KHẢO SÁT LINH KIỆN & DATASHEET
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Khảo sát linh kiện & Phân tích Datasheet chi tiết")

    w4 = Inches(5.6)
    h4 = Inches(2.45)
    add_card(s4, Inches(0.8), Inches(1.6), w4, h4,
             "Cảm biến vân tay quang học AS608",
             [
                 "Điện áp cấp: 3.3V – 5.0V DC; Dòng đỉnh: < 120 mA.",
                 "Giao tiếp: UART TTL (baudrate 57600 bps mặc định).",
                 "Độ phân giải: 500 DPI, thời gian đối sánh mẫu: < 1.0 giây."
             ])

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), h4,
             "Module đọc thẻ từ RFID-RC522",
             [
                 "Điện áp hoạt động: 3.3V DC (Tuyệt đối không cấp 5V gây hỏng chip).",
                 "Tần số sóng mang: 13.56 MHz; Chuẩn giao tiếp: SPI tốc độ cao.",
                 "Dòng tiêu thụ: 13 – 26 mA; Khoảng cách đọc: 0 – 30 mm."
             ])

    add_card(s4, Inches(0.8), Inches(4.35), w4, h4,
             "Bàn phím ma trận 4x4 & LCD I2C",
             [
                 "Keypad 4x4: 16 phím cơ độ nảy cao, chống bụi bẩn, 8 chân hàng-cột.",
                 "Màn hình LCD 16x2 + Ba lô PCF8574: Tiết kiệm từ 16 chân còn 2 chân I2C.",
                 "Điện áp cấp LCD: 5V DC đảm bảo độ tương phản rõ nét."
             ])

    add_card(s4, Inches(6.8), Inches(4.35), Inches(5.7), h4,
             "Vi điều khiển ESP32 & Khóa chốt 12V",
             [
                 "ESP32-WROOM-32: Bộ nhớ Flash 4MB, tích hợp Wi-Fi 2.4GHz & Bluetooth.",
                 "Khóa chốt điện từ 12V: Dòng kích cuộn dây 0.8A – 1.0A (Fail-Secure).",
                 "Bảo vệ quá áp: Sử dụng Diode dập xung ngược 1N4007 song song cuộn hút."
             ])

    # =========================================================================
    # SLIDE 5: SƠ ĐỒ NGUYÊN LÝ & QUY HOẠCH CHÂN PINOUT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Quy hoạch sơ đồ chân ESP32 & Giải pháp chống nhiễu")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.2),
             "Bảng phân bổ chân GPIO trên ESP32",
             [
                 "Cảm biến AS608: RX2 -> GPIO 16, TX2 -> GPIO 17 (HardwareSerial2 độc lập).",
                 "RFID RC522 (SPI): SS -> GPIO 5, SCK -> GPIO 18, MOSI -> GPIO 23, MISO -> GPIO 19, RST -> GPIO 4.",
                 "Màn hình LCD 16x2: SDA -> GPIO 21, SCL -> GPIO 22 (Chuẩn I2C mặc định).",
                 "Khóa chốt điện 12V: Kích mở qua GPIO 2 (Logic HIGH kích mở).",
                 "Bàn phím ma trận 4x4 (8 chân GPIO):",
                 "    • Hàng R1 – R4: GPIO 13, 12, 14, 27 (cấu hình INPUT_PULLUP)",
                 "    • Cột C1 – C4: GPIO 26, 25, 33, 32 (quét mức LOW tuần tự)",
                 "Nguyên tắc: Không sử dụng các chân GPIO 34-39 (chỉ đọc) và các chân Strapping (GPIO 0, 15) để tránh lỗi khởi động nạp firmware."
             ],
             subtitle="Tránh xung đột chân Bootloader & Strapping Pins")

    add_card(s5, Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.2),
             "Giải pháp thiết kế chống xung nhiễu",
             [
                 "Tách tầng nguồn công suất & vi điều khiển: Nguồn tổng 12V cấp khóa chốt; hạ áp 5V cấp ESP32/LCD; hạ áp 3.3V cấp riêng cho RC522.",
                 "Xử lý sụt áp cuộn cảm: Bố trí tụ hóa 470uF và tụ gốm 100nF lọc nguồn tức thời khi khóa 12V đóng ngắt.",
                 "Dập xung điện áp ngược cảm ứng: Mắc Diode 1N4007 song song ngược cực với khóa 12V để triệt tiêu điện áp e = -L(di/dt).",
                 "Cách ly quang: Sử dụng Optocoupler kích Relay/MOSFET giúp vi điều khiển ESP32 không bị reset khi tải cảm hoạt động."
             ],
             subtitle="Đảm bảo hệ thống hoạt động ổn định 24/7",
             highlight=True)

    # =========================================================================
    # SLIDE 6: TIẾN ĐỘ THIẾT KẾ MẠCH IN PCB
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Tiến độ thiết kế mạch in PCB (Phụ trách: Vũ Hữu Hoạt)")

    w6 = Inches(5.6)
    h6 = Inches(5.2)
    add_card(s6, Inches(0.8), Inches(1.6), w6, h6,
             "Kết quả thiết kế Schematic & Layout PCB",
             [
                 "Đo đạc chính xác kích thước chân cắm (Footprint): Đo khoảng cách header 6 chân của AS608, 8 chân RC522, 8 chân Keypad 4x4 và cọc đấu dây Domino 12V.",
                 "Hoàn thiện bản vẽ nguyên lý (Schematic): Kết nối đầy đủ các khối chức năng, tích hợp IC hạ áp nguồn, tụ lọc và transistor công suất.",
                 "Vẽ Layout mạch in 2 lớp (Double-layer PCB):",
                 "    • Đường mạch công suất cấp khóa 12V được thiết kế bản rộng (> 40 mil), chịu dòng tức thời đến 2A an toàn.",
                 "    • Phủ mass toàn bộ 2 mặt (GND Copper Pouring) để triệt tiêu nhiễu cao tần phát sinh từ module Wi-Fi và sóng RFID 13.56 MHz.",
                 "    • Các đường tín hiệu SPI và UART đi song song khoảng cách hợp lý, giảm tối đa hiện tượng xuyên âm (Crosstalk)."
             ],
             subtitle="Tối ưu kích thước & Khả năng tản nhiệt")

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), h6,
             "Trạng thái phần cứng & Kế hoạch chế tạo",
             [
                 "Trạng thái linh kiện: 100% linh kiện đã được mua đủ và kiểm tra thông mạch (AS608, RC522, Keypad 4x4, LCD I2C, ESP32, Khóa 12V).",
                 "Trạng thái PCB: Đã hoàn tất kiểm tra quy tắc thiết kế (DRC) và xuất trọn bộ file Gerber gia công.",
                 "Kế hoạch triển khai sau giữa kỳ:",
                 "    • Nhận mạch in PCB gia công từ nhà máy.",
                 "    • Hàn gắn linh kiện, đo kiểm tra điện áp các điểm test point (12V, 5V, 3.3V).",
                 "    • Gia công cơ khí khung mô hình cửa gỗ/mica, gá lắp khóa chốt và cảm biến."
             ],
             subtitle="Sẵn sàng cho giai đoạn lắp ráp hoàn thiện",
             highlight=True)

    # =========================================================================
    # SLIDE 7: PHẦN MỀM NHÚNG ESP32
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Xây dựng phần mềm nhúng ESP32 (Phụ trách: Nguyễn Tuấn Sơn)")

    w7 = Inches(5.6)
    h7 = Inches(5.2)
    add_card(s7, Inches(0.8), Inches(1.6), w7, h7,
             "Kiến trúc lập trình Non-blocking",
             [
                 "Loại bỏ hoàn toàn hàm chặn delay(): Sử dụng kỹ thuật định thời millis() và máy trạng thái hữu hạn (Finite State Machine).",
                 "Phân phối chu kỳ quét cảm biến hợp lý:",
                 "    • Quét ma trận Keypad 4x4: Thực thi liên tục theo từng chu kỳ vòng lặp, độ trễ nhận phím < 5ms.",
                 "    • Quét RFID và Vân tay AS608: Thực thi theo chu kỳ định thời 80ms, tránh nghẽn CPU.",
                 "    • Đếm ngược đóng cửa tự động: Xử lý chạy nền song song với việc giữ kết nối WebSocket."
             ],
             subtitle="Đảm bảo hệ thống phản hồi mượt mà không treo đơ")

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), h7,
             "Quản lý bộ nhớ Flash LittleFS & Kết nối",
             [
                 "Phân vùng Flash LittleFS:",
                 "    • Lưu trữ toàn bộ mã nguồn Web App tĩnh (HTML, CSS, JS) nén trực tiếp vào Flash.",
                 "    • Quản lý cơ sở dữ liệu dạng JSON (config.json) lưu mật khẩu PIN, danh sách UID thẻ và ID vân tay.",
                 "Bảo toàn dữ liệu khi mất điện: Mọi thay đổi cấu hình từ Web App hoặc Keypad được ghi trực tiếp vào LittleFS, khởi động lại không bị mất.",
                 "Tên miền nội bộ mDNS (smartdoor.local): Người dùng chỉ cần gõ http://smartdoor.local là mở Web App ngay trong mạng Wi-Fi."
             ],
             subtitle="Lưu trữ bền vững & Truy cập tiện lợi",
             highlight=True)

    # =========================================================================
    # SLIDE 8: CƠ CHẾ BẢO MẬT ĐA CẤP ĐỘ (1 LỚP & 2 LỚP)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Cơ chế bảo mật đa cấp độ (Xác thực 1 lớp & 2FA)")

    w8 = Inches(5.6)
    h8 = Inches(5.2)
    add_card(s8, Inches(0.8), Inches(1.6), w8, h8,
             "Chế độ Xác thực 1 lớp (Single Auth)",
             [
                 "Nguyên lý vận hành: Người dùng chỉ cần xác thực thành công 1 trong 3 phương thức là cửa mở ngay lập tức.",
                 "Phương thức hỗ trợ:",
                 "    • Quét Vân tay AS608 hợp lệ (khớp mẫu trong bộ nhớ ID 1–127).",
                 "    • Quẹt Thẻ từ RFID RC522 hợp lệ (khớp mã UID trong cơ sở dữ liệu).",
                 "    • Nhập đúng mã PIN trên Bàn phím ma trận 4x4 rồi nhấn phím # hoặc D.",
                 "Ứng dụng: Phù hợp cho môi trường gia đình, văn phòng thông thường cần thao tác ra vào nhanh chóng."
             ],
             subtitle="Tối ưu sự tiện lợi & Tốc độ mở cửa")

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), h8,
             "Chế độ Xác thực 2 lớp (Two-Factor Authentication)",
             [
                 "Tùy chọn đa dạng cấu hình trực tiếp từ Web App:",
                 "    1. Vân tay AS608 + Mã PIN Keypad 4x4",
                 "    2. Thẻ từ RFID RC522 + Mã PIN Keypad 4x4",
                 "    3. Vân tay AS608 + Thẻ từ RFID RC522",
                 "Quy trình xử lý phiên 2FA an toàn:",
                 "    • Bước 1: Người dùng xác thực lớp 1 đúng -> Khóa chưa mở, màn hình LCD và Web hiển thị yêu cầu thực hiện tiếp lớp 2.",
                 "    • Bước 2: Kích hoạt bộ đếm thời gian Timeout 15 giây. Nếu nhập đúng lớp 2 -> Mở khóa. Nếu quá 15s hoặc sai -> Hủy phiên ngay lập tức."
             ],
             subtitle="Bảo vệ khu vực trọng yếu & Phòng thí nghiệm",
             highlight=True)

    # =========================================================================
    # SLIDE 9: GIAO DIỆN WEB APP QUẢN LÝ
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Giao diện Web App quản lý & Triển khai đám mây")

    w9 = Inches(5.6)
    h9 = Inches(5.2)
    add_card(s9, Inches(0.8), Inches(1.6), w9, h9,
             "Thiết kế giao diện hiện đại (Shadcn/Vercel)",
             [
                 "Phong cách thiết kế tối giản: Tông màu sáng đơn sắc (Monochrome Light Theme), sử dụng hệ font chuẩn Inter và icon vector nét mảnh.",
                 "4 Phân hệ chức năng hoàn chỉnh:",
                 "    • Tổng quan: Trạng thái khóa cửa thời gian thực, nút mở từ xa, màn hình LCD 16x2 phản chiếu (Live Mirror).",
                 "    • Nhật ký ra vào: Ghi nhận thời gian, phương thức, kết quả hợp lệ/từ chối, bộ lọc và xuất file báo cáo CSV.",
                 "    • Quản lý vân tay & RFID: Đăng ký mẫu vân tay mới, đọc thẻ nhanh từ RC522, xóa từng người dùng.",
                 "    • Cấu hình hệ thống: Chuyển đổi 1 lớp / 2 lớp, đổi mã PIN Keypad, chỉnh thời gian mở."
             ],
             subtitle="Trực quan, dễ dùng trên cả Smartphone & Laptop")

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), h9,
             "Triển khai trực tuyến & Bộ giả lập phần cứng",
             [
                 "Triển khai thành công trên nền tảng Vercel:",
                 "    • Địa chỉ truy cập trực tuyến: https://smartdoor-nhom13-data.vercel.app",
                 "    • Đồng bộ liên tục qua kho mã nguồn GitHub: tuansonuet197/smartdoor-nhom13.",
                 "Bộ giả lập phần cứng tích hợp sẵn (Draggable Simulator):",
                 "    • Hỗ trợ kéo thả tự do trên màn hình để không che bảng điều khiển.",
                 "    • Cho phép giả lập quét vân tay đúng/sai, quẹt thẻ RFID và bàn phím 4x4 ảo để kiểm thử toàn diện quy trình 2FA ngay cả khi chưa cắm mạch."
             ],
             subtitle="Sẵn sàng trình chiếu demo trực tiếp tại buổi báo cáo",
             highlight=True)

    # =========================================================================
    # SLIDE 10: TỔNG KẾT TIẾN ĐỘ & KẾ HOẠCH
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Tổng kết tiến độ giữa kỳ & Kế hoạch giai đoạn 2")

    w10 = Inches(5.6)
    h10 = Inches(5.2)
    add_card(s10, Inches(0.8), Inches(1.6), w10, h10,
             "Đánh giá kết quả giai đoạn giữa kỳ (Đạt 100%)",
             [
                 "Khảo sát & Chuẩn bị linh kiện: Đã mua đủ 100% linh kiện chính và phụ trợ (ESP32, AS608, RC522, Keypad 4x4, LCD I2C, Khóa 12V).",
                 "Nghiên cứu kỹ thuật: Nắm vững tập lệnh UART của AS608, giao thức SPI của RC522, cơ chế dập xung khóa điện 12V.",
                 "Thiết kế mạch in PCB: Hoàn thành 100% Schematic và Layout PCB 2 lớp, đã xuất file Gerber gửi xưởng gia công.",
                 "Phần mềm & Web App: Hoàn thành 100% firmware nhúng Non-blocking, cơ chế bảo mật 2FA, giao diện Web App và deploy thành công lên Vercel."
             ],
             subtitle="Hoàn thành đúng tiến độ Tuần 1 – Tuần 4")

    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), h10,
             "Kế hoạch triển khai nửa cuối học kỳ (Tuần 5 – Tuần 8)",
             [
                 "Tuần 5: Nhận mạch in PCB gia công, tiến hành hàn linh kiện, đo kiểm tra ổn định điện áp 12V, 5V, 3.3V và tầng công suất kích khóa.",
                 "Tuần 6: Gia công khung mô hình cửa cơ khí, gá lắp khóa chốt điện, đầu đọc vân tay, thẻ từ, bàn phím và màn hình LCD hoàn thiện.",
                 "Tuần 7: Nạp firmware tích hợp, kiểm thử hoạt động liên tục 24/7, đo đạc độ trễ nhận dạng và tinh chỉnh thuật toán.",
                 "Tuần 8: Thu thập số liệu thực nghiệm, hoàn thiện báo cáo thuyết minh đồ án chuẩn học thuật UET và chuẩn bị slide bảo vệ tốt nghiệp."
             ],
             subtitle="Lộ trình đưa mô hình vào hoạt động thực tế",
             highlight=True)

    # Save
    out_path = r"d:\WORKING PLACE\DoAn\slide_baocao\BaoCao_GiuaKy_Nhom13.pptx"
    prs.save(out_path)
    print(f"Successfully generated PowerPoint presentation at: {out_path}")

if __name__ == "__main__":
    create_presentation()
