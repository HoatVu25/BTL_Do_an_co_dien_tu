# HỆ THỐNG CỬA BẢO MẬT ĐA PHƯƠNG THỨC & GIÁM SÁT QUA WEB APP (IoT)

> **Môn học:** Đồ án Cơ Điện Tử — Trường Đại học Công nghệ (VNU - UET)  
> **Nhóm thực hiện:** Nhóm 13  
> **Thành viên:**
> - **Nguyễn Tuấn Sơn** — Phụ trách Firmware ESP32, Web App Dashboard & Triển khai Cloud
> - **Vũ Hữu Hoạt** — Phụ trách Thiết kế sơ đồ nguyên lý phần cứng, Bo mạch PCB 2 lớp & Cơ khí

---

## 📌 1. Giới Thiệu Đề Tài

Hệ thống khóa cửa thông minh được xây dựng nhằm nâng cao độ an toàn và tiện lợi cho người dùng gia đình hoặc văn phòng. Hệ thống kết hợp nhiều phương thức xác thực sinh trắc học và thẻ từ, đồng thời kết nối Wi-Fi để đồng bộ dữ liệu trạng thái và điều khiển từ xa qua giao diện Web.

### Các tính năng chính:
- **Xác thực đa phương thức:**
  - Cảm biến vân tay quang học AS608 (lưu trữ tới 300 mẫu, UART).
  - Đầu đọc thẻ từ RFID-RC522 (tần số 13.56 MHz, giao thức SPI).
  - Bàn phím ma trận 4x4 nhập mã PIN bảo mật có nắp che.
  - Màn hình LCD 16x2 I2C hiển thị thông báo và hướng dẫn thao tác.
- **Bảo mật 2 lớp (2-Factor Authentication - 2FA):**
  - Cơ chế an ninh nâng cao yêu cầu đồng thời Thẻ/Vân tay + Mã PIN.
  - Bộ đếm thời gian an toàn (Timeout 15 giây): Tự động hủy phiên nếu không hoàn thành bước 2.
  - Cơ chế chống dò mật khẩu (Brute-force): Khóa hệ thống tạm thời khi nhập sai quá 3 lần.
- **Điều khiển & Giám sát qua Web App:**
  - Giám sát trạng thái Đóng/Mở cửa thời gian thực.
  - Xem nhật ký ra vào (Access Logs) lưu vết thời gian và phương thức xác thực.
  - Nút bấm mở cửa từ xa qua Internet (triển khai trên Vercel Cloud).
- **Phần cứng bảo vệ an toàn:**
  - Mạch công suất điều khiển Relay kích hoạt chốt khóa từ 12V.
  - Sử dụng Diode dập xung ngược (Flyback Diode 1N4007) và Optocoupler bảo vệ vi điều khiển ESP32.

---

## 📂 2. Cấu Trúc Thư Mục Dự Án

```
├── data/                    # Giao diện Web App điều khiển (HTML, CSS, JS)
│   ├── index.html           # Trang Dashboard giám sát
│   ├── app.js               # Xử lý logic và API đồng bộ
│   └── style.css            # Giao diện tối giản hiện đại (Shadcn UI style)
├── include/                 # Header files cấu hình chân GPIO và thư viện
├── src/                     # Mã nguồn Firmware vi điều khiển ESP32
│   └── main.cpp             # Logic điều khiển chính, state machine non-blocking
├── platformio.ini           # Cấu hình biên dịch PlatformIO cho ESP32 DevKit
├── vercel.json              # Cấu hình triển khai Web App lên Vercel Cloud
└── README.md                # Tài liệu tổng quan dự án
```

---

## 🛠️ 3. Sơ Đồ Kết Nối Phần Cứng (ESP32 30-Pin)

| Linh kiện / Module | Giao thức / Loại tín hiệu | Chân ESP32 tương ứng | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Vân tay AS608** | UART (HardwareSerial) | TX ➔ GPIO 16, RX ➔ GPIO 17 | Tốc độ Baud 57600 |
| **RFID RC522** | SPI Bus | SCK: 18, MISO: 19, MOSI: 23, SDA: 5, RST: 22 | Nguồn cấp 3.3V chuẩn |
| **Màn hình LCD 16x2** | I2C | SDA: GPIO 21, SCL: GPIO 22 | Địa chỉ I2C `0x27` qua module PCF8574 |
| **Relay Khóa 12V** | Digital Output | Signal: GPIO 4 | Kèm Diode 1N4007 dập xung ngược |
| **Bàn phím 4x4** | Matrix Scanning | GPIO 13, 12, 14, 27, 26, 25, 33, 32 | Quét ma trận hàng - cột |

---

## 🚀 4. Hướng Dẫn Nạp Code & Chạy Thử Nghiệm

### Nạp Firmware cho ESP32:
1. Cài đặt tiện ích mở rộng [PlatformIO IDE](https://platformio.org/) trên VS Code.
2. Mở thư mục gốc của dự án.
3. Kết nối ESP32 qua cáp Micro-USB và nhấn nút **Upload** (`Ctrl + Alt + U`).

---

## 🌐 5. Web App Trực Tuyến

Giao diện Web App điều khiển và mô phỏng đã được triển khai tại:  
👉 **[https://smartdoor-nhom13-data.vercel.app](https://smartdoor-nhom13-data.vercel.app)**
