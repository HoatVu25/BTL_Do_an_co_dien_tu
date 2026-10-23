# Thiết Kế Mô Hình 3D Hộp Điều Khiển Cửa Bảo Mật (Nhóm 13) - Bản v4.0

Thư mục này chứa toàn bộ bản vẽ CAD 3D (`.STL`, `.SCAD`) cho hộp điều khiển trung tâm của đề tài:
**"Thiết kế mô hình hệ thống cửa bảo mật tích hợp sinh trắc học vân tay, thẻ từ RFID, Keypad, Màn hình LCD 16x2"** — Nhóm 13 (Nguyễn Tuấn Sơn, Vũ Hữu Hoạt).

---

## 1. Danh sách các file trong thư mục

| Tên file | Mô tả chi tiết |
| :--- | :--- |
| `HopDieuKhien_ThanDuoi_Base.stl` | File in 3D **Thân hộp dưới** (`130 × 210 × 48 mm`, vách dày `2.8 mm`, tích hợp 4 trụ vít M3 + 4 gờ chữ L giữ mạch PCB `100 × 100 mm`, lỗ bắt vít treo tường và cổng nguồn DC 12V + dây khóa chốt 12V). |
| `HopDieuKhien_NapTruoc_Cover.stl` | File in 3D **Nắp mặt trước** (`130 × 210 × 3.5 mm` - mỏng nhẹ, tối ưu chi phí in 3D) khoét sẵn: Cửa sổ hiển thị **LCD 16x2** (`72 × 27 mm`) kèm **4 trụ vít M3** tâm `75 × 31 mm`, lỗ đục hở vân tay AS608 (`15.6 × 18.5 mm`), hốc định vị RFID RC522 (`40 × 60 mm`), và hốc bàn phím ma trận (`65 × 64 mm`) đặt chính giữa cân đối. |
| `HopDieuKhien_LapRap_Full.stl` | File 3D lắp ráp tổng thể nguyên cụm (gồm cả vỏ hộp và các khối linh kiện bên trong). |
| `ThietKeHop_CuaBaoMat_Nhom13.scad` | File mã nguồn CAD tham số (OpenSCAD v4.0) dễ dàng tùy chỉnh kích thước. |

---

## 2. Thông số kích thước linh kiện & bố cục mặt trước (Bản v4.0)

- **Kích thước phủ bì hộp**: `130.0 × 210.0 × 51.5 mm` (Thân dưới sâu `48.0 mm` + Nắp dày `3.5 mm`, lòng trong `124.0 × 204.0 × 48.0 mm`).
- **Nắp mặt trước mỏng nhẹ (3.5 mm):** Tiết kiệm tối đa sợi nhựa in 3D và rút ngắn thời gian in.
- **Bố cục các tầng linh kiện trên mặt trước:**
  - **Hàng 1 (Trên cùng - Xác thực):**
    - Bên trái: Cảm biến vân tay quang học AS608 tại `(-32, +68)` mm (Lỗ đục hở `15.6 × 18.5 mm`).
    - Bên phải: Module đọc thẻ từ RFID-RC522 tại `(+28, +68)` mm (Hốc âm định vị `40.6 × 60.6 mm`).
  - **Hàng 2 (Ở giữa - Hiển thị trạng thái):**
    - Chính giữa: **Màn hình LCD 16x2 I2C** tại `(0, +18)` mm.
    - Cửa sổ đục hở khung hiển thị kim loại: `72.0 × 27.0 mm`.
    - **4 điểm bắt vít M3:** Khoảng cách tâm `75.0 × 31.0 mm` với 4 trụ vít M3 ở mặt sau nắp, bắt ốc cố định bo mạch LCD 1602 cực kỳ chắc chắn.
  - **Hàng 3 (Dưới cùng - Nhập mã PIN):**
    - Chính giữa: Bàn phím cứng ma trận tại `(0, -46)` mm (Mặt bích `65.0 × 64.0 mm`, lỗ đục xuyên thân `55.0 × 56.0 mm`, 4 lỗ vít cố định tâm `58.0 × 57.0 mm`).
- **Mạch PCB trung tâm (ESP32 + Nguồn + Relay):**
  - Kích thước PCB: `100.0 × 100.0 mm` đặt tại khoang dưới đáy (`Y = -40.0 mm`), cố định bằng 4 trụ vít M3 (tâm `92.0 × 92.0 mm`, cao `5.0 mm`) kết hợp 4 gờ chữ L ôm khít 4 góc bo.
