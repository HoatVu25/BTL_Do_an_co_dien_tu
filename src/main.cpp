/**
 * ĐỀ TÀI: THIẾT KẾ MÔ HÌNH HỆ THỐNG CỬA BẢO MẬT TÍCH HỢP VÂN TAY AS608, RFID RC522, KEYPAD 4x4 & LCD
 * NHÓM 13: NGUYỄN TUẤN SƠN - VŨ HỮU HOẠT
 *
 * File: src/main.cpp
 * Chức năng:
 *  - Giao tiếp đồng thời Cảm biến vân tay AS608 (UART2), Thẻ từ RFID RC522 (SPI),
 *    Bàn phím ma trận Keypad 4x4 (8 GPIO), Màn hình LCD 16x2 (I2C) và Khóa điện 12V.
 *  - Khởi chạy Web App cục bộ từ bộ nhớ Flash LittleFS qua ESPAsyncWebServer.
 *  - Đồng bộ thời gian thực 2 chiều giữa Cửa <-> Trình duyệt Web qua WebSocket (/ws).
 */

#include <Arduino.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <DNSServer.h>
#include <LittleFS.h>
#include <Wire.h>
#include <SPI.h>
#include <time.h>

#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>
#include <Adafruit_Fingerprint.h>
#include <MFRC522.h>
#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

#include "config.h"

// ============================================================================
// 1. KHỞI TẠO ĐỐI TƯỢNG PHẦN CỨNG & WEB SERVER
// ============================================================================
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

LiquidCrystal_I2C lcd(LCD_I2C_ADDR, LCD_COLS, LCD_ROWS);
MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);
HardwareSerial fpSerial(2); // UART2 (RX=16, TX=17)
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fpSerial);

// Ma trận bàn phím 4x4 (16 phím)
char keyMap[KEYPAD_ROWS][KEYPAD_COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}
};
byte rowPins[KEYPAD_ROWS] = {KP_ROW1_PIN, KP_ROW2_PIN, KP_ROW3_PIN, KP_ROW4_PIN};
byte colPins[KEYPAD_COLS] = {KP_COL1_PIN, KP_COL2_PIN, KP_COL3_PIN, KP_COL4_PIN};
Keypad keypad = Keypad(makeKeymap(keyMap), rowPins, colPins, KEYPAD_ROWS, KEYPAD_COLS);

// ============================================================================
// 2. BIẾN TRẠNG THÁI HỆ THỐNG (STATE MACHINE KHÔNG CHẶN)
// ============================================================================
struct RfidEntry {
    String uid;
    String name;
    String addedAt;
};

struct FpEntry {
    int id;
    String name;
    String addedAt;
};

struct LogEntry {
    String time;
    String method;
    String user;
    bool valid;
};

String currentPinCode = DEFAULT_PIN_CODE;
int unlockDurationSec = DEFAULT_UNLOCK_TIME_SEC;
int maxWrongAttempts = DEFAULT_MAX_WRONG_ATTEMPTS;

bool isDoorUnlocked = false;
unsigned long doorUnlockStartMs = 0;
unsigned long lastSensorPollMs = 0;

String keypadInputBuffer = "";
int wrongAttemptCount = 0;

// Chế độ học thẻ RFID mới & Đăng ký vân tay mới từ Web
bool rfidLearnMode = false;
bool fpEnrollActive = false;
int fpEnrollTargetId = 0;
String fpEnrollTargetName = "";

std::vector<RfidEntry> rfidList;
std::vector<FpEntry> fpList;
std::vector<LogEntry> accessLogs;

// ============================================================================
// 3. HÀM TIỆN ÍCH THỜI GIAN & HIỂN THỊ LCD
// ============================================================================
String getCurrentTimeStr() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo, 50)) {
        unsigned long sec = millis() / 1000;
        char buf[24];
        snprintf(buf, sizeof(buf), "Uptime %02lu:%02lu:%02lu", sec / 3600, (sec % 3600) / 60, sec % 60);
        return String(buf);
    }
    char buf[25];
    strftime(buf, sizeof(buf), "%d/%m/%Y %H:%M:%S", &timeinfo);
    return String(buf);
}

void updateLcd(const String& line1, const String& line2) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(line1.substring(0, 16));
    lcd.setCursor(0, 1);
    lcd.print(line2.substring(0, 16));

    // Phản chiếu đồng thời lên màn hình LCD ảo trên Web App
    JsonDocument doc;
    doc["type"] = "LCD_UPDATE";
    doc["line1"] = line1;
    doc["line2"] = line2;
    String out;
    serializeJson(doc, out);
    ws.textAll(out);
}

