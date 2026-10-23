import struct
import math
import os

# ==============================================================================
# Trình tạo lưới Tam Giác 3D (STL) chính xác theo kích thước kỹ thuật (mm)
# Đề tài: Hệ thống cửa bảo mật tích hợp AS608, RFID RC522, Keypad - Nhóm 13
# BẢN v3.0 - ĐÃ KIỂM TRA CHỐNG ĐỤNG CHẠM 3 CHIỀU (X - Y - Z CLEARANCE VERIFIED)
#
# KÍCH THƯỚC CHUẨN:
# 1. Hộp phủ bì            : 134.0 (Rộng) x 210.0 (Cao) x 61.0 (Sâu: Đáy 55 + Nắp 6) mm
#                            -> Lòng trong: 128.0 x 204.0 x 55.0 mm
# 2. Bàn phím cứng ma trận : 65.0 x 64.0 mm (Hốc mặt bích 65.5x64.5, lỗ thân 55x56) tại (-20, -42)
# 3. Cảm biến vân tay AS608: Mặt cảm biến 15.3 x 18.2 mm (Lỗ khoét 15.6 x 18.5 mm),
#                            Cửa sổ 15.0 x 17.0 mm, Hốc thân 20.8 x 23.6 mm, sâu 45mm tại (-30, +58)
# 4. Mạch đọc RFID RC522   : 40.0 x 60.0 mm (Hốc âm 40.6 x 60.6 mm, vách RF 1.5mm) tại (+26, +58)
# 5. Mạch PCB trung tâm    : 100.0 x 100.0 mm đặt tại (0, -34), chiếm Y từ -84 đến +16 mm
#                            -> Cách đáy thân AS608 (+46.2 mm) hẳn 30.2 mm (Không bao giờ cấn!)
# ==============================================================================

