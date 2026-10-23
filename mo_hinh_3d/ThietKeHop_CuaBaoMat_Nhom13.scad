// ============================================================================
// ĐỀ TÀI: HỆ THỐNG CỬA BẢO MẬT TÍCH HỢP VÂN TAY AS608, RFID RC522, KEYPAD
// NHÓM 13: Nguyễn Tuấn Sơn - Vũ Hữu Hoạt
// FILE: Thiết kế 3D Hộp điều khiển trung tâm (Bản v3.0 - Chống va chạm & Tối ưu không gian đi dây)
// Đơn vị: mm
// ============================================================================
// KIỂM TRA KHÔNG GIAN LẮP RÁP (CLEARANCE CHECK 3 CHIỀU X - Y - Z):
// 1. Kích thước phủ bì hộp: 134 (Rộng) x 210 (Cao) x 61 (Sâu: Đáy 55 + Nắp 6) mm
//    -> Lòng trong hộp: 128 x 204 x 55 mm
// 2. Chiều sâu Z (Lòng trong 55mm + Nắp 6mm = 58mm tính từ mặt trong đáy lên mặt ngoài nắp):
//    - Cảm biến AS608 dài 45mm: Đuôi dừng ở Z = 16mm (cách đáy hộp 13mm để cắm giắc 6 chân)
//    - Mạch PCB 100x100mm đặt ở Z = 8mm: Còn 35mm phía trên cho ESP32, Relay, Domino & dây cắm
// 3. Chiều dọc Y (Tách biệt hoàn toàn vùng AS608 và vùng PCB 100x100mm):
//    - PCB 100x100mm đặt ở nửa dưới (tâm Y = -34mm -> chiếm Y từ -84 đến +16mm)
//    - Cảm biến AS608 đặt ở nửa trên (tâm Y = +58mm -> thân chiếm Y từ +46.2 đến +69.8mm)
//    -> Khoảng cách an toàn giữa đuôi AS608 và mép trên PCB là 30.2mm (KHÔNG BAO GIỜ ĐỤNG NHAU!)
// ============================================================================

$fn = 48;

mode = "explode"; // "assembled", "explode", "print"
explode_dist = 38;

// --- 1. KÍCH THƯỚC TỔNG THỂ HỘP (ĐÃ MỞ RỘNG ĐỂ DƯ CHỖ ĐI DÂY) ---
box_w    = 134.0;     // Rộng phủ bì 134mm (Lòng trong 128mm -> dư 14mm mỗi bên PCB 100mm)
box_h    = 210.0;     // Cao phủ bì 210mm (Lòng trong 204mm -> tách riêng khoang AS608 & PCB)
base_d   = 55.0;      // Chiều sâu thân dưới 55mm (Đủ sâu cho AS608 dài 45mm + ESP32 + Relay)
lid_d    = 6.0;       // Chiều dày nắp mặt trước 6mm
wall     = 3.0;       // Độ dày thành vách 3mm
corner_r = 7.5;       // Bán kính bo góc hộp

// --- 2. MẠCH PCB TRUNG TÂM (100 x 100 mm) ---
pcb_w       = 100.0;
pcb_h       = 100.0;
pcb_y_off   = -34.0;  // Tâm Y = -34mm -> PCB nằm từ Y = -84mm đến Y = +16mm
pcb_hole_dx = 92.0;   // Khoảng cách tâm 4 lỗ vít M3 trên PCB (cách mép 4mm)
pcb_hole_dy = 92.0;
standoff_h  = 5.0;    // Chiều cao trụ đỡ PCB dưới đáy (5mm)