// ============================================================================
// 4. LƯU & ĐỌC CẤU HÌNH TỪ BỘ NHỚ FLASH (LITTLEFS)
// ============================================================================
void loadConfigFromFlash() {
    if (!LittleFS.exists("/config.json")) return;
    File file = LittleFS.open("/config.json", "r");
    if (!file) return;

    JsonDocument doc;
    if (deserializeJson(doc, file) == DeserializationError::Ok) {
        currentPinCode = doc["pinCode"] | DEFAULT_PIN_CODE;
        unlockDurationSec = doc["unlockDurationSec"] | DEFAULT_UNLOCK_TIME_SEC;
        maxWrongAttempts = doc["maxWrongAttempts"] | DEFAULT_MAX_WRONG_ATTEMPTS;

        rfidList.clear();
        for (JsonObject card : doc["rfidCards"].as<JsonArray>()) {
            rfidList.push_back({
                card["uid"].as<String>(),
                card["name"].as<String>(),
                card["addedAt"].as<String>()
            });
        }

        fpList.clear();
        for (JsonObject fp : doc["fingerprints"].as<JsonArray>()) {
            fpList.push_back({
                fp["id"].as<int>(),
                fp["name"].as<String>(),
                fp["addedAt"].as<String>()
            });
        }
    }
    file.close();
}

void saveConfigToFlash() {
    File file = LittleFS.open("/config.json", "w");
    if (!file) return;

    JsonDocument doc;
    doc["pinCode"] = currentPinCode;
    doc["unlockDurationSec"] = unlockDurationSec;
    doc["maxWrongAttempts"] = maxWrongAttempts;

    JsonArray cards = doc["rfidCards"].to<JsonArray>();
    for (const auto& c : rfidList) {
        JsonObject obj = cards.add<JsonObject>();
        obj["uid"] = c.uid;
        obj["name"] = c.name;
        obj["addedAt"] = c.addedAt;
    }

    JsonArray fps = doc["fingerprints"].to<JsonArray>();
    for (const auto& f : fpList) {
        JsonObject obj = fps.add<JsonObject>();
        obj["id"] = f.id;
        obj["name"] = f.name;
        obj["addedAt"] = f.addedAt;
    }

    serializeJsonPretty(doc, file);
    file.close();
}

// ============================================================================
// 5. ĐIỀU KHIỂN KHÓA CHỐT ĐIỆN TỪ 12V & GHI NHẬT KÝ SỰ KIỆN
// ============================================================================
void setLockHardware(bool unlock) {
    isDoorUnlocked = unlock;
    if (unlock) {
        doorUnlockStartMs = millis();
        digitalWrite(LOCK_RELAY_PIN, RELAY_ACTIVE_HIGH ? HIGH : LOW);
    } else {
        digitalWrite(LOCK_RELAY_PIN, RELAY_ACTIVE_HIGH ? LOW : HIGH);
    }
}

void broadcastFullState() {
    JsonDocument doc;
    doc["type"] = "FULL_SYNC";
    doc["doorUnlocked"] = isDoorUnlocked;
    doc["unlockDurationSec"] = unlockDurationSec;

    JsonObject cfg = doc["config"].to<JsonObject>();
    cfg["pinCode"] = currentPinCode;
    cfg["unlockDurationSec"] = unlockDurationSec;
    cfg["maxWrongAttempts"] = maxWrongAttempts;

    JsonArray cards = doc["rfidCards"].to<JsonArray>();
    for (const auto& c : rfidList) {
        JsonObject o = cards.add<JsonObject>();
        o["uid"] = c.uid;
        o["name"] = c.name;
        o["addedAt"] = c.addedAt;
    }

    JsonArray fps = doc["fingerprints"].to<JsonArray>();
    for (const auto& f : fpList) {
        JsonObject o = fps.add<JsonObject>();
        o["id"] = f.id;
        o["name"] = f.name;
        o["addedAt"] = f.addedAt;
    }

    JsonArray logs = doc["logs"].to<JsonArray>();
    for (const auto& l : accessLogs) {
        JsonObject o = logs.add<JsonObject>();
        o["time"] = l.time;
        o["method"] = l.method;
        o["user"] = l.user;
        o["valid"] = l.valid;
    }

    String out;
    serializeJson(doc, out);
    ws.textAll(out);
}

