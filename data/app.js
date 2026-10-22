/**
 * SmartDoor Security System - Minimalist Web App Client (Nhóm 13)
 * Thiết kế theo phong cách shadcn/ui tối giản, sạch sẽ, dễ nhìn
 */

const SVG_LOCK = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`;
const SVG_UNLOCK = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>`;

const state = {
    isEspConnected: false,
    ws: null,
    doorUnlocked: false,
    unlockCountdown: 0,
    countdownTimer: null,
    keypadBuffer: "",
    wrongAttempts: 0,
    rfidLearningMode: false,

    config: {
        securityMode: 1, // 1: 1 lớp, 2: FP+PIN, 3: RFID+PIN, 4: FP+RFID
        dualTimeoutSec: 15,
        pinCode: "123456",
        unlockDurationSec: 5,
        maxWrongAttempts: 5
    },

    dualSession: {
        active: false,
        stage1Method: null,
        user: null,
        expiresAt: 0,
        timer: null
    },

    fingerprints: [
        { id: 1, name: "Nguyễn Tuấn Sơn (Ngón trỏ phải)", addedAt: "22/10/2026 08:40" },
        { id: 2, name: "Vũ Hữu Hoạt (Ngón trỏ phải)", addedAt: "22/10/2026 08:42" }
    ],

    rfidCards: [
        { uid: "A3:4F:8B:12", name: "Nguyễn Tuấn Sơn (Thẻ S50)", addedAt: "22/10/2026 08:30" },
        { uid: "9B:11:C4:7E", name: "Vũ Hữu Hoạt (Móc khóa NFC)", addedAt: "22/10/2026 08:35" }
    ],

    logs: [
        {
            time: "22/10/2026 13:30:12",
            method: "FINGERPRINT",
            user: "Nguyễn Tuấn Sơn (ID #1)",
            valid: true
        },
        {
            time: "22/10/2026 13:25:40",
            method: "RFID",
            user: "Vũ Hữu Hoạt (9B:11:C4:7E)",
            valid: true
        },
        {
            time: "22/10/2026 13:18:05",
            method: "KEYPAD",
            user: "Nhập sai mã PIN (****)",
            valid: false
        }
    ]
};

document.addEventListener("DOMContentLoaded", () => {
    loadLocalBackup();
    initTabs();
    initEventListeners();
    renderAll();
    connectWebSocket();
});

function loadLocalBackup() {
    try {
        const saved = localStorage.getItem("smartdoor_nhom13_state");
        if (saved) {
            const parsed = JSON.parse(saved);
            if (parsed.config) state.config = parsed.config;
            if (parsed.fingerprints) state.fingerprints = parsed.fingerprints;
            if (parsed.rfidCards) state.rfidCards = parsed.rfidCards;
            if (parsed.logs) state.logs = parsed.logs;
        }
    } catch (e) {}
}

function saveLocalBackup() {
    try {
        localStorage.setItem("smartdoor_nhom13_state", JSON.stringify({
            config: state.config,
            fingerprints: state.fingerprints,
            rfidCards: state.rfidCards,
            logs: state.logs
        }));
    } catch (e) {}
}

function connectWebSocket() {
    const host = window.location.hostname;
    const isCloudDemo =
        window.location.protocol === "file:" ||
        host === "localhost" ||
        host === "127.0.0.1" ||
        host.endsWith(".vercel.app") ||
        host.endsWith(".github.io") ||
        host.endsWith(".netlify.app");

    if (isCloudDemo) {
        setConnectionMode(false);
        return;
    }

    const wsUrl = `ws://${window.location.host}/ws`;
    try {
        state.ws = new WebSocket(wsUrl);

        state.ws.onopen = () => {
            setConnectionMode(true);
            showToast("Đã kết nối với ESP32");
            sendCommand({ action: "GET_STATE" });
        };

        state.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleEspMessage(data);
            } catch (err) {}
        };

        state.ws.onclose = () => {
            setConnectionMode(false);
            setTimeout(connectWebSocket, 4000);
        };
    } catch (err) {
        setConnectionMode(false);
    }
}

