// ============================================================================
// ĐỀ TÀI: HỆ THỐNG CỬA BẢO MẬT TÍCH HỢP VÂN TAY AS608, RFID RC522, KEYPAD, LCD 16x2
// NHÓM 13: Nguyễn Tuấn Sơn - Vũ Hữu Hoạt
// BẢN v4.0 - THAY LOA BẰNG MÀN HÌNH LCD 16x2 I2C, ĐỤC MẶT THỦNG TIẾT KIỆM NHỰA
// Đơn vị: mm
// ============================================================================
// CẢI TIẾN QUAN TRỌNG:
// 1. BỎ HOÀN TOÀN LOA THÔNG BÁO theo yêu cầu nhóm.
// 2. THÊM MÀN HÌNH LCD 16x2 I2C:
//    - Đục lỗ xuyên nắp (72.0 x 27.0 mm) để lộ khung viền hiển thị LCD 1602 ra mặt trước.
//    - 4 trụ vít M3 ở mặt sau nắp (khoảng cách tâm 75.0 x 31.0 mm) để bắt chặt bo LCD.
// 3. TIẾT KIỆM NHỰA & CHI PHÍ IN 3D:
//    - Nắp làm mỏng tối ưu (3.0 mm), các hốc đều đục hở giúp in cực nhanh, không tốn nhựa.
//    - Bàn phím ma trận (65 x 64 mm) đặt chính giữa nửa dưới, cân đối thẩm mỹ tuyệt đối.
// ============================================================================

$fn = 48;

mode = "explode"; // "assembled", "explode", "print"
explode_dist = 38;

// --- 1. KÍCH THƯỚC TỔNG THỂ HỘP ---
box_w    = 130.0;     // Rộng phủ bì 130 mm (Lòng trong 124 mm -> vừa bo PCB 100x100 và LCD 80mm)
box_h    = 210.0;     // Cao phủ bì 210 mm
base_d   = 48.0;      // Chiều sâu thân dưới 48 mm (thoải mái cắm giắc)
lid_d    = 3.5;       // Chiều dày nắp mặt trước chỉ 3.5 mm (siêu tiết kiệm nhựa in)
wall     = 2.8;       // Độ dày thành vách 2.8 mm
corner_r = 7.0;       // Bo góc

// --- 2. MẠCH PCB TRUNG TÂM (100 x 100 mm) DƯỚI ĐÁY ---
pcb_w       = 100.0;
pcb_h       = 100.0;
pcb_y_off   = -40.0;  // Nằm ở nửa dưới hộp
pcb_hole_dx = 92.0;   // Tâm 4 lỗ vít M3 (cách mép 4mm)
pcb_hole_dy = 92.0;
standoff_h  = 5.0;    // Cao trụ đỡ đáy 5mm

// --- 3. HÀNG TRÊN: VÂN TAY AS608 VÀ RFID RC522 ---
// 3.1. Cảm biến vân tay AS608 (Góc trên bên trái)
as608_x      = -32.0;
as608_y      = 68.0;
as608_cut_w  = 15.6;  // Đục hở mặt cảm biến (15.3 x 18.2 mm)
as608_cut_h  = 18.5;
as608_body_w = 20.8;
as608_body_h = 23.6;

// 3.2. Module RFID RC522 (Góc trên bên phải)
rc522_x      = 28.0;
rc522_y      = 68.0;
rc522_cut_w  = 40.6;  // Kích thước module 40 x 60 mm
rc522_cut_h  = 60.6;

// --- 4. HÀNG GIỮA: MÀN HÌNH LCD 16x2 I2C (CHÍNH GIỮA) ---
lcd_x        = 0.0;   // Đặt chính giữa
lcd_y        = 18.0;  // Giữa khoang thẻ/vân tay và bàn phím
lcd_cut_w    = 72.0;  // Lỗ đục hở khung hiển thị kim loại (71.3 x 26.3 mm + dung sai)
lcd_cut_h    = 27.0;
lcd_pcb_w    = 80.0;  // Kích thước PCB ngoài cùng của LCD 1602
lcd_pcb_h    = 36.0;
lcd_hole_dx  = 75.0;  // Khoảng cách tâm lỗ vít M3 ngang
lcd_hole_dy  = 31.0;  // Khoảng cách tâm lỗ vít M3 dọc

// --- 5. HÀNG DƯỚI: BÀN PHÍM CỨNG MA TRẬN 65 x 64 mm (CHÍNH GIỮA) ---
kp_x        = 0.0;    // Đặt chính giữa cân đối
kp_y        = -46.0;
kp_flange_w = 65.5;   // Mặt bích 65.0 x 64.0 mm
kp_flange_h = 64.5;
kp_cut_w    = 55.0;   // Đục hở xuyên thân bàn phím
kp_cut_h    = 56.0;
kp_hole_dx  = 58.0;   // Tâm vít 58.0 x 57.0 mm
kp_hole_dy  = 57.0;

