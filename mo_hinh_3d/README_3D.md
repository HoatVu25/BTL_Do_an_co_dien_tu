# Thiết Kế Mô Hình 3D Hộp Điều Khiển Cửa Bảo Mật (Nhóm 13)

Thư mục này chứa toàn bộ bản vẽ CAD 3D (`.STL`, `.SCAD`) và trình xem 3D tương tác (`.HTML`) cho hộp điều khiển trung tâm của đề tài:
**"Thiết kế mô hình hệ thống cửa bảo mật tích hợp sinh trắc học vân tay, thẻ từ RFID, Keypad"** — Nhóm 13 (Nguyễn Tuấn Sơn, Vũ Hữu Hoạt).

---

## 1. Danh sách các file trong thư mục

| Tên file | Mô tả chi tiết |
| :--- | :--- |
| `HopDieuKhien_ThanDuoi_Base.stl` | File in 3D **Thân hộp dưới** (`134 × 210 × 55 mm`, vách dày `3 mm`, tích hợp 4 trụ vít M3 + 4 gờ chữ L giữ mạch PCB `100 × 100 mm`, lỗ bắt vít treo tường và cổng nguồn DC 12V + dây khóa chốt 12V). |
| `HopDieuKhien_NapTruoc_Cover.stl` | File in 3D **Nắp mặt trước** (`134 × 210 × 6 mm`) khoét sẵn lỗ bậc 2 tầng cho vân tay AS608, hốc âm mặt bích bàn phím `65 × 64 mm`, hốc âm mỏng `1.5 mm` cho RFID RC522 (`40 × 60 mm`), và lưới loa thông báo `Ø30 mm`. |
| `HopDieuKhien_LapRap_Full.stl` | File 3D lắp ráp tổng thể nguyên cụm (gồm cả vỏ hộp và các khối linh kiện bên trong). |
| `ThietKeHop_CuaBaoMat_Nhom13.scad` | File mã nguồn CAD tham số (OpenSCAD) dễ dàng tùy chỉnh kích thước. |
| `generate_stl_models.py` | Script Python tự động sinh bộ file lưới 3D `.STL` chính xác theo kích thước kỹ thuật. |
| `XemMoHinh3D_TuongTac.html` | Trình xem 3D tương tác trực tiếp trên trình duyệt (xoay 360°, tách lớp Exploded View, xuyên thấu X-Ray và bản vẽ mặt cắt kiểm tra khoảng trống 2D). |

---

## 2. Thông số kích thước linh kiện & dung sai lắp ghép (Bản v3.0)

- **Kích thước phủ bì hộp**: `134.0 × 210.0 × 61.0 mm` (Thân dưới sâu `55.0 mm` + Nắp dày `6.0 mm`, lòng trong `128.0 × 204.0 × 55.0 mm`).
- **Cảm biến vân tay quang học AS608**:
  - Kích thước mặt cảm biến: `15.3 × 18.2 mm` (Lỗ khoét xuyên mặt nắp: `15.6 × 18.5 mm`).
  - Kích thước cửa sổ nhận diện: `15.0 × 17.0 mm`.
  - Hốc bậc đỡ thân sau (Counterbore): `20.8 × 23.6 mm` kèm ống gá sâu `15.0 mm` ở mặt trong nắp.
  - Thân cảm biến dài `45.0 mm` đặt ở khoang trên (`Y = +58.0 mm`), cách đáy hộp `13.0 mm` và cách mép trên của PCB `30.2 mm` (đảm bảo không bao giờ cấn PCB).
- **Mạch đọc thẻ từ RFID RC522**:
  - Kích thước mạch: `40.0 × 60.0 mm` (Hốc âm mặt trong nắp: `40.6 × 60.6 mm`, chừa vách nhựa mặt ngoài mỏng `1.5 mm` để sóng RF `13.56 MHz` xuyên qua nhạy nhất).
- **Bàn phím cứng ma trận 3×4**:
  - Kích thước mặt bích: `65.0 × 64.0 mm` (Hốc âm mặt ngoài: `65.5 × 64.5 mm` sâu `2.0 mm`, lỗ xuyên thân: `55.0 × 56.0 mm`, 4 lỗ vít cố định cách tâm `58.0 × 57.0 mm`).
- **Mạch PCB trung tâm (ESP32 + Nguồn + Relay)**:
  - Kích thước PCB: `100.0 × 100.0 mm` đặt tại khoang dưới (`Y = -34.0 mm`), cố định bằng 4 trụ vít M3 (tâm `92.0 × 92.0 mm`, cao `5.0 mm`) kết hợp 4 gờ chữ L ôm khít 4 góc bo (`100.4 × 100.4 mm`).