function setConnectionMode(isEsp) {
    state.isEspConnected = isEsp;
    const modeBadge = document.getElementById("modeBadge");
    const wsStatusText = document.getElementById("wsStatusText");

    if (isEsp) {
        modeBadge.textContent = "ESP32 Wi-Fi";
        modeBadge.className = "badge badge-success";
        wsStatusText.textContent = "Đã kết nối mạch";
    } else {
        modeBadge.textContent = "Chế độ Mô phỏng";
        modeBadge.className = "badge badge-neutral";
        wsStatusText.textContent = "Trực tuyến";
    }
}

function sendCommand(payload) {
    if (state.isEspConnected && state.ws && state.ws.readyState === WebSocket.OPEN) {
        state.ws.send(JSON.stringify(payload));
        return true;
    }
    return false;
}

function handleEspMessage(data) {
    if (data.type === "FULL_SYNC") {
        if (data.config) state.config = data.config;
        if (data.fingerprints) state.fingerprints = data.fingerprints;
        if (data.rfidCards) state.rfidCards = data.rfidCards;
        if (data.logs) state.logs = data.logs;
        if (data.doorUnlocked !== undefined) {
            updateDoorVisual(data.doorUnlocked, data.unlockDurationSec || state.config.unlockDurationSec);
        }
        renderAll();
    } else if (data.type === "ACCESS_EVENT") {
        recordAccessEvent(data.method, data.user, data.valid, data.lcd1, data.lcd2, false);
    } else if (data.type === "LCD_UPDATE") {
        updateLcdScreen(data.line1, data.line2);
    } else if (data.type === "RFID_SCANNED_LEARN") {
        document.getElementById("rfidUidInput").value = data.uid;
        state.rfidLearningMode = false;
        showToast(`Đã đọc mã UID: ${data.uid}`);
    } else if (data.type === "FP_ENROLL_STATUS") {
        const box = document.getElementById("fpEnrollProgress");
        const txt = document.getElementById("fpEnrollText");
        box.style.display = "flex";
        txt.textContent = data.message;
        if (data.done) {
            setTimeout(() => { box.style.display = "none"; }, 2500);
        }
    }
}

function initTabs() {
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            switchTab(btn.dataset.tab);
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll(".tab-btn").forEach(b => {
        b.classList.toggle("active", b.dataset.tab === tabId);
    });
    document.querySelectorAll(".tab-content").forEach(sec => {
        sec.classList.toggle("active", sec.id === tabId);
    });
}

