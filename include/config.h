#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ============================================================================
// 1. CẤU HÌNH KẾT NỐI WI-FI & NTP TIME
// ============================================================================
#define WIFI_SSID           "SmartDoor_WiFi"      // Đổi tên Wi-Fi nhà/trường của bạn
#define WIFI_PASSWORD       "12345678"            // Đổi mật khẩu Wi-Fi
#define AP_FALLBACK_SSID    "SmartDoor_Nhom13"    // Phát Wi-Fi riêng nếu không kết nối được
#define AP_FALLBACK_PASS    "12345678"
#define MDNS_HOSTNAME       "smartdoor"           // Truy cập bằng tên miền: http://smartdoor.local

#define NTP_SERVER          "pool.ntp.org"
#define GMT_OFFSET_SEC      (7 * 3600)            // Múi giờ Việt Nam (GMT+7)
#define DAYLIGHT_OFFSET_SEC 0

// ============================================================================
// 2. QUY HOẠCH SƠ ĐỒ CHÂN (PINOUT ESP32) - CHUẨN CHO THIẾT KẾ MẠCH PCB
// ============================================================================

// --- Khối 1: Cảm biến vân tay quang học AS608 (Giao tiếp UART2) ---
#define FP_RX_PIN           16  // Nối với chân TX của AS608
#define FP_TX_PIN           17  // Nối với chân RX của AS608
#define FP_BAUDRATE         57600

// --- Khối 2: Module đọc thẻ từ RFID RC522 (Giao tiếp SPI - Nguồn 3.3V) ---
#define RFID_SS_PIN         5   // Chân SDA (SS)
#define RFID_SCK_PIN        18  // Chân SCK
#define RFID_MOSI_PIN       23  // Chân MOSI
#define RFID_MISO_PIN       19  // Chân MISO
#define RFID_RST_PIN        4   // Chân RST

// --- Khối 3: Màn hình hiển thị LCD 16x2 / 20x4 I2C ---
#define LCD_SDA_PIN         21
#define LCD_SCL_PIN         22
#define LCD_I2C_ADDR        0x27 // Địa chỉ phổ biến: 0x27 hoặc 0x3F
#define LCD_COLS            16
#define LCD_ROWS            2

// --- Khối 4: Cơ cấu chấp hành Khóa chốt điện từ 12V (Qua Relay / MOSFET) ---
#define LOCK_RELAY_PIN      2   // Kích mức HIGH để mở khóa
#define RELAY_ACTIVE_HIGH   true

// --- Khối 5: Bàn phím ma trận Keypad 4x4 (8 chân GPIO) ---
#define KEYPAD_ROWS         4
#define KEYPAD_COLS         4

// 4 Chân Hàng (Rows R1 -> R4)
#define KP_ROW1_PIN         13
#define KP_ROW2_PIN         12
#define KP_ROW3_PIN         14
#define KP_ROW4_PIN         27

// 4 Chân Cột (Cols C1 -> C4)
#define KP_COL1_PIN         26
#define KP_COL2_PIN         25
#define KP_COL3_PIN         33
#define KP_COL4_PIN         32

// ============================================================================
// 3. HẰNG SỐ MẶC ĐỊNH HỆ THỐNG
// ============================================================================
#define DEFAULT_PIN_CODE            "123456"
#define DEFAULT_UNLOCK_TIME_SEC     5
#define DEFAULT_MAX_WRONG_ATTEMPTS  5
#define DEFAULT_LOCKOUT_TIME_SEC    30
#define MAX_LOG_ENTRIES             50

#endif // CONFIG_H