void triggerAccessEvent(const String& method, const String& user, bool valid, const String& lcd1, const String& lcd2) {
    LogEntry entry = {getCurrentTimeStr(), method, user, valid};
    accessLogs.insert(accessLogs.begin(), entry);
    if (accessLogs.size() > MAX_LOG_ENTRIES) {
        accessLogs.pop_back();
    }

    if (valid) {
        wrongAttemptCount = 0;
        setLockHardware(true);
    } else {
        wrongAttemptCount++;
    }

    updateLcd(lcd1, lcd2);

    JsonDocument doc;
    doc["type"] = "ACCESS_EVENT";
    doc["method"] = method;
    doc["user"] = user;
    doc["valid"] = valid;
    doc["lcd1"] = lcd1;
    doc["lcd2"] = lcd2;
    String out;
    serializeJson(doc, out);
    ws.textAll(out);
}

// ============================================================================
// 6. QUÉT BÀN PHÍM MA TRẬN KEYPAD 4x4
// ============================================================================
void handleKeypad4x4() {
    char key = keypad.getKey();
    if (!key) return;

    if (key == '*') {
        keypadInputBuffer = "";
        updateLcd("NHAP MAT KHAU:", "DA XOA BUFFER");
        return;
    }

    if (key == 'C') {
        keypadInputBuffer = "";
        setLockHardware(false);
        updateLcd(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
        broadcastFullState();
        return;
    }

    if (key == '#' || key == 'D') {
        if (keypadInputBuffer.length() == 0) return;
        String entered = keypadInputBuffer;
        keypadInputBuffer = "";

        if (entered == currentPinCode) {
            triggerAccessEvent("KEYPAD", "Nhập đúng PIN từ Keypad 4x4", true, "MAT KHAU DUNG!", "MO CUA KEYPAD");
        } else {
            triggerAccessEvent("KEYPAD", "Nhập sai PIN từ Keypad 4x4", false, "SAI MAT KHAU!", "VUI LONG THU LAI");
        }
        return;
    }

    if (key == 'A' || key == 'B') {
        updateLcd(String("PHIM CHUC NANG ") + key, "NHAP PIN + #");
        return;
    }

    if (keypadInputBuffer.length() < 8) {
        keypadInputBuffer += key;
        String masked = "";
        for (size_t i = 0; i < keypadInputBuffer.length(); i++) masked += "*";
        updateLcd("NHAP MAT KHAU:", "PIN: " + masked);
    }
}

// ============================================================================
// 7. QUÉT THẺ TỪ RFID RC522 (SPI)
// ============================================================================
void handleRfidRc522() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) return;

    String uidStr = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        if (i > 0) uidStr += ":";
        if (rfid.uid.uidByte[i] < 0x10) uidStr += "0";
        uidStr += String(rfid.uid.uidByte[i], HEX);
    }
    uidStr.toUpperCase();

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    // Nếu Web App đang bật chế độ "Đọc thẻ mới từ RC522"
    if (rfidLearnMode) {
        rfidLearnMode = false;
        updateLcd("DA DOC MA THE!", uidStr);
        JsonDocument doc;
        doc["type"] = "RFID_SCANNED_LEARN";
        doc["uid"] = uidStr;
        String out;
        serializeJson(doc, out);
        ws.textAll(out);
        return;
    }

    // Kiểm tra UID trong danh sách hợp lệ
    for (const auto& card : rfidList) {
        if (card.uid == uidStr) {
            triggerAccessEvent("RFID", card.name + " (" + uidStr + ")", true, "THE TU HOP LE", card.name);
            return;
        }
    }

    triggerAccessEvent("RFID", "Thẻ lạ (" + uidStr + ")", false, "THE KHONG HOP LE", uidStr);
}

// ============================================================================
// 8. QUÉT & ĐĂNG KÝ VÂN TAY QUANG HỌC AS608 (UART2)
// ============================================================================
void sendFpStatus(const String& msg, bool done = false) {
    JsonDocument doc;
    doc["type"] = "FP_ENROLL_STATUS";
    doc["message"] = msg;
    doc["done"] = done;
    String out;
    serializeJson(doc, out);
    ws.textAll(out);
}