function initEventListeners() {
    document.getElementById("btnRemoteUnlock").addEventListener("click", () => {
        if (!sendCommand({ action: "REMOTE_UNLOCK" })) {
            recordAccessEvent("WEB", "Quản trị viên (Mở từ Web)", true, "MO CUA TU WEB", "XIN MOI VAO!");
        }
    });

    document.getElementById("btnForceLock").addEventListener("click", () => {
        if (!sendCommand({ action: "FORCE_LOCK" })) {
            lockDoorNow();
            showToast("Đã đóng khóa chốt 12V");
        }
    });

    document.getElementById("filterMethod").addEventListener("change", () => {
        renderLogs();
    });

    document.getElementById("btnExportCsv").addEventListener("click", exportLogsToCsv);

    document.getElementById("btnClearLogs").addEventListener("click", () => {
        if (confirm("Xóa toàn bộ lịch sử ra vào?")) {
            state.logs = [];
            saveLocalBackup();
            sendCommand({ action: "CLEAR_LOGS" });
            renderAll();
            showToast("Đã xóa lịch sử");
        }
    });

    document.getElementById("formAddFingerprint").addEventListener("submit", (e) => {
        e.preventDefault();
        const id = parseInt(document.getElementById("fpIdInput").value, 10);
        const name = document.getElementById("fpNameInput").value.trim();

        if (state.fingerprints.some(f => f.id === id)) {
            showToast(`ID vân tay #${id} đã tồn tại`);
            return;
        }

        if (!sendCommand({ action: "ENROLL_FP", id, name })) {
            simulateFingerprintEnrollment(id, name);
        }
    });

    document.getElementById("btnScanRfidLearn").addEventListener("click", () => {
        state.rfidLearningMode = true;
        updateLcdScreen("CHE DO THEM THE", "MOI QUET THE...");
        if (!sendCommand({ action: "START_RFID_LEARN" })) {
            const randomHex = () => Math.floor(16 + Math.random() * 239).toString(16).toUpperCase();
            const mockUid = `${randomHex()}:${randomHex()}:${randomHex()}:${randomHex()}`;
            setTimeout(() => {
                document.getElementById("rfidUidInput").value = mockUid;
                updateLcdScreen("DA DOC MA THE!", mockUid);
                showToast(`Đã đọc mã thẻ: ${mockUid}`);
                state.rfidLearningMode = false;
            }, 600);
        } else {
            showToast("Đưa thẻ RFID vào đầu đọc RC522...");
        }
    });

    document.getElementById("formAddRfid").addEventListener("submit", (e) => {
        e.preventDefault();
        const uid = document.getElementById("rfidUidInput").value.trim().toUpperCase();
        const name = document.getElementById("rfidNameInput").value.trim();

        if (state.rfidCards.some(c => c.uid === uid)) {
            showToast(`Mã thẻ ${uid} đã tồn tại`);
            return;
        }

        state.rfidCards.push({ uid, name, addedAt: formatNow() });
        saveLocalBackup();
        sendCommand({ action: "ADD_RFID", uid, name });

        document.getElementById("rfidUidInput").value = "";
        document.getElementById("rfidNameInput").value = "";
        renderAll();
        showToast(`Đã thêm thẻ cho ${name}`);
    });

    document.getElementById("btnTogglePin").addEventListener("click", () => {
        const input = document.getElementById("settingPinCode");
        const isPass = input.type === "password";
        input.type = isPass ? "text" : "password";
        document.getElementById("btnTogglePin").textContent = isPass ? "Ẩn" : "Hiện";
    });

    document.getElementById("settingSecMode").addEventListener("change", (e) => {
        updateSecModeHint(parseInt(e.target.value, 10));
    });

    document.getElementById("formSettings").addEventListener("submit", (e) => {
        e.preventDefault();
        state.config.securityMode = parseInt(document.getElementById("settingSecMode").value, 10) || 1;
        state.config.dualTimeoutSec = parseInt(document.getElementById("settingDualTimeout").value, 10) || 15;
        state.config.pinCode = document.getElementById("settingPinCode").value.trim();
        state.config.unlockDurationSec = parseInt(document.getElementById("settingUnlockTime").value, 10) || 5;
        state.config.maxWrongAttempts = parseInt(document.getElementById("settingMaxAttempts").value, 10) || 5;

        // Reset bất kỳ phiên 2 lớp đang dang dở
        cancelDualSession();

        saveLocalBackup();
        sendCommand({ action: "SAVE_CONFIG", config: state.config });
        updateLcdScreen("CAP NHAT CHE DO", getSecModeLabelShort(state.config.securityMode));
        renderAll();
        showToast("Đã lưu cấu hình chế độ bảo mật");
    });

    const simDrawer = document.getElementById("simulatorPanel");
    const simBody = document.getElementById("simBodyContent");
    const minBtn = document.getElementById("minSimBtn");

    document.getElementById("toggleSimBtn").addEventListener("click", () => {
        simDrawer.classList.toggle("hidden");
    });
    document.getElementById("closeSimBtn").addEventListener("click", () => {
        simDrawer.classList.add("hidden");
    });
    if (minBtn && simBody) {
        minBtn.addEventListener("click", () => {
            const isMin = simBody.classList.toggle("minimized");
            minBtn.innerHTML = isMin ? "&#43;" : "&ndash;";
        });
    }

    initDraggableSimulator(simDrawer, document.getElementById("simDragHeader"));
}