// --- 3. CẢM BIẾN VÂN TAY AS608 (Góc trên bên trái) ---
as608_x        = -30.0;
as608_y        = 58.0;  // Cách mép trên PCB hơn 30mm -> thả thẳng thân sâu 45mm xuống thoải mái
as608_win_w    = 15.0;  // Cửa sổ nhận diện 15 x 17 mm
as608_win_h    = 17.0;
as608_face_w   = 15.3;  // Mặt cảm biến 15.3 x 18.2 mm
as608_face_h   = 18.2;
as608_cut_w    = 15.6;  // Lỗ khoét xuyên nắp (15.3 + 0.3mm dung sai)
as608_cut_h    = 18.5;  // Lỗ khoét xuyên nắp (18.2 + 0.3mm dung sai)
as608_body_w   = 20.8;  // Hốc bậc giữ thân cảm biến ở mặt trong nắp
as608_body_h   = 23.6;

// --- 4. MODULE ĐỌC THẺ TỪ RFID RC522 (40 x 60 mm - Góc trên bên phải) ---
rc522_x     = 26.0;
rc522_y     = 58.0;
rc522_w     = 40.0;
rc522_h     = 60.0;
rc522_cut_w = 40.6;    // Hốc âm mặt trong (40 + 0.6mm dung sai)
rc522_cut_h = 60.6;    // Hốc âm mặt trong (60 + 0.6mm dung sai)
rc522_rf_t  = 1.5;     // Độ dày vách nhựa mỏng phía trước cho sóng RF xuyên qua

// --- 5. BÀN PHÍM CỨNG MA TRẬN (65 x 64 mm - Khu vực dưới bên trái) ---
kp_x        = -20.0;
kp_y        = -42.0;
kp_flange_w = 65.5;    // Hốc âm mặt bích bàn phím (65.0 + 0.5mm dung sai)
kp_flange_h = 64.5;    // Hốc âm mặt bích bàn phím (64.0 + 0.5mm dung sai)
kp_cut_w    = 55.0;    // Lỗ khoét xuyên lòng bàn phím & chân cáp
kp_cut_h    = 56.0;
kp_hole_dx  = 58.0;    // Khoảng cách tâm lỗ vít bàn phím ngang
kp_hole_dy  = 57.0;    // Khoảng cách tâm lỗ vít bàn phím dọc

// --- 6. LOA THÔNG BÁO & ĐÈN LED BÁO TRẠNG THÁI (Khu vực dưới bên phải) ---
spk_x = 39.0;
spk_y = -44.0;
spk_r = 15.0;          // Loa đường kính 30mm

// ============================================================================
// MODULE TIỆN ÍCH
// ============================================================================
module rounded_box(w, h, d, r) {
    hull() {
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([ix*(w/2 - r), iy*(h/2 - r), 0])
                cylinder(r=r, h=d);
        }
    }
}

module standoff(h_post, r_outer=4.2, r_inner=1.5) {
    difference() {
        cylinder(r=r_outer, h=h_post);
        translate([0, 0, -0.1])
            cylinder(r=r_inner, h=h_post + 0.2);
    }
}

// ============================================================================
// CHI TIẾT 1: THÂN HỘP DƯỚI (BASE ENCLOSURE - 134 x 210 x 55 mm)
// ============================================================================
module base_enclosure() {
    difference() {
        rounded_box(box_w, box_h, base_d, corner_r);

        // Khoét rỗng lòng hộp (128 x 204 x 52 mm)
        translate([0, 0, wall])
            rounded_box(box_w - 2*wall, box_h - 2*wall, base_d, corner_r - wall);

        // Bậc ngàm lắp ghép nắp trước
        translate([0, 0, base_d - 2.5])
            rounded_box(box_w - wall, box_h - wall, 3.0, corner_r - wall/2);

        // 4 lỗ bắt vít treo tường / gắn cửa ở mặt đáy (M4)
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([ix*46, iy*88, -0.5]) {
                cylinder(r=2.2, h=wall + 1);
                translate([0, 0, 1.5]) cylinder(r1=2.2, r2=4.2, h=2.0);
            }
        }

        // Lỗ luồn dây âm mặt lưng (Ø18mm ở khoang trên - dễ dàng luồn dây nguồn & khóa)
        translate([0, 32, -0.5])
            cylinder(r=9.0, h=wall + 1);