void processFingerprintEnrollBlocking(int id, const String& name) {
    sendFpStatus("Bước 1: Đặt ngón tay lên cảm biến AS608...", false);
    updateLcd("DANG KY ID #" + String(id), "DAT NGON TAY 1..");

    unsigned long t0 = millis();
    while (finger.getImage() != FINGERPRINT_OK) {
        if (millis() - t0 > 10000) {
            sendFpStatus("Hết thời gian chờ đặt ngón tay!", true);
            updateLcd("LOI DANG KY!", "HET THOI GIAN");
            return;
        }
        delay(50);
    }

    if (finger.image2Tz(1) != FINGERPRINT_OK) {
        sendFpStatus("Ảnh vân tay mờ, vui lòng thử lại!", true);
        return;
    }

    sendFpStatus("Bước 2: Nhấc ngón tay ra rồi đặt lại lần 2...", false);
    updateLcd("NHAC TAY RA...", "ROI DAT LAN 2");
    delay(1500);

    t0 = millis();
    while (finger.getImage() != FINGERPRINT_OK) {
        if (millis() - t0 > 10000) {
            sendFpStatus("Hết thời gian chờ lần 2!", true);
            return;
        }
        delay(50);
    }

    if (finger.image2Tz(2) != FINGERPRINT_OK ||
        finger.createModel() != FINGERPRINT_OK ||
        finger.storeModel(id) != FINGERPRINT_OK) {
        sendFpStatus("Hai lần đặt tay không khớp, vui lòng thử lại!", true);
        updateLcd("LOI DANG KY!", "KHONG KHOP MAU");
        return;
    }

    fpList.push_back({id, name, getCurrentTimeStr()});
    saveConfigToFlash();
    sendFpStatus("Đăng ký vân tay ID #" + String(id) + " thành công!", true);
    updateLcd("LUU THANH CONG!", "ID #" + String(id) + " OK");
    broadcastFullState();
}

void handleFingerprintAs608() {
    if (finger.getImage() != FINGERPRINT_OK) return;

    if (finger.image2Tz() != FINGERPRINT_OK || finger.fingerFastSearch() != FINGERPRINT_OK) {
        triggerAccessEvent("FINGERPRINT", "Vân tay không khớp AS608", false, "VAN TAY SAI!", "TU CHOI MO CUA");
        return;
    }

    int foundId = finger.fingerID;
    String userName = "ID #" + String(foundId);
    for (const auto& f : fpList) {
        if (f.id == foundId) {
            userName = f.name + " (ID #" + String(foundId) + ")";
            break;
        }
    }

    triggerAccessEvent("FINGERPRINT", userName, true, "VAN TAY HOP LE", "ID #" + String(foundId) + " MOI VAO");
}

// ============================================================================
// 9. XỬ LÝ LỆNH WEBSOCKET TỪ GIAO DIỆN WEB APP
// ============================================================================
void onWsEvent(AsyncWebSocket* server, AsyncWebSocketClient* client, AwsEventType type,
               void* arg, uint8_t* data, size_t len) {
    if (type == WS_EVT_CONNECT) {
        broadcastFullState();
        return;
    }

    if (type == WS_EVT_DATA) {
        AwsFrameInfo* info = (AwsFrameInfo*)arg;
        if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
            JsonDocument doc;
            if (deserializeJson(doc, data, len) != DeserializationError::Ok) return;

            String action = doc["action"] | "";

            if (action == "GET_STATE") {
                broadcastFullState();
            } else if (action == "REMOTE_UNLOCK") {
                triggerAccessEvent("WEB", "Quản trị viên (Mở từ Web App)", true, "MO CUA TU WEB", "XIN MOI VAO!");
                broadcastFullState();
            } else if (action == "FORCE_LOCK") {
                setLockHardware(false);
                updateLcd(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
                broadcastFullState();
            } else if (action == "START_RFID_LEARN") {
                rfidLearnMode = true;
                updateLcd("CHE DO THEM THE", "MOI QUET THE...");
            } else if (action == "ADD_RFID") {
                rfidList.push_back({
                    doc["uid"].as<String>(),
                    doc["name"].as<String>(),
                    getCurrentTimeStr()
                });
                saveConfigToFlash();
                broadcastFullState();
            } else if (action == "DELETE_RFID") {
                String uid = doc["uid"].as<String>();
                rfidList.erase(std::remove_if(rfidList.begin(), rfidList.end(),
                    [&](const RfidEntry& r) { return r.uid == uid; }), rfidList.end());
                saveConfigToFlash();
                broadcastFullState();
            } else if (action == "ENROLL_FP") {
                fpEnrollActive = true;
                fpEnrollTargetId = doc["id"].as<int>();
                fpEnrollTargetName = doc["name"].as<String>();
            } else if (action == "DELETE_FP") {
                int id = doc["id"].as<int>();
                finger.deleteModel(id);
                fpList.erase(std::remove_if(fpList.begin(), fpList.end(),
                    [&](const FpEntry& f) { return f.id == id; }), fpList.end());
                saveConfigToFlash();
                broadcastFullState();
            } else if (action == "SAVE_CONFIG") {
                currentPinCode = doc["config"]["pinCode"] | currentPinCode;
                unlockDurationSec = doc["config"]["unlockDurationSec"] | unlockDurationSec;
                maxWrongAttempts = doc["config"]["maxWrongAttempts"] | maxWrongAttempts;
                saveConfigToFlash();
                updateLcd("CAP NHAT PIN OK", "LUU FLASH XONG");
                broadcastFullState();
            } else if (action == "CLEAR_LOGS") {
                accessLogs.clear();
                broadcastFullState();
            }
        }
    }
}