function initDraggableSimulator(panel, handle) {
    if (!panel || !handle) return;

    let isDragging = false;
    let startX = 0, startY = 0;
    let initialLeft = 0, initialTop = 0;

    handle.addEventListener("pointerdown", (e) => {
        // Không kéo nếu người dùng bấm vào nút Đóng / Thu gọn
        if (e.target.closest("button")) return;

        isDragging = true;
        panel.classList.add("dragging");

        const rect = panel.getBoundingClientRect();
        initialLeft = rect.left;
        initialTop = rect.top;
        startX = e.clientX;
        startY = e.clientY;

        // Chuyển từ định vị bottom/right sang top/left để kéo mượt mà
        panel.style.left = `${initialLeft}px`;
        panel.style.top = `${initialTop}px`;
        panel.style.right = "auto";
        panel.style.bottom = "auto";

        handle.setPointerCapture(e.pointerId);
    });

    handle.addEventListener("pointermove", (e) => {
        if (!isDragging) return;

        const dx = e.clientX - startX;
        const dy = e.clientY - startY;

        const maxLeft = window.innerWidth - panel.offsetWidth - 8;
        const maxTop = window.innerHeight - panel.offsetHeight - 8;

        const newLeft = Math.max(8, Math.min(initialLeft + dx, maxLeft));
        const newTop = Math.max(8, Math.min(initialTop + dy, maxTop));

        panel.style.left = `${newLeft}px`;
        panel.style.top = `${newTop}px`;
    });

    const stopDrag = (e) => {
        if (!isDragging) return;
        isDragging = false;
        panel.classList.remove("dragging");
        try {
            handle.releasePointerCapture(e.pointerId);
        } catch (_) {}
    };

    handle.addEventListener("pointerup", stopDrag);
    handle.addEventListener("pointercancel", stopDrag);
}