        // Cổng nguồn DC 12V (Ø8.4mm) và dây Khóa chốt điện từ 12V (Ø6.4mm) ở cạnh dưới
        translate([-22, -box_h/2 + wall/2, 18])
            rotate([90, 0, 0]) cylinder(r=4.2, h=wall*3, center=true);
        translate([22, -box_h/2 + wall/2, 18])
            rotate([90, 0, 0]) cylinder(r=3.2, h=wall*3, center=true);
    }

    // 4 Trụ bắt vít nắp hộp ở 4 góc (M3)
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(box_w/2 - 7.0), iy*(box_h/2 - 7.0), wall])
            standoff(base_d - wall - 2.5, r_outer=4.8, r_inner=1.6);
    }

    // 4 Trụ đỡ mạch PCB trung tâm 100x100mm (Tâm lỗ 92x92mm, cao 5mm)
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(pcb_hole_dx/2), pcb_y_off + iy*(pcb_hole_dy/2), wall])
            standoff(standoff_h, r_outer=4.2, r_inner=1.5);
    }

    // 4 Gờ chữ L định vị 4 góc bo PCB 100x100mm
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(pcb_w/2 + 1.2), pcb_y_off + iy*(pcb_h/2 + 1.2), wall + standoff_h/2 + 1.0])
            cube([2.2, 2.2, standoff_h + 2.0], center=true);
    }
}

// ============================================================================
// CHI TIẾT 2: NẮP MẶT TRƯỚC (FRONT COVER PANEL - 134 x 210 x 6 mm)
// ============================================================================
module front_cover() {
    difference() {
        union() {
            rounded_box(box_w, box_h, lid_d, corner_r);
            translate([0, 0, -2.0])
                rounded_box(box_w - wall - 0.4, box_h - wall - 0.4, 2.0, corner_r - wall/2);
        }

        translate([0, 0, -2.5])
            rounded_box(box_w - 2*wall - 1.0, box_h - 2*wall - 1.0, lid_d, corner_r - wall);

        // 1. CẢM BIẾN VÂN TAY AS608:
        // - Lỗ xuyên mặt cảm biến 15.6 x 18.5 mm (mặt thực 15.3 x 18.2, cửa sổ 15 x 17)
        translate([as608_x, as608_y, 0])
            cube([as608_cut_w, as608_cut_h, 25.0], center=true);
        // - Hốc bậc mặt trong cho phần thân cảm biến (20.8 x 23.6 mm)
        translate([as608_x, as608_y, -2.0])
            cube([as608_body_w, as608_body_h, (lid_d - 2.0)*2], center=true);

        // 2. MẠCH ĐỌC RFID RC522 (40 x 60 mm):
        translate([rc522_x, rc522_y, -1.5])
            cube([rc522_cut_w, rc522_cut_h, (lid_d - rc522_rf_t)*2], center=true);

        // 3. BÀN PHÍM CỨNG MA TRẬN (65 x 64 mm):
        translate([kp_x, kp_y, lid_d - 1.0])
            cube([kp_flange_w, kp_flange_h, 2.2], center=true);
        translate([kp_x, kp_y, 0])
            cube([kp_cut_w, kp_cut_h, 25.0], center=true);
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([kp_x + ix*(kp_hole_dx/2), kp_y + iy*(kp_hole_dy/2), -5])
                cylinder(r=1.5, h=20);
        }

        // 4. LƯỚI LOA THÔNG BÁO & 3 LỖ ĐÈN LED:
        translate([spk_x, spk_y, -5]) {
            cylinder(r=1.8, h=20);
            for (a = [0:60:300])
                rotate([0, 0, a]) translate([6.0, 0, 0]) cylinder(r=1.6, h=20);
            for (a = [0:30:330])
                rotate([0, 0, a]) translate([11.5, 0, 0]) cylinder(r=1.5, h=20);
        }
        for (i = [-1, 0, 1]) {
            translate([spk_x + i*9.0, -8.0, -5])
                cylinder(r=1.6, h=20);
        }