// ============================================================================
// 10. SETUP & VÒNG LẶP CHÍNH (MAIN LOOP)
// ============================================================================
void setup() {
    Serial.begin(115200);

    // 1. Khởi tạo chân kích Khóa chốt điện từ 12V
    pinMode(LOCK_RELAY_PIN, OUTPUT);
    setLockHardware(false);

    // 2. Khởi tạo màn hình LCD I2C
    Wire.begin(LCD_SDA_PIN, LCD_SCL_PIN);
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print(" SMART DOOR 13  ");
    lcd.setCursor(0, 1);
    lcd.print("DANG KHOI DONG..");

    // 3. Khởi tạo bộ nhớ Flash LittleFS & nạp cấu hình
    if (LittleFS.begin(true)) {
        loadConfigFromFlash();
    }

    // 4. Khởi tạo Module RFID RC522 (SPI) & Cảm biến vân tay AS608 (UART2)
    SPI.begin(RFID_SCK_PIN, RFID_MISO_PIN, RFID_MOSI_PIN, RFID_SS_PIN);
    rfid.PCD_Init();
    finger.begin(FP_BAUDRATE);

    // 5. Kết nối Wi-Fi (Nếu quá 8 giây không có Wi-Fi thì tự phát Access Point riêng)
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    unsigned long wifiStart = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - wifiStart < 8000) {
        delay(250);
    }

    if (WiFi.status() == WL_CONNECTED) {
        configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, NTP_SERVER);
        Serial.print("Da ket noi Wi-Fi! Truy cap Web App tai IP: http://");
        Serial.println(WiFi.localIP());
        updateLcd("WIFI CONNECTED!", WiFi.localIP().toString());
    } else {
        WiFi.mode(WIFI_AP);
        WiFi.softAP(AP_FALLBACK_SSID, AP_FALLBACK_PASS);
        Serial.print("Phat Wi-Fi AP rieng: ");
        Serial.println(AP_FALLBACK_SSID);
        Serial.print("Truy cap Web App tai IP: http://");
        Serial.println(WiFi.softAPIP());
        updateLcd("AP: SmartDoor13", WiFi.softAPIP().toString());
    }

    // Khởi tạo tên miền cục bộ mDNS: http://smartdoor.local
    if (MDNS.begin(MDNS_HOSTNAME)) {
        MDNS.addService("http", "tcp", 80);
        Serial.println("Da kich hoat ten mien: http://" MDNS_HOSTNAME ".local");
    }

    delay(1500);
    updateLcd(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");

    // 6. Khởi chạy WebSocket & Phục vụ giao diện Web App từ LittleFS
    ws.onEvent(onWsEvent);
    server.addHandler(&ws);
    server.serveStatic("/", LittleFS, "/").setDefaultFile("index.html");
    server.begin();
}

void loop() {
    ws.cleanupClients();

    // Tự động đóng khóa chốt 12V sau khi hết thời gian giữ mở
    if (isDoorUnlocked && (millis() - doorUnlockStartMs >= (unsigned long)unlockDurationSec * 1000UL)) {
        setLockHardware(false);
        updateLcd(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
        broadcastFullState();
    }

    // Nếu người dùng bấm "Đăng ký vân tay mới" từ Web App
    if (fpEnrollActive) {
        fpEnrollActive = false;
        processFingerprintEnrollBlocking(fpEnrollTargetId, fpEnrollTargetName);
    }

    // Quét bàn phím Keypad 4x4 liên tục (không độ trễ)
    handleKeypad4x4();

    // Quét RFID RC522 và Vân tay AS608 mỗi 80ms
    if (millis() - lastSensorPollMs >= 80) {
        lastSensorPollMs = millis();
        handleRfidRc522();
        handleFingerprintAs608();
    }
}
