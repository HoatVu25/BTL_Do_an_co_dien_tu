# BÁO CÁO TIẾN ĐỘ GIỮA KỲ — ĐỒ ÁN CƠ ĐIỆN TỬ
## ĐỀ TÀI: THIẾT KẾ MÔ HÌNH HỆ THỐNG CỬA BẢO MẬT TÍCH HỢP SINH TRẮC HỌC VÂN TAY, THẺ TỪ RFID VÀ BÀN PHÍM MA TRẬN
**Nhóm sinh viên thực hiện (Nhóm 13):**
* Nguyễn Tuấn Sơn (Phụ trách Lập trình nhúng ESP32, Giao diện Web App & Báo cáo)
* Vũ Hữu Hoạt (Phụ trách Phần cứng, Thiết kế PCB & Mô hình Cơ khí)

---

### SLIDE 1: TRANG TIÊU ĐỀ
* **Tiêu đề lớn:** THIẾT KẾ MÔ HÌNH HỆ THỐNG CỬA BẢO MẬT ĐA PHƯƠNG THỨC XÁC THỰC TÍCH HỢP GIÁM SÁT REALTIME QUA WEB APP
* **Phụ đề:** Báo cáo tiến độ đồ án giữa kỳ — Ngành Công nghệ Kỹ thuật Cơ điện tử (UET - ĐHQGHN)
* **Thông tin nhóm:** Nhóm 13 (Nguyễn Tuấn Sơn - Vũ Hữu Hoạt)
* **Thời gian:** Học kỳ I, Năm học 2026 - 2027

---

### SLIDE 2: TỔNG QUAN ĐỀ TÀI & MỤC TIÊU NGHIÊN CỨU
* **Bối cảnh thực tế:** Nhu cầu kiểm soát an ninh tại các khu vực làm việc, văn phòng và phòng thí nghiệm đòi hỏi độ tin cậy cao, khả năng giám sát linh hoạt và dự phòng đa phương thức xác thực khi có sự cố sinh trắc học hoặc mất thẻ vật lý.
* **Mục tiêu kỹ thuật cốt lõi:**
  1. Tích hợp đồng bộ 3 phương thức xác thực cục bộ tại cửa: Vân tay quang học (AS608), Thẻ từ RFID (RC522) và Mật mã bàn phím ma trận 4x4.
  2. Xây dựng cơ chế an ninh đa cấp độ: Chế độ 1 lớp (Single Auth) và chế độ 2 lớp (2FA: Vân tay + PIN, RFID + PIN, Vân tay + RFID) kèm cơ chế Timeout 15 giây chống treo phiên.
  3. Xây dựng Web App điều khiển và giám sát thời gian thực nhúng trực tiếp vào Flash LittleFS của ESP32 qua WebSocket, đồng thời triển khai bản demo đám mây trên Vercel.
  4. Thiết kế mạch in PCB trung tâm tối ưu kích thước, tích hợp khối nguồn cách ly xung nhiễu và tầng công suất kích khóa chốt điện từ 12V.

---

### SLIDE 3: CẤU TRÚC TỔNG THỂ HỆ THỐNG (SYSTEM ARCHITECTURE)
* **Khối Thu thập & Xác thực (Inputs):**
  * Cảm biến vân tay quang học AS608: Chuẩn truyền thông UART TTL (57600 bps), lưu trữ mẫu vân tay trực tiếp trong bộ nhớ cảm biến (ID 1-127).
  * Module đọc thẻ RFID RC522: Tần số chuẩn 13.56 MHz, giao tiếp tốc độ cao qua bus SPI (nguồn chuẩn 3.3V).
  * Bàn phím ma trận 4x4: Quét ma trận 4 hàng x 4 cột (8 GPIO), hỗ trợ các phím chức năng `A, B, C, D`, `*` (xóa buffer), `#` (xác nhận mở cửa).
* **Khối Xử lý Trung tâm (Controller):**
  * ESP32-WROOM-32: Dual-core 240 MHz, Wi-Fi 802.11 b/g/n, quản lý State Machine điều khiển không chặn (Non-blocking).
* **Khối Phản hồi & Chấp hành (Outputs):**
  * Màn hình LCD 16x2 qua giao tiếp I2C (địa chỉ 0x27): Hiển thị trạng thái cửa, hướng dẫn thao tác nhập mã PIN và đếm ngược thời gian.
  * Mạch kích khóa chốt điện từ 12V: Điều khiển qua Relay/MOSFET cách ly kèm Diode dập xung ngược (Flyback 1N4007).
* **Khối Giám sát & Quản trị (Network / Software):**
  * Web Server bất đồng bộ (ESPAsyncWebServer) & WebSocket Server (`/ws`): Phản xạ sự kiện hai chiều thời gian thực dưới 100ms.
  * Bộ nhớ Flash LittleFS: Lưu trữ cơ sở dữ liệu JSON (`config.json`, nhật ký ra vào, danh sách thẻ và vân tay).

---