        // 5. 4 LỖ VÍT M3 Ở 4 GÓC NẮP HỘP:
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([ix*(box_w/2 - 7.0), iy*(box_h/2 - 7.0), -5])
                cylinder(r=1.7, h=20);
        }
    }

    // Ống gá giữ thân cảm biến vân tay AS608 ở mặt trong nắp (sâu 15mm)
    translate([as608_x, as608_y, -7.5])
        difference() {
            cube([as608_body_w + 5.0, as608_body_h + 5.0, 15.0], center=true);
            cube([as608_body_w, as608_body_h, 17.0], center=true);
        }

    // Gờ giữ 4 cạnh mạch RFID RC522 (40 x 60 mm) ở mặt trong nắp
    translate([rc522_x, rc522_y, -2.0])
        difference() {
            cube([rc522_cut_w + 4.0, rc522_cut_h + 4.0, 4.0], center=true);
            cube([rc522_cut_w, rc522_cut_h, 6.0], center=true);
        }

    // Vành định vị Loa Ø30mm ở mặt trong nắp
    translate([spk_x, spk_y, -4.0])
        difference() {
            cylinder(r=spk_r + 2.2, h=4.0);
            translate([0, 0, -0.5]) cylinder(r=spk_r + 0.3, h=5.0);
        }
}

module components_preview() {
    // 1. Mạch PCB trung tâm 100 x 100 mm + ESP32 + Relay (Tại Y = -34mm, Z = 8mm)
    color([0.1, 0.5, 0.22])
    translate([0, pcb_y_off, wall + standoff_h + 0.8])
        cube([pcb_w, pcb_h, 1.6], center=true);

    color([0.15, 0.18, 0.22])
    translate([0, pcb_y_off, wall + standoff_h + 8.5])
        cube([28, 52, 14], center=true);

    // 2. Cảm biến vân tay AS608 (Tại Y = +58mm, thân sâu 45mm hoàn toàn không chạm PCB!)
    color([0.12, 0.12, 0.12])
    translate([as608_x, as608_y, base_d - 20.5])
        cube([20.4, 23.3, 41], center=true);
    color([0.2, 0.2, 0.2])
    translate([as608_x, as608_y, base_d + 3])
        cube([as608_face_w, as608_face_h, 6], center=true);
    color([0.2, 0.75, 0.95])
    translate([as608_x, as608_y, base_d + 6.2])
        cube([as608_win_w, as608_win_h, 0.5], center=true);

    // 3. Mạch RFID RC522 (40 x 60 mm)
    color([0.05, 0.35, 0.68])
    translate([rc522_x, rc522_y, base_d + 2.0])
        cube([rc522_w, rc522_h, 1.6], center=true);

    // 4. Bàn phím ma trận (65 x 64 mm)
    color([0.18, 0.18, 0.22])
    translate([kp_x, kp_y, base_d + lid_d - 2.0])
        cube([65.0, 64.0, 8.0], center=true);

    // 5. Loa thông báo Ø30mm
    color([0.75, 0.55, 0.1])
    translate([spk_x, spk_y, base_d - 6])
        cylinder(r=15, h=8);
}

if (mode == "assembled") {
    color([0.22, 0.25, 0.30]) base_enclosure();
    components_preview();
    color([0.92, 0.94, 0.96]) translate([0, 0, base_d]) front_cover();
} else if (mode == "explode") {
    color([0.22, 0.25, 0.30]) base_enclosure();
    translate([0, 0, explode_dist * 0.6]) components_preview();
    color([0.92, 0.94, 0.96]) translate([0, 0, base_d + explode_dist * 1.5]) front_cover();
} else if (mode == "print") {
    translate([-box_w/2 - 10, 0, 0]) base_enclosure();
    translate([box_w/2 + 10, 0, lid_d]) rotate([0, 180, 0]) front_cover();
}