// ============================================================================
// TIỆN ÍCH HÌNH HỌC
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
// CHI TIẾT 1: THÂN HỘP DƯỚI (BASE ENCLOSURE)
// ============================================================================
module base_enclosure() {
    difference() {
        rounded_box(box_w, box_h, base_d, corner_r);

        // Khoét rỗng lòng hộp
        translate([0, 0, wall])
            rounded_box(box_w - 2*wall, box_h - 2*wall, base_d, corner_r - wall);

        // Bậc gờ ngàm nắp
        translate([0, 0, base_d - 2.0])
            rounded_box(box_w - wall, box_h - wall, 2.5, corner_r - wall/2);

        // 4 lỗ bắt vít treo tường M4 ở đáy
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([ix*45, iy*88, -0.5]) {
                cylinder(r=2.2, h=wall + 1);
                translate([0, 0, 1.5]) cylinder(r1=2.2, r2=4.2, h=1.8);
            }
        }

        // Lỗ luồn dây âm mặt lưng (Ø18mm)
        translate([0, 68, -0.5])
            cylinder(r=9.0, h=wall + 1);

        // Cổng nguồn DC 12V và dây Khóa chốt 12V ở cạnh dưới
        translate([-22, -box_h/2 + wall/2, 16])
            rotate([90, 0, 0]) cylinder(r=4.2, h=wall*3, center=true);
        translate([22, -box_h/2 + wall/2, 16])
            rotate([90, 0, 0]) cylinder(r=3.2, h=wall*3, center=true);

        // Lỗ luồn dây hông bên phải (Ø8mm) chạy thẳng sang Khóa chốt 12V trên khung cửa
        translate([box_w/2 - wall/2, -40, 16])
            rotate([0, 90, 0]) cylinder(r=4.0, h=wall*3, center=true);
    }

    // 4 Trụ bắt vít nắp hộp M3 ở 4 góc
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(box_w/2 - 6.5), iy*(box_h/2 - 6.5), wall])
            standoff(base_d - wall - 2.0, r_outer=4.6, r_inner=1.6);
    }

    // 4 Trụ đỡ mạch PCB trung tâm 100x100mm (Tâm 92x92mm, cao 5mm)
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(pcb_hole_dx/2), pcb_y_off + iy*(pcb_hole_dy/2), wall])
            standoff(standoff_h, r_outer=4.0, r_inner=1.5);
    }

    // 4 Gờ chữ L định vị 4 góc bo PCB 100x100mm
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([ix*(pcb_w/2 + 1.2), pcb_y_off + iy*(pcb_h/2 + 1.2), wall + standoff_h/2 + 1.0])
            cube([2.0, 2.0, standoff_h + 2.0], center=true);
    }
}

// ============================================================================
// CHI TIẾT 2: NẮP MẶT TRƯỚC (FRONT COVER PANEL - MỎNG & ĐỤC HỞ CÁC MẶT)
// ============================================================================
module front_cover() {
    difference() {
        union() {
            rounded_box(box_w, box_h, lid_d, corner_r);
            // Gờ định vị âm lọt vào thân dưới
            translate([0, 0, -1.8])
                rounded_box(box_w - wall - 0.4, box_h - wall - 0.4, 1.8, corner_r - wall/2);
        }

        // 1. ĐỤC HỞ CỬA SỔ HIỂN THỊ MÀN HÌNH LCD 16x2 (72 x 27 mm)
        translate([lcd_x, lcd_y, -5])
            cube([lcd_cut_w, lcd_cut_h, 20.0], center=true);

        // 4 lỗ vít M3 bắt màn hình LCD 16x2 (khoảng cách tâm 75.0 x 31.0 mm)
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([lcd_x + ix*(lcd_hole_dx/2), lcd_y + iy*(lcd_hole_dy/2), -5])
                cylinder(r=1.6, h=20);
        }

        // 2. ĐỤC HỞ CẢM BIẾN VÂN TAY AS608 (15.6 x 18.5 mm)
        translate([as608_x, as608_y, -5])
            cube([as608_cut_w, as608_cut_h, 20.0], center=true);