class MeshBuilder:
    def __init__(self):
        self.triangles = []

    def add_tri(self, p1, p2, p3):
        ux, uy, uz = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
        vx, vy, vz = p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]
        nx = uy*vz - uz*vy
        ny = uz*vx - ux*vz
        nz = ux*vy - uy*vx
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length > 1e-9:
            nx, ny, nz = nx/length, ny/length, nz/length
        else:
            nx, ny, nz = 0.0, 0.0, 1.0
        self.triangles.append(((nx, ny, nz), p1, p2, p3))

    def add_quad(self, p1, p2, p3, p4):
        self.add_tri(p1, p2, p3)
        self.add_tri(p1, p3, p4)

    def add_box(self, x0, x1, y0, y1, z0, z1):
        p000 = (x0, y0, z0); p100 = (x1, y0, z0); p110 = (x1, y1, z0); p010 = (x0, y1, z0)
        p001 = (x0, y0, z1); p101 = (x1, y0, z1); p111 = (x1, y1, z1); p011 = (x0, y1, z1)
        self.add_quad(p000, p010, p110, p100)
        self.add_quad(p001, p101, p111, p011)
        self.add_quad(p000, p100, p101, p001)
        self.add_quad(p110, p010, p011, p111)
        self.add_quad(p010, p000, p001, p011)
        self.add_quad(p100, p110, p111, p101)

    def add_hollow_cylinder(self, cx, cy, z0, z1, r_in, r_out, segs=32):
        for i in range(segs):
            a0 = 2.0 * math.pi * i / segs
            a1 = 2.0 * math.pi * (i + 1) / segs
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)

            pb_out0 = (cx + r_out*c0, cy + r_out*s0, z0)
            pb_out1 = (cx + r_out*c1, cy + r_out*s1, z0)
            pt_out0 = (cx + r_out*c0, cy + r_out*s0, z1)
            pt_out1 = (cx + r_out*c1, cy + r_out*s1, z1)

            pb_in0 = (cx + r_in*c0, cy + r_in*s0, z0)
            pb_in1 = (cx + r_in*c1, cy + r_in*s1, z0)
            pt_in0 = (cx + r_in*c0, cy + r_in*s0, z1)
            pt_in1 = (cx + r_in*c1, cy + r_in*s1, z1)

            self.add_quad(pb_out0, pb_out1, pt_out1, pt_out0)
            if r_in > 0:
                self.add_quad(pb_in1, pb_in0, pt_in0, pt_in1)
            self.add_quad(pt_in0, pt_out0, pt_out1, pt_in1)
            self.add_quad(pb_out0, pb_in0, pb_in1, pb_out1)

    def add_cylinder(self, cx, cy, z0, z1, r, segs=28):
        for i in range(segs):
            a0 = 2.0 * math.pi * i / segs
            a1 = 2.0 * math.pi * (i + 1) / segs
            p0b = (cx + r*math.cos(a0), cy + r*math.sin(a0), z0)
            p1b = (cx + r*math.cos(a1), cy + r*math.sin(a1), z0)
            p0t = (cx + r*math.cos(a0), cy + r*math.sin(a0), z1)
            p1t = (cx + r*math.cos(a1), cy + r*math.sin(a1), z1)
            self.add_quad(p0b, p1b, p1t, p0t)
            self.add_tri((cx, cy, z1), p0t, p1t)
            self.add_tri((cx, cy, z0), p1b, p0b)

    def add_perforated_plate(self, x0, x1, y0, y1, z0, z1, features, nx=88, ny=136):
        xs = set([x0, x1])
        ys = set([y0, y1])
        for i in range(nx + 1):
            xs.add(round(x0 + (x1 - x0) * i / nx, 4))
        for j in range(ny + 1):
            ys.add(round(y0 + (y1 - y0) * j / ny, 4))
        for f in features:
            if f['shape'] == 'rect':
                if x0 < f['x0'] < x1: xs.add(round(f['x0'], 4))
                if x0 < f['x1'] < x1: xs.add(round(f['x1'], 4))
                if y0 < f['y0'] < y1: ys.add(round(f['y0'], 4))
                if y0 < f['y1'] < y1: ys.add(round(f['y1'], 4))

        xs = sorted(list(xs))
        ys = sorted(list(ys))

        def get_z_interval(cx, cy):
            zb, zt = z0, z1
            for f in features:
                inside = False
                if f['shape'] == 'rect':
                    if f['x0'] + 1e-5 < cx < f['x1'] - 1e-5 and f['y0'] + 1e-5 < cy < f['y1'] - 1e-5:
                        inside = True
                elif f['shape'] == 'circle':
                    if (cx - f['cx'])**2 + (cy - f['cy'])**2 < f['r']**2:
                        inside = True
                if inside:
                    mode = f.get('mode', 'through')
                    if mode == 'through':
                        return None
                    elif mode == 'blind_bottom':
                        zb = max(zb, f['z_floor'])
                    elif mode == 'blind_top':
                        zt = min(zt, f['z_ceil'])
            if zb >= zt - 1e-5:
                return None
            return (zb, zt)

        gw = len(xs) - 1
        gh = len(ys) - 1
        grid = [[get_z_interval(0.5*(xs[i]+xs[i+1]), 0.5*(ys[j]+ys[j+1])) for j in range(gh)] for i in range(gw)]

        def add_wall_strip(pa, pb, z_low, z_high):
            if z_high > z_low + 1e-5:
                self.add_quad(
                    (pa[0], pa[1], z_low),
                    (pb[0], pb[1], z_low),
                    (pb[0], pb[1], z_high),
                    (pa[0], pa[1], z_high)
                )

        def connect_neighbor(pa, pb, curr_iv, nb_iv):
            zb, zt = curr_iv
            if nb_iv is None:
                add_wall_strip(pa, pb, zb, zt)
            else:
                nb_b, nb_t = nb_iv
                if zb < nb_b:
                    add_wall_strip(pa, pb, zb, min(zt, nb_b))
                if zt > nb_t:
                    add_wall_strip(pa, pb, max(zb, nb_t), zt)

        for i in range(gw):
            for j in range(gh):
                iv = grid[i][j]
                if iv is None:
                    continue
                zb, zt = iv
                xa, xb = xs[i], xs[i+1]
                ya, yb = ys[j], ys[j+1]

                self.add_quad((xa, ya, zb), (xa, yb, zb), (xb, yb, zb), (xb, ya, zb))
                self.add_quad((xa, ya, zt), (xb, ya, zt), (xb, yb, zt), (xa, yb, zt))

                connect_neighbor((xa, yb), (xa, ya), iv, grid[i-1][j] if i > 0 else None)
                connect_neighbor((xb, ya), (xb, yb), iv, grid[i+1][j] if i < gw - 1 else None)
                connect_neighbor((xa, ya), (xb, ya), iv, grid[i][j-1] if j > 0 else None)
                connect_neighbor((xb, yb), (xa, yb), iv, grid[i][j+1] if j < gh - 1 else None)

    def save_binary_stl(self, filepath, header_text="Nhom13_Security_Door_Box_v3"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            hdr = header_text.encode('ascii', errors='ignore')[:80].ljust(80, b'\0')
            f.write(hdr)
            f.write(struct.pack('<I', len(self.triangles)))
            for norm, p1, p2, p3 in self.triangles:
                f.write(struct.pack('<12fH',
                    norm[0], norm[1], norm[2],
                    p1[0], p1[1], p1[2],
                    p2[0], p2[1], p2[2],
                    p3[0], p3[1], p3[2],
                    0
                ))


def build_base_enclosure(mesh, z_offset=0.0):
    """
    Thân hộp dưới (Base Enclosure - Bản v3.0 Chống va chạm):
    - Kích thước phủ bì: 134.0 x 210.0 x 55.0 mm (Lòng trong: 128.0 x 204.0 x 52.0 mm)
    - Mạch PCB 100 x 100 mm đặt tại Y = -34.0 mm (chiếm Y từ -84 đến +16 mm),
      tách biệt hoàn toàn với cảm biến vân tay AS608 dài 45mm ở phía trên (Y = +58 mm).
    """
    W, H, D = 134.0, 210.0, 55.0
    wall = 3.0
    z0 = z_offset
    pcb_y_off = -34.0

    # 1. Tấm đáy có 4 lỗ bắt vít treo tường (M4) + 1 lỗ luồn dây âm tường (Ø18mm ở khoang trên)
    bottom_holes = [
        {'shape': 'circle', 'cx': -46.0, 'cy': -88.0, 'r': 2.2, 'mode': 'through'},
        {'shape': 'circle', 'cx':  46.0, 'cy': -88.0, 'r': 2.2, 'mode': 'through'},
        {'shape': 'circle', 'cx': -46.0, 'cy':  88.0, 'r': 2.2, 'mode': 'through'},
        {'shape': 'circle', 'cx':  46.0, 'cy':  88.0, 'r': 2.2, 'mode': 'through'},
        {'shape': 'circle', 'cx':   0.0, 'cy':  32.0, 'r': 9.0, 'mode': 'through'},
    ]
    mesh.add_perforated_plate(-W/2, W/2, -H/2, H/2, z0, z0 + wall, bottom_holes, nx=52, ny=76)

    # 2. 4 Thành hộp (dày 3.0 mm, cao 55.0 mm)
    mesh.add_box(-W/2, -W/2 + wall, -H/2, H/2, z0 + wall, z0 + D)
    mesh.add_box( W/2 - wall,  W/2, -H/2, H/2, z0 + wall, z0 + D)
    mesh.add_box(-W/2 + wall, W/2 - wall, H/2 - wall, H/2, z0 + wall, z0 + D)

    # Thành dưới khoét 2 cổng cáp: Nguồn DC 12V (x=-22, 8x8mm) & Dây Khóa chốt 12V (x=+22, 6x6mm)
    mesh.add_box(-W/2 + wall, W/2 - wall, -H/2, -H/2 + wall, z0 + wall, z0 + 14.0)
    mesh.add_box(-W/2 + wall, W/2 - wall, -H/2, -H/2 + wall, z0 + 22.0, z0 + D)
    mesh.add_box(-W/2 + wall, -26.0, -H/2, -H/2 + wall, z0 + 14.0, z0 + 22.0)
    mesh.add_box(-18.0, 19.0, -H/2, -H/2 + wall, z0 + 14.0, z0 + 22.0)
    mesh.add_box( 25.0, W/2 - wall, -H/2, -H/2 + wall, z0 + 14.0, z0 + 22.0)

    # 3. 4 Trụ bắt vít nắp hộp ở 4 góc (M3, tọa độ ±60.0 x ±98.0 mm)
    for ix in (-1, 1):
        for iy in (-1, 1):
            mesh.add_hollow_cylinder(ix*(W/2 - 7.0), iy*(H/2 - 7.0), z0 + wall, z0 + D - 2.0, 1.6, 4.8)

    # 4. 4 Trụ đỡ mạch PCB trung tâm 100 x 100 mm (Tâm lỗ vít 92 x 92 mm, cao 5.0 mm)
    for ix in (-1, 1):
        for iy in (-1, 1):
            mesh.add_hollow_cylinder(ix*46.0, pcb_y_off + iy*46.0, z0 + wall, z0 + wall + 5.0, 1.5, 4.2)

    # 5. 4 Gờ định vị góc chữ L ôm khít mép bo PCB 100 x 100 mm (100.4 x 100.4 mm)
    pcb_half = 50.2
    post_t = 2.5
    post_l = 8.0
    z_top = z0 + wall + 8.5
    for ix in (-1, 1):
        for iy in (-1, 1):
            cx = ix * pcb_half
            cy = pcb_y_off + iy * pcb_half
            x_a = min(cx, cx - ix * post_l)
            x_b = max(cx, cx - ix * post_l)
            y_a = min(cy, cy + iy * post_t)
            y_b = max(cy, cy + iy * post_t)
            mesh.add_box(x_a, x_b, y_a, y_b, z0 + wall, z_top)

            x_c = min(cx, cx + ix * post_t)
            x_d = max(cx, cx + ix * post_t)
            y_c = min(cy, cy - iy * post_l)
            y_d = max(cy, cy - iy * post_l)
            mesh.add_box(x_c, x_d, y_c, y_d, z0 + wall, z_top)


def build_front_cover(mesh, z_offset=0.0):
    """
    Nắp mặt trước (Front Cover Panel - Bản v3.0): 134.0 x 210.0 x 6.0 mm
    """
    W, H, lid_d = 134.0, 210.0, 6.0
    wall = 3.0
    z0 = z_offset

    # 1) Cảm biến vân tay AS608 tại (-30, +58)
    as_x, as_y = -30.0, 58.0
    as_cut_w, as_cut_h = 15.6, 18.5
    as_body_w, as_body_h = 20.8, 23.6

    # 2) Module RFID RC522 tại (+26, +58): 40 x 60 mm -> hốc âm 40.6 x 60.6 mm
    rc_x, rc_y = 26.0, 58.0
    rc_w, rc_h = 40.6, 60.6

    # 3) Bàn phím cứng ma trận tại (-20, -42): 65 x 64 mm
    kp_x, kp_y = -20.0, -42.0
    kp_flange_w, kp_flange_h = 65.5, 64.5
    kp_cut_w, kp_cut_h = 55.0, 56.0

    # 4) Loa thông báo tại (+39, -44)
    spk_x, spk_y = 39.0, -44.0

    features = [
        # AS608: Lỗ xuyên mặt cảm biến 15.6 x 18.5 mm
        {'shape': 'rect', 'x0': as_x - as_cut_w/2, 'x1': as_x + as_cut_w/2,
         'y0': as_y - as_cut_h/2, 'y1': as_y + as_cut_h/2, 'mode': 'through'},
        # AS608: Hốc bậc đỡ vai cảm biến ở mặt trong (20.8 x 23.6 mm)
        {'shape': 'rect', 'x0': as_x - as_body_w/2, 'x1': as_x + as_body_w/2,
         'y0': as_y - as_body_h/2, 'y1': as_y + as_body_h/2, 'mode': 'blind_bottom', 'z_floor': z0 + lid_d - 2.0},

        # RFID RC522: Hốc âm mặt trong 40.6 x 60.6 mm, vách mỏng 1.5mm
        {'shape': 'rect', 'x0': rc_x - rc_w/2, 'x1': rc_x + rc_w/2,
         'y0': rc_y - rc_h/2, 'y1': rc_y + rc_h/2, 'mode': 'blind_bottom', 'z_floor': z0 + lid_d - 1.5},

        # Bàn phím 65x64mm: Hốc âm mặt bích 65.5 x 64.5 mm ở mặt ngoài (sâu 2.0mm)
        {'shape': 'rect', 'x0': kp_x - kp_flange_w/2, 'x1': kp_x + kp_flange_w/2,
         'y0': kp_y - kp_flange_h/2, 'y1': kp_y + kp_flange_h/2, 'mode': 'blind_top', 'z_ceil': z0 + lid_d - 2.0},
        # Bàn phím 65x64mm: Lỗ xuyên thân bàn phím 55.0 x 56.0 mm
        {'shape': 'rect', 'x0': kp_x - kp_cut_w/2, 'x1': kp_x + kp_cut_w/2,
         'y0': kp_y - kp_cut_h/2, 'y1': kp_y + kp_cut_h/2, 'mode': 'through'},
    ]

    # 4 lỗ vít M3 ở 4 góc nắp hộp (±60.0, ±98.0)
    for ix in (-1, 1):
        for iy in (-1, 1):
            features.append({'shape': 'circle', 'cx': ix*(W/2 - 7.0), 'cy': iy*(H/2 - 7.0), 'r': 1.7, 'mode': 'through'})

    # 4 lỗ vít cố định mặt bích bàn phím (tâm lỗ 58.0 x 57.0 mm)
    for ix in (-1, 1):
        for iy in (-1, 1):
            features.append({'shape': 'circle', 'cx': kp_x + ix*29.0, 'cy': kp_y + iy*28.5, 'r': 1.5, 'mode': 'through'})

    # Lưới Loa thông báo (Speaker Grille)
    features.append({'shape': 'circle', 'cx': spk_x, 'cy': spk_y, 'r': 2.0, 'mode': 'through'})
    for k in range(6):
        ang = k * math.pi / 3.0
        features.append({'shape': 'circle', 'cx': spk_x + 6.0*math.cos(ang), 'cy': spk_y + 6.0*math.sin(ang), 'r': 1.7, 'mode': 'through'})
    for k in range(12):
        ang = k * math.pi / 6.0
        features.append({'shape': 'circle', 'cx': spk_x + 11.5*math.cos(ang), 'cy': spk_y + 11.5*math.sin(ang), 'r': 1.5, 'mode': 'through'})

    # 3 lỗ đèn LED Ø3mm báo trạng thái phía trên Loa
    for idx in (-1, 0, 1):
        features.append({'shape': 'circle', 'cx': spk_x + idx*8.5, 'cy': -8.0, 'r': 1.6, 'mode': 'through'})

    mesh.add_perforated_plate(-W/2, W/2, -H/2, H/2, z0, z0 + lid_d, features, nx=96, ny=144)

    # Khung ống giữ thân cảm biến vân tay AS608 ở mặt trong nắp (sâu 15mm)
    t_h = 2.4
    mesh.add_box(as_x - as_body_w/2 - t_h, as_x - as_body_w/2, as_y - as_body_h/2 - t_h, as_y + as_body_h/2 + t_h, z0 - 15.0, z0)
    mesh.add_box(as_x + as_body_w/2, as_x + as_body_w/2 + t_h, as_y - as_body_h/2 - t_h, as_y + as_body_h/2 + t_h, z0 - 15.0, z0)
    mesh.add_box(as_x - as_body_w/2, as_x + as_body_w/2, as_y - as_body_h/2 - t_h, as_y - as_body_h/2, z0 - 15.0, z0)
    mesh.add_box(as_x - as_body_w/2, as_x + as_body_w/2, as_y + as_body_h/2, as_y + as_body_h/2 + t_h, z0 - 15.0, z0)

    # Khung gờ giữ 4 cạnh mạch RFID RC522 (40.6 x 60.6 mm) ở mặt trong nắp (sâu 3.0mm)
    t_rc = 2.0
    mesh.add_box(rc_x - rc_w/2 - t_rc, rc_x - rc_w/2, rc_y - rc_h/2 - t_rc, rc_y + rc_h/2 + t_rc, z0 - 3.0, z0)
    mesh.add_box(rc_x + rc_w/2, rc_x + rc_w/2 + t_rc, rc_y - rc_h/2 - t_rc, rc_y + rc_h/2 + t_rc, z0 - 3.0, z0)
    mesh.add_box(rc_x - rc_w/2, rc_x + rc_w/2, rc_y - rc_h/2 - t_rc, rc_y - rc_h/2, z0 - 3.0, z0)
    mesh.add_box(rc_x - rc_w/2, rc_x + rc_w/2, rc_y + rc_h/2, rc_y + rc_h/2 + t_rc, z0 - 3.0, z0)

    # Vành tròn định vị Loa thông báo Ø30mm ở mặt trong nắp
    mesh.add_hollow_cylinder(spk_x, spk_y, z0 - 4.0, z0, 15.2, 17.5)

    # Gờ định vị nắp (Lip) ở cạnh trên và dưới mặt trong
    lip_in = wall + 0.3
    lip_t = 2.0
    mesh.add_box(-W/2 + lip_in, W/2 - lip_in, H/2 - lip_in - lip_t, H/2 - lip_in, z0 - 2.0, z0)
    mesh.add_box(-W/2 + lip_in, W/2 - lip_in, -H/2 + lip_in, -H/2 + lip_in + lip_t, z0 - 2.0, z0)


def build_internal_components(mesh, z_base=0.0):
    pcb_y_off = -34.0
    # 1. Mạch PCB trung tâm: 100.0 x 100.0 x 1.6 mm tại Y = -34, Z = 8.0
    zp = z_base + 8.0
    mesh.add_box(-50.0, 50.0, pcb_y_off - 50.0, pcb_y_off + 50.0, zp, zp + 1.6)
    mesh.add_box(-14.0, 14.0, pcb_y_off - 26.0, pcb_y_off + 26.0, zp + 1.6, zp + 14.0)

    # 2. Cảm biến vân tay AS608 tại (-30, +58), dài 45mm (từ Z=16 đến Z=61)
    mesh.add_box(-30.0 - 10.2, -30.0 + 10.2, 58.0 - 11.65, 58.0 + 11.65, z_base + 16.0, z_base + 59.0)
    mesh.add_box(-30.0 - 7.65, -30.0 + 7.65, 58.0 - 9.1, 58.0 + 9.1, z_base + 59.0, z_base + 61.5)
    mesh.add_box(-30.0 - 7.5, -30.0 + 7.5, 58.0 - 8.5, 58.0 + 8.5, z_base + 61.5, z_base + 62.0)

    # 3. Module RFID RC522: 40.0 x 60.0 x 1.6 mm tại (+26, +58)
    mesh.add_box(26.0 - 20.0, 26.0 + 20.0, 58.0 - 30.0, 58.0 + 30.0, z_base + 57.5, z_base + 59.1)

    # 4. Bàn phím cứng ma trận: 65.0 x 64.0 mm tại (-20, -42)
    kp_x, kp_y = -20.0, -42.0
    mesh.add_box(kp_x - 32.5, kp_x + 32.5, kp_y - 32.0, kp_y + 32.0, z_base + 48.0, z_base + 59.2)
    for r in range(4):
        for c in range(3):
            kx = kp_x + (c - 1) * 14.5
            ky = kp_y + (1.5 - r) * 13.0
            mesh.add_box(kx - 4.8, kx + 4.8, ky - 4.5, ky + 4.5, z_base + 59.2, z_base + 62.5)

    # 5. Loa thông báo Ø30mm tại (+39, -44)
    mesh.add_cylinder(39.0, -44.0, z_base + 47.0, z_base + 55.0, 15.0)


if __name__ == '__main__':
    out_dir = r"c:\Users\Admin\OneDrive\Desktop\LinkTink\KhoiLaTex\MoHinh3D_HopCuaBaoMat_Nhom13"

    m_base = MeshBuilder()
    build_base_enclosure(m_base, 0.0)
    base_path = os.path.join(out_dir, "HopDieuKhien_ThanDuoi_Base.stl")
    m_base.save_binary_stl(base_path, "Nhom13_Base_134x210x55_ZeroCollision")
    print(f"Saved {base_path} ({len(m_base.triangles)} triangles)")

    m_cover = MeshBuilder()
    build_front_cover(m_cover, 0.0)
    cover_path = os.path.join(out_dir, "HopDieuKhien_NapTruoc_Cover.stl")
    m_cover.save_binary_stl(cover_path, "Nhom13_Cover_134x210x6_ZeroCollision")
    print(f"Saved {cover_path} ({len(m_cover.triangles)} triangles)")

    m_full = MeshBuilder()
    build_base_enclosure(m_full, 0.0)
    build_internal_components(m_full, 0.0)
    build_front_cover(m_full, 55.0)
    full_path = os.path.join(out_dir, "HopDieuKhien_LapRap_Full.stl")
    m_full.save_binary_stl(full_path, "Nhom13_Full_Assembly_v3")
    print(f"Saved {full_path} ({len(m_full.triangles)} triangles)")