### SLIDE 4: TỔNG HỢP LINH KIỆN & KHẢO SÁT DATASHEET CHI TIẾT
* **Bảng thông số kỹ thuật linh kiện đã chuẩn bị:**
  * ESP32 Dev Kit V1 (30 pins): Nguồn 5V Micro-USB / 5V Vin, dòng hoạt động 80-240 mA.
  * Module AS608 Optical Fingerprint: Điện áp hoạt động 3.3V - 5V DC, dòng đỉnh < 120mA, thời gian nhận dạng < 1.0 giây, FAR < 0.001%, FRR < 0.1%.
  * Module RFID RC522: Điện áp cấp tuyệt đối 3.3V DC (không chịu mức 5V), dòng tiêu thụ 13-26 mA, khoảng cách đọc thẻ 0-30 mm.
  * Bàn phím ma trận cơ 4x4 (16 phím vật lý): Điện trở tiếp điểm < 100 Ohm, tuổi thọ bấm > 1 triệu lần.
  * Màn hình LCD 16x2 + Module I2C PCF8574: Tiết kiệm chân từ 16 chân LCD còn 2 chân I2C (SDA/SCL).
  * Khóa chốt điện từ 12V (Fail-Secure / Thường đóng): Điện áp danh định 12V DC, dòng cuộn hút 0.8A - 1.2A khi kích mở.

---

### SLIDE 5: THIẾT KẾ MẠCH NGUYÊN LÝ & PHÂN BỔ CHÂN (PINOUT ESP32)
* **Quy hoạch chân GPIO tránh xung đột Bootloader & Strapping Pins:**
  * Cảm biến vân tay AS608: `GPIO 16 (RX2)`, `GPIO 17 (TX2)` (sử dụng HardwareSerial UART2 độc lập).
  * Module RFID RC522: `GPIO 5 (SS)`, `GPIO 18 (SCK)`, `GPIO 23 (MOSI)`, `GPIO 19 (MISO)`, `GPIO 4 (RST)`.
  * Màn hình LCD 16x2: `GPIO 21 (SDA)`, `GPIO 22 (SCL)`.
  * Khóa chốt điện từ 12V: `GPIO 2` (điều khiển mức logic tích cực).
  * Bàn phím ma trận 4x4 (8 chân):
    * Hàng R1 -> R4: `GPIO 13, 12, 14, 27` (cấu hình `INPUT_PULLUP`).
    * Cột C1 -> C4: `GPIO 26, 25, 33, 32` (quét mức LOW tuần tự).
* **Biện pháp chống nhiễu phần cứng:**
  * Hạ áp từ nguồn 12V xuống 5V và 3.3V bằng module nguồn tuyến tính/switching độc lập để chống sụt áp khi khóa chốt 12V hút dòng.
  * Bố trí tụ hóa lọc nguồn 470uF và tụ gốm 100nF gần chân VCC các module.
  * Tầng đệm cách ly quang (Optocoupler) hoặc Diode dập xung 1N4007 mắc song song ngược cực với cuộn dây khóa 12V để triệt tiêu điện áp cảm ứng $V = -L \frac{di}{dt}$ gây reset vi điều khiển.

---

### SLIDE 6: TIẾN ĐỘ THIẾT KẾ MẠCH IN PCB (VŨ HỮU HOẠT)
* **Kết quả thực hiện:**
  * Đã hoàn thiện sơ đồ nguyên lý (Schematic) liên kết toàn bộ 5 khối chức năng trên phần mềm thiết kế mạch.
  * Đã đo đạc kích thước thực tế chân cắm (Footprint) của AS608, RC522, Header Keypad 4x4 và Domino cấp nguồn 12V.
  * Đã hoàn thành bản vẽ Layout PCB 2 lớp:
    * Đường mạch công suất cấp cho khóa 12V được phủ đồng kích thước lớn (width > 40 mil) đảm bảo dẫn dòng 1.5A an toàn.
    * Phủ mass toàn bộ 2 mặt (GND Copper Pour) để giảm thiểu nhiễu điện từ tần số cao từ module Wi-Fi ESP32 và module RFID 13.56 MHz.
  * Trạng thái hiện tại: Đã xuất file Gerber và gửi gia công mạch in.

---

### SLIDE 7: XÂY DỰNG PHẦN MỀM NHÚNG ESP32 & QUẢN TRỊ BỘ NHỚ (NGUYỄN TUẤN SƠN)
* **Kiến trúc phần mềm Non-blocking:**
  * Loại bỏ hoàn toàn hàm chặn `delay()`, sử dụng `millis()` để lập lịch tuần tự cho việc quét bàn phím 4x4 (tần số liên tục), quét cảm biến RFID và vân tay (chu kỳ 80ms) và kiểm tra timeout cửa.
* **Hệ thống tệp LittleFS & Lưu trữ dữ liệu bền vững:**
  * Khởi tạo phân vùng LittleFS để nạp trọn bộ giao diện Web (HTML, CSS, JS) và cơ sở dữ liệu cấu hình `config.json`.
  * Cơ chế tự phục hồi: Khi mất nguồn điện đột ngột, toàn bộ danh sách thẻ RFID, mẫu ID vân tay và mã PIN đã đổi đều được bảo toàn.