function recordAccessEvent(method, user, valid, lcdLine1, lcdLine2, triggerDoor = true) {
    const entry = {
        time: formatNow(),
        method,
        user,
        valid
    };
    state.logs.unshift(entry);
    if (state.logs.length > 50) state.logs.pop();

    document.getElementById("lastEventTitle").textContent = `${getMethodLabel(method)} — ${user}`;
    document.getElementById("lastEventTime").textContent = `${entry.time} • ${valid ? "Hợp lệ" : "Từ chối"}`;

    const alertBadge = document.getElementById("systemAlertBadge");

    if (valid) {
        state.wrongAttempts = 0;
        alertBadge.textContent = "Hệ thống an toàn";
        alertBadge.className = "badge badge-success";
        updateLcdScreen(lcdLine1 || "XAC THUC DUNG!", lcdLine2 || "CUA DANG MO...");
        if (triggerDoor) {
            updateDoorVisual(true, state.config.unlockDurationSec);
        }
        showToast(`Đã mở cửa: ${user}`);
    } else {
        state.wrongAttempts++;
        alertBadge.textContent = `Cảnh báo sai (${state.wrongAttempts}/${state.config.maxWrongAttempts})`;
        alertBadge.className = "badge badge-danger";
        updateLcdScreen(lcdLine1 || "TRUY CAP SAI!", lcdLine2 || `SAI LAN ${state.wrongAttempts}/${state.config.maxWrongAttempts}`);
        showToast(`Từ chối truy cập: ${user}`);

        setTimeout(() => {
            if (!state.doorUnlocked) {
                updateLcdScreen(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
            }
        }, 3000);
    }

    saveLocalBackup();
    renderAll();
}

function updateDoorVisual(unlocked, durationSec) {
    state.doorUnlocked = unlocked;
    const ring = document.getElementById("lockRing");
    const icon = document.getElementById("lockIcon");
    const title = document.getElementById("doorStateText");
    const sub = document.getElementById("doorCountdownText");
    const metricDoor = document.getElementById("metricDoorStatus");
    const btnUnlock = document.getElementById("btnRemoteUnlock");
    const btnLock = document.getElementById("btnForceLock");

    if (state.countdownTimer) {
        clearInterval(state.countdownTimer);
        state.countdownTimer = null;
    }

    if (unlocked) {
        ring.className = "lock-indicator unlocked";
        icon.innerHTML = SVG_UNLOCK;
        title.textContent = "CỬA ĐANG MỞ";
        metricDoor.textContent = "Đang mở";
        btnUnlock.style.display = "none";
        btnLock.style.display = "inline-flex";

        state.unlockCountdown = durationSec;
        sub.textContent = `Tự động đóng khóa sau ${state.unlockCountdown} giây`;

        state.countdownTimer = setInterval(() => {
            state.unlockCountdown--;
            if (state.unlockCountdown <= 0) {
                lockDoorNow();
            } else {
                sub.textContent = `Tự động đóng khóa sau ${state.unlockCountdown} giây`;
            }
        }, 1000);
    } else {
        lockDoorNow();
    }
}

function lockDoorNow() {
    if (state.countdownTimer) {
        clearInterval(state.countdownTimer);
        state.countdownTimer = null;
    }
    state.doorUnlocked = false;
    document.getElementById("lockRing").className = "lock-indicator locked";
    document.getElementById("lockIcon").innerHTML = SVG_LOCK;
    document.getElementById("doorStateText").textContent = "CỬA ĐANG KHÓA";
    document.getElementById("metricDoorStatus").textContent = "Đang khóa";
    document.getElementById("doorCountdownText").textContent = "Chốt khóa điện từ 12V đang đóng";
    document.getElementById("btnRemoteUnlock").style.display = "inline-flex";
    document.getElementById("btnForceLock").style.display = "none";

    updateLcdScreen(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
}

function updateLcdScreen(line1, line2) {
    const pad16 = (str) => (str || "").substring(0, 16).padEnd(16, " ");
    document.getElementById("lcdLine1").textContent = pad16(line1);
    document.getElementById("lcdLine2").textContent = pad16(line2);
}

function cancelDualSession() {
    if (state.dualSession.timer) {
        clearTimeout(state.dualSession.timer);
    }
    state.dualSession = {
        active: false,
        stage1Method: null,
        user: null,
        expiresAt: 0,
        timer: null
    };
}

function handleAuthInput(method, user, valid, defaultLcd1, defaultLcd2) {
    if (!valid) {
        cancelDualSession();
        recordAccessEvent(method, user, false, defaultLcd1 || "XAC THUC THAT BAI", defaultLcd2 || "TU CHOI TRUY CAP");
        return;
    }

    const mode = state.config.securityMode || 1;

    // Chế độ 1 LỚP hoặc Mở khóa từ xa Web -> Mở ngay
    if (mode === 1 || method === "WEB") {
        cancelDualSession();
        recordAccessEvent(method, user, true, defaultLcd1 || "XAC THUC DUNG!", defaultLcd2 || "CUA DANG MO...");
        return;
    }

    // ==================== CÁC CHẾ ĐỘ 2 LỚP (2FA) ====================
    // Mode 2: Vân tay + PIN
    // Mode 3: Thẻ RFID + PIN
    // Mode 4: Vân tay + Thẻ RFID

    if (!state.dualSession.active) {
        // --- GIAI ĐOẠN 1: Kiểm tra phương thức đầu tiên có hợp lệ cho chế độ hiện tại không ---
        let isStage1Valid = false;
        let expectedNext = "";

        if (mode === 2 && method === "FINGERPRINT") {
            isStage1Valid = true;
            expectedNext = "NHAP PIN + #";
        } else if (mode === 3 && method === "RFID") {
            isStage1Valid = true;
            expectedNext = "NHAP PIN + #";
        } else if (mode === 4 && (method === "FINGERPRINT" || method === "RFID")) {
            isStage1Valid = true;
            expectedNext = method === "FINGERPRINT" ? "QUET THE RFID" : "QUET VAN TAY";
        }

        if (isStage1Valid) {
            state.dualSession.active = true;
            state.dualSession.stage1Method = method;
            state.dualSession.user = user;
            state.dualSession.expiresAt = Date.now() + (state.config.dualTimeoutSec * 1000);

            if (state.dualSession.timer) clearTimeout(state.dualSession.timer);
            state.dualSession.timer = setTimeout(() => {
                cancelDualSession();
                updateLcdScreen("HET THOI GIAN 2FA", "PHIEN BI HUY");
                showToast("Hết thời gian chờ xác thực lớp thứ 2!", "warning");
                setTimeout(() => {
                    if (!state.doorUnlocked) updateLcdScreen(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
                }, 2000);
            }, state.config.dualTimeoutSec * 1000);

            updateLcdScreen("XAC THUC LOP 1 OK", expectedNext);
            showToast(`Lớp 1 thành công: ${user}. Vui lòng thực hiện lớp 2 (${expectedNext})`);
            return;
        } else {
            // Nhập sai thứ tự hoặc phương thức không đúng yêu cầu lớp 1
            let needMethod = "";
            if (mode === 2) needMethod = "Vân tay trước";
            else if (mode === 3) needMethod = "Thẻ RFID trước";
            else if (mode === 4) needMethod = "Vân tay hoặc Thẻ trước";
            
            updateLcdScreen("YEU CAU 2 LOP!", needMethod);
            showToast(`Chế độ 2 lớp: Vui lòng xác thực ${needMethod}`, "warning");
            return;
        }
    } else {
        // --- GIAI ĐOẠN 2: Kiểm tra phương thức thứ hai ---
        let isStage2Valid = false;
        const prevMethod = state.dualSession.stage1Method;

        if (mode === 2 && prevMethod === "FINGERPRINT" && method === "KEYPAD") {
            isStage2Valid = true;
        } else if (mode === 3 && prevMethod === "RFID" && method === "KEYPAD") {
            isStage2Valid = true;
        } else if (mode === 4 && (
            (prevMethod === "FINGERPRINT" && method === "RFID") ||
            (prevMethod === "RFID" && method === "FINGERPRINT")
        )) {
            isStage2Valid = true;
        }

        if (isStage2Valid) {
            const combinedUser = `${state.dualSession.user} + ${getMethodLabel(method)}`;
            cancelDualSession();
            recordAccessEvent(`2FA (${getMethodLabelShort(prevMethod)}+${getMethodLabelShort(method)})`, combinedUser, true, "XAC THUC 2 LOP OK", "XIN MOI VAO!");
        } else {
            cancelDualSession();
            recordAccessEvent(method, `Lớp 2 không đúng (${user})`, false, "LOP 2 SAI!", "PHIEN BI HUY");
        }
    }
}

function simFingerprint(isValid) {
    if (isValid) {
        const user = state.fingerprints[0]
            ? `${state.fingerprints[0].name} (ID #${state.fingerprints[0].id})`
            : "Nguyễn Tuấn Sơn (ID #1)";
        handleAuthInput("FINGERPRINT", user, true, "VAN TAY HOP LE", "XIN CHAO SON!");
    } else {
        handleAuthInput("FINGERPRINT", "Vân tay không khớp AS608", false, "VAN TAY SAI!", "TU CHOI MO CUA");
    }
}

function simRfid(isValid) {
    if (isValid) {
        const card = state.rfidCards[0] || { uid: "A3:4F:8B:12", name: "Vũ Hữu Hoạt" };
        handleAuthInput("RFID", `${card.name} (${card.uid})`, true, "THE TU HOP LE", `CHAO: ${card.name.substring(0, 9)}`);
    } else {
        handleAuthInput("RFID", "Thẻ lạ (UID: FF:09:A2:1C)", false, "THE KHONG HOP LE", "UID: FF:09:A2:1C");
    }
}

function simKeypadPress(key) {
    if (key === "*") {
        state.keypadBuffer = "";
        updateLcdScreen("NHAP MAT KHAU:", "DA XOA BUFFER");
        return;
    }

    if (key === "C") {
        state.keypadBuffer = "";
        cancelDualSession();
        lockDoorNow();
        showToast("Đã khóa cửa từ phím C");
        return;
    }

    if (key === "#" || key === "D") {
        if (!state.keypadBuffer) return;
        const entered = state.keypadBuffer;
        state.keypadBuffer = "";

        if (entered === state.config.pinCode) {
            handleAuthInput("KEYPAD", "Nhập đúng mã PIN từ Keypad 4x4", true, "MAT KHAU DUNG!", "MO CUA KEYPAD");
        } else {
            handleAuthInput("KEYPAD", `Nhập sai PIN (${entered.length} số)`, false, "SAI MAT KHAU!", "VUI LONG THU LAI");
        }
        return;
    }

    if (key === "A" || key === "B") {
        updateLcdScreen(`PHIM CHUC NANG ${key}`, "NHAP PIN + #");
        return;
    }

    if (state.keypadBuffer.length < 8) {
        state.keypadBuffer += key;
        const masked = "*".repeat(state.keypadBuffer.length);
        updateLcdScreen("NHAP MAT KHAU:", `PIN: ${masked}`);
    }
}

function simulateFingerprintEnrollment(id, name) {
    const box = document.getElementById("fpEnrollProgress");
    const txt = document.getElementById("fpEnrollText");
    box.style.display = "flex";

    txt.textContent = `Bước 1/2: Đặt ngón tay lên cảm biến AS608 (ID #${id})...`;
    updateLcdScreen(`DANG KY ID #${id}`, "DAT NGON TAY 1..");

    setTimeout(() => {
        txt.textContent = "Bước 2/2: Nhấc ngón tay ra và đặt lại lần 2...";
        updateLcdScreen(`DANG KY ID #${id}`, "DAT LAI LAN 2...");
    }, 1200);

    setTimeout(() => {
        state.fingerprints.push({ id, name, addedAt: formatNow() });
        saveLocalBackup();
        renderAll();

        document.getElementById("fpIdInput").value = id + 1;
        document.getElementById("fpNameInput").value = "";
        updateLcdScreen("LUU THANH CONG!", `ID #${id} HOAN TAT`);
        showToast(`Đã đăng ký vân tay ID #${id}`);

        setTimeout(() => {
            box.style.display = "none";
            updateLcdScreen(" CUA BAO MAT 13 ", "TRANG THAI: KHOA");
        }, 1200);
    }, 2400);
}

// ==================== RENDER UI ====================
function renderAll() {
    renderStats();
    renderLogs();
    renderFingerprints();
    renderRfidCards();
    renderSettingsForm();
}

function renderStats() {
    const validCount = state.logs.filter(l => l.valid).length;
    const invalidCount = state.logs.filter(l => !l.valid).length;

    document.getElementById("statValidCount").textContent = validCount;
    document.getElementById("statInvalidCount").textContent = invalidCount;
    document.getElementById("statFpRegistered").textContent = state.fingerprints.length;
    document.getElementById("statRfidRegistered").textContent = state.rfidCards.length;
    document.getElementById("logCountBadge").textContent = state.logs.length;
}

function renderLogs() {
    const recentBody = document.getElementById("recentLogsBody");
    const fullBody = document.getElementById("fullLogsBody");
    const filter = document.getElementById("filterMethod").value;

    recentBody.innerHTML = state.logs.slice(0, 5).map(log => `
        <tr>
            <td class="mono" style="font-size:12px;color:var(--text-muted);">${log.time}</td>
            <td><span class="method-pill">${getMethodLabel(log.method)}</span></td>
            <td>${escapeHtml(log.user)}</td>
            <td>
                <span class="badge ${log.valid ? 'badge-success' : 'badge-danger'}">
                    ${log.valid ? 'Hợp lệ' : 'Từ chối'}
                </span>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="4" style="text-align:center;color:var(--text-muted);">Chưa có dữ liệu</td></tr>`;

    const filtered = filter === "ALL" ? state.logs : state.logs.filter(l => l.method === filter);
    fullBody.innerHTML = filtered.map((log, idx) => `
        <tr>
            <td style="color:var(--text-muted);">${idx + 1}</td>
            <td class="mono" style="font-size:12px;color:var(--text-muted);">${log.time}</td>
            <td><span class="method-pill">${getMethodLabel(log.method)}</span></td>
            <td>${escapeHtml(log.user)}</td>
            <td>
                <span class="badge ${log.valid ? 'badge-success' : 'badge-danger'}">
                    ${log.valid ? 'Hợp lệ' : 'Từ chối'}
                </span>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="5" style="text-align:center;color:var(--text-muted);">Không có bản ghi</td></tr>`;
}

function renderFingerprints() {
    const tbody = document.getElementById("fpListBody");
    tbody.innerHTML = state.fingerprints.map(fp => `
        <tr>
            <td class="mono">#${fp.id}</td>
            <td>${escapeHtml(fp.name)}</td>
            <td style="color:var(--text-muted);font-size:12px;">${fp.addedAt}</td>
            <td style="text-align:right;">
                <button class="btn btn-outline-danger btn-sm" onclick="deleteFingerprint(${fp.id})">Xóa</button>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="4" style="text-align:center;color:var(--text-muted);">Chưa có dữ liệu</td></tr>`;
}

function renderRfidCards() {
    const tbody = document.getElementById("rfidListBody");
    tbody.innerHTML = state.rfidCards.map(c => `
        <tr>
            <td><code>${escapeHtml(c.uid)}</code></td>
            <td>${escapeHtml(c.name)}</td>
            <td style="color:var(--text-muted);font-size:12px;">${c.addedAt}</td>
            <td style="text-align:right;">
                <button class="btn btn-outline-danger btn-sm" onclick="deleteRfid('${c.uid}')">Xóa</button>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="4" style="text-align:center;color:var(--text-muted);">Chưa có dữ liệu</td></tr>`;
}

function renderSettingsForm() {
    const mode = state.config.securityMode || 1;
    document.getElementById("settingSecMode").value = mode;
    document.getElementById("settingDualTimeout").value = state.config.dualTimeoutSec || 15;
    document.getElementById("settingPinCode").value = state.config.pinCode;
    document.getElementById("settingUnlockTime").value = state.config.unlockDurationSec;
    document.getElementById("settingMaxAttempts").value = state.config.maxWrongAttempts;

    updateSecModeHint(mode);
    const badge = document.getElementById("metricSecModeBadge");
    if (badge) {
        badge.textContent = `Chế độ: ${getSecModeLabelShort(mode)}`;
    }
}

function updateSecModeHint(mode) {
    const hint = document.getElementById("secModeDescription");
    if (!hint) return;
    switch (mode) {
        case 1:
            hint.textContent = "Chế độ 1 lớp: Người dùng chỉ cần 1 phương thức hợp lệ (Vân tay hoặc Thẻ RFID hoặc PIN) là cửa sẽ mở.";
            break;
        case 2:
            hint.textContent = "Chế độ 2 lớp (2FA): Cần quét Vân tay hợp lệ TRƯỚC, sau đó nhập mã PIN trên Keypad 4x4 + # để mở cửa.";
            break;
        case 3:
            hint.textContent = "Chế độ 2 lớp (2FA): Cần quẹt Thẻ RFID hợp lệ TRƯỚC, sau đó nhập mã PIN trên Keypad 4x4 + # để mở cửa.";
            break;
        case 4:
            hint.textContent = "Chế độ 2 lớp (2FA): Cần quét đồng thời cả Vân tay hợp lệ và Thẻ RFID hợp lệ để mở cửa.";
            break;
    }
}

function getSecModeLabelShort(mode) {
    switch (mode) {
        case 1: return "1 Lớp";
        case 2: return "2 Lớp (Vân tay + PIN)";
        case 3: return "2 Lớp (Thẻ + PIN)";
        case 4: return "2 Lớp (Vân tay + Thẻ)";
        default: return "1 Lớp";
    }
}

function getMethodLabelShort(method) {
    switch (method) {
        case "FINGERPRINT": return "Vân tay";
        case "RFID": return "Thẻ RFID";
        case "KEYPAD": return "Mã PIN";
        case "WEB": return "Web";
        default: return method;
    }
}

function deleteFingerprint(id) {
    state.fingerprints = state.fingerprints.filter(f => f.id !== id);
    saveLocalBackup();
    sendCommand({ action: "DELETE_FP", id });
    renderAll();
    showToast(`Đã xóa vân tay ID #${id}`);
}

function deleteRfid(uid) {
    state.rfidCards = state.rfidCards.filter(c => c.uid !== uid);
    saveLocalBackup();
    sendCommand({ action: "DELETE_RFID", uid });
    renderAll();
    showToast(`Đã xóa thẻ ${uid}`);
}

function getMethodLabel(method) {
    switch (method) {
        case "FINGERPRINT": return "Vân tay AS608";
        case "RFID": return "Thẻ RFID";
        case "KEYPAD": return "Keypad 4x4";
        case "WEB": return "Web Remote";
        default: return method;
    }
}

function formatNow() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function escapeHtml(str) {
    return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function exportLogsToCsv() {
    const headers = ["STT,Thoi Gian,Phuong Thuc,Nguoi Dung / Chi Tiet,Ket Qua"];
    const rows = state.logs.map((l, i) =>
        `${i + 1},"${l.time}","${l.method}","${l.user.replace(/"/g, '""')}","${l.valid ? 'Hop le' : 'Tu choi'}"`
    );
    const csvContent = "\uFEFF" + headers.concat(rows).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `NhatKy_CuaBaoMat_Nhom13_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Đã xuất file CSV");
}

function showToast(message) {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 2800);
}