        // 3. ĐỤC HỞ THÂN BÀN PHÍM CỨNG MA TRẬN 65 x 64 mm
        // Hốc âm mặt bích ở mặt ngoài sâu 1.5mm
        translate([kp_x, kp_y, lid_d - 0.8])
            cube([kp_flange_w, kp_flange_h, 1.8], center=true);
        // Lỗ đục xuyên thân & cáp
        translate([kp_x, kp_y, -5])
            cube([kp_cut_w, kp_cut_h, 20.0], center=true);
        // 4 lỗ vít cố định bàn phím (58.0 x 57.0 mm)
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([kp_x + ix*(kp_hole_dx/2), kp_y + iy*(kp_hole_dy/2), -5])
                cylinder(r=1.5, h=20);
        }

        // 4. HỐC ĐỠ MODULE RFID RC522 (40 x 60 mm) Ở MẶT TRONG NẮP
        translate([rc522_x, rc522_y, -0.6])
            cube([rc522_cut_w, rc522_cut_h, 3.0], center=true);

        // 5. 4 LỖ VÍT M3 Ở 4 GÓC NẮP HỘP
        for (ix = [-1, 1], iy = [-1, 1]) {
            translate([ix*(box_w/2 - 6.5), iy*(box_h/2 - 6.5), -5])
                cylinder(r=1.7, h=20);
        }
    }

    // 4 Trụ bắt vít M3 cho LCD 16x2 ở mặt trong nắp (cao 4mm)
    for (ix = [-1, 1], iy = [-1, 1]) {
        translate([lcd_x + ix*(lcd_hole_dx/2), lcd_y + iy*(lcd_hole_dy/2), -4.0])
            difference() {
                cylinder(r=3.8, h=4.0);
                translate([0, 0, -0.2]) cylinder(r=1.5, h=4.5);
            }
    }

    // Ống gá ôm thân cảm biến AS608 ở mặt trong nắp
    translate([as608_x, as608_y, -8.0])
        difference() {
            cube([as608_body_w + 4.0, as608_body_h + 4.0, 8.0], center=true);
            cube([as608_body_w, as608_body_h, 9.0], center=true);
        }

    // Khung định vị module RFID RC522 ở mặt trong nắp
    translate([rc522_x, rc522_y, -1.5])
        difference() {
            cube([rc522_cut_w + 3.0, rc522_cut_h + 3.0, 3.0], center=true);
            cube([rc522_cut_w, rc522_cut_h, 4.0], center=true);
        }
}

// ============================================================================
// LINH KIỆN MÔ PHỎNG LẮP RÁP
// ============================================================================
module components_preview() {
    // 1. Mạch PCB trung tâm 100x100mm ở đáy
    color([0.1, 0.5, 0.22])
    translate([0, pcb_y_off, wall + standoff_h + 0.8])
        cube([pcb_w, pcb_h, 1.6], center=true);
    color([0.15, 0.18, 0.22])
    translate([0, pcb_y_off, wall + standoff_h + 8.0])
        cube([28, 52, 12], center=true);

    // 2. Màn hình LCD 16x2 I2C
    color([0.1, 0.35, 0.15])
    translate([lcd_x, lcd_y, base_d - 4])
        cube([lcd_pcb_w, lcd_pcb_h, 1.6], center=true);
    // Khung kim loại & kính LCD
    color([0.7, 0.7, 0.75])
    translate([lcd_x, lcd_y, base_d + 1])
        cube([71.3, 26.3, 7.0], center=true);
    color([0.1, 0.6, 0.8])
    translate([lcd_x, lcd_y, base_d + 4.8])
        cube([64.5, 14.5, 0.5], center=true);

    // 3. Cảm biến vân tay AS608
    color([0.12, 0.12, 0.12])
    translate([as608_x, as608_y, base_d - 20])
        cube([20.4, 23.3, 41], center=true);
    color([0.2, 0.75, 0.95])
    translate([as608_x, as608_y, base_d + 4.0])
        cube([as608_cut_w, as608_cut_h, 0.5], center=true);

    // 4. RFID RC522
    color([0.05, 0.35, 0.68])
    translate([rc522_x, rc522_y, base_d + 1.0])
        cube([rc522_cut_w, rc522_cut_h, 1.6], center=true);

    // 5. Bàn phím ma trận 65x64mm
    color([0.18, 0.18, 0.22])
    translate([kp_x, kp_y, base_d + lid_d - 1.5])
        cube([65.0, 64.0, 7.0], center=true);
}

if (mode == "assembled") {
    color([0.22, 0.25, 0.30]) base_enclosure();
    components_preview();
    color([0.92, 0.94, 0.96]) translate([0, 0, base_d]) front_cover();
} else if (mode == "explode") {
    color([0.22, 0.25, 0.30]) base_enclosure();
    translate([0, 0, explode_dist * 0.6]) components_preview();
    color([0.92, 0.94, 0.96]) translate([0, 0, base_d + explode_dist * 1.4]) front_cover();
} else if (mode == "print") {
    translate([-box_w/2 - 10, 0, 0]) base_enclosure();
    translate([box_w/2 + 10, 0, lid_d]) rotate([0, 180, 0]) front_cover();
}