* **Đồng bộ thời gian thực qua mDNS & WebSocket:**
  * Tích hợp giao thức mDNS: Cho phép người dùng truy cập trực tiếp bằng tên miền nội bộ `http://smartdoor.local` mà không cần ghi nhớ địa chỉ IP cục bộ.
  * Xử lý WebSocket 2 chiều: Truyền nhận sự kiện dạng gói tin JSON siêu nhẹ, giảm tải cho CPU của ESP32.

---

### SLIDE 8: CƠ CHẾ BẢO MẬT ĐA CẤP ĐỘ (1 LỚP VÀ 2FA)
* **Chế độ 1 lớp (Single-Factor Authentication):**
  * Người dùng xác thực hợp lệ bằng 1 trong 3 phương thức: Vân tay, Thẻ RFID hoặc Mã PIN -> Cửa lập tức mở khóa.
* **Chế độ 2 lớp (Two-Factor Authentication - 2FA):**
  * Tùy chọn 1: Vân tay AS608 + Mã PIN Keypad 4x4.
  * Tùy chọn 2: Thẻ từ RFID RC522 + Mã PIN Keypad 4x4.
  * Tùy chọn 3: Thẻ từ RFID RC522 + Vân tay AS608.
* **Luồng xử lý phiên 2FA:**
  * Lớp 1 hợp lệ -> Khóa chưa mở, màn hình LCD và Web hiển thị *"XAC THUC LOP 1 OK"* kèm chỉ dẫn lớp tiếp theo.
  * Kích hoạt bộ đếm thời gian Timeout 15 giây.
  * Nếu hoàn thành lớp 2 đúng -> Cửa mở, ghi nhận log `2FA`. Nếu quá 15s hoặc nhập sai -> Hủy phiên, trả về trạng thái khóa an toàn.

---

### SLIDE 9: GIAO DIỆN WEB APP QUẢN LÝ THỜI GIAN THỰC
* **Thiết kế theo chuẩn Shadcn / Minimalist Monochrome:**
  * Tối ưu hóa trải nghiệm người dùng, sử dụng tông màu trung tính sạch sẽ, dễ nhìn, hiển thị sắc nét trên cả điện thoại di động và máy tính.
* **Các phân hệ chức năng trên Web App:**
  1. *Dashboard Trung tâm:* Theo dõi trạng thái khóa 12V trực quan, nút mở khóa từ xa một chạm, màn hình LCD 16x2 phản chiếu thời gian thực (Live Mirror) và bảng thống kê KPI.
  2. *Nhật ký Lịch sử (Access Logs):* Tự động đẩy sự kiện mới lên đầu bảng, bộ lọc thông minh theo từng phương thức và nút xuất file báo cáo `.CSV`.
  3. *Quản trị Vân tay & Thẻ RFID:* Thêm mới vân tay (hướng dẫn đặt ngón tay 2 lần), tính năng "Quét thẻ nhanh từ RC522" và xóa quyền truy cập.
  4. *Cấu hình Hệ thống:* Chuyển đổi linh hoạt giữa 1 lớp / 2 lớp, đổi mã PIN Keypad, chỉnh thời gian giữ mở khóa.
* **Triển khai Đám mây (Cloud Deployment):**
  * Đã kết nối kho mã nguồn GitHub và triển khai hoạt động ổn định trên nền tảng Vercel tại địa chỉ: `https://smartdoor-nhom13-data.vercel.app`.
  * Tích hợp sẵn bộ giả lập phần cứng kéo thả (Draggable Simulator) phục vụ demo và kiểm thử trực quan.

---

### SLIDE 10: TỔNG KẾT TIẾN ĐỘ GIỮA KỲ & KẾ HOẠCH GIAI ĐOẠN TIẾP THEO
* **Đánh giá tiến độ giữa kỳ:** Đạt 100% mục tiêu giai đoạn 1 và giai đoạn 2 đề ra trong đề cương.
  * Phần cứng: Đã mua đủ 100% linh kiện, đo đạc chân cắm và hoàn thành vẽ Schematic/Layout PCB.
  * Phần mềm & Web: Hoàn thành 100% cấu trúc Web App, firmware ESP32, cơ chế 2FA và triển khai thành công lên Vercel.
* **Kế hoạch giai đoạn 2 (Tuần 5 - Tuần 8):**
  * Nhận mạch in PCB gia công, tiến hành hàn linh kiện và đo kiểm tra nguồn cách ly.
  * Gia công khung mô hình cửa cơ khí, gá lắp khóa chốt 12V, cảm biến AS608, đầu đọc RC522, bàn phím 4x4 và LCD.
  * Ghép nối phần mềm với phần cứng hoàn chỉnh, kiểm thử độ ổn định và đo đạc thời gian đáp ứng thực tế.
  * Tổng hợp số liệu thực nghiệm và hoàn thiện báo cáo thuyết minh đồ án chuẩn UET.
