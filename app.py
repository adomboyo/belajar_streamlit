# ══════════════════════════════════════════════════════════════════════════════
# NOC Bot — Asisten Engineer Jaringan
# Network Operations Center Assistant for Field Technicians & Junior Engineers
# ══════════════════════════════════════════════════════════════════════════════

import streamlit as st
from google import genai

# ── 1. Konfigurasi Halaman ───────────────────────────────────────────────────
st.set_page_config(
    page_title="NOC Bot — Asisten Engineer Jaringan",
    page_icon="🛜",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── 2. Custom CSS — Dark Network Operations Theme ────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ──────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    /* ── Root Variables ──────────────────────────────────────────────────── */
    :root {
        --noc-bg: #0a0e17;
        --noc-surface: #111827;
        --noc-surface-2: #1a2332;
        --noc-border: #1e3a5f;
        --noc-accent: #00d4aa;
        --noc-accent-dim: #00a88a;
        --noc-accent-glow: rgba(0, 212, 170, 0.15);
        --noc-blue: #3b82f6;
        --noc-yellow: #fbbf24;
        --noc-red: #ef4444;
        --noc-text: #e2e8f0;
        --noc-text-dim: #94a3b8;
        --noc-mono: 'JetBrains Mono', monospace;
        --noc-sans: 'Inter', sans-serif;
    }

    /* ── Global Styles ───────────────────────────────────────────────────── */
    .stApp {
        background: linear-gradient(165deg, #0a0e17 0%, #0f172a 40%, #0c1929 100%) !important;
        font-family: var(--noc-sans) !important;
    }

    /* ── Header Banner ───────────────────────────────────────────────────── */
    .noc-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        border: 1px solid var(--noc-border);
        border-radius: 16px;
        padding: 2rem 2rem 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .noc-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--noc-accent), var(--noc-blue), var(--noc-accent));
        background-size: 200% 100%;
        animation: scanline 3s linear infinite;
    }
    @keyframes scanline {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    .noc-header h1 {
        font-family: var(--noc-sans) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        margin: 0 0 0.25rem 0 !important;
        letter-spacing: -0.02em;
    }
    .noc-header .noc-subtitle {
        color: var(--noc-accent);
        font-family: var(--noc-mono);
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0;
    }
    .noc-header .noc-desc {
        color: var(--noc-text-dim);
        font-size: 0.85rem;
        margin-top: 0.75rem;
        line-height: 1.5;
    }

    /* ── Status Indicator ────────────────────────────────────────────────── */
    .noc-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: var(--noc-mono);
        font-size: 0.72rem;
        color: var(--noc-accent);
        margin-top: 0.75rem;
        padding: 4px 10px;
        background: var(--noc-accent-glow);
        border-radius: 20px;
        border: 1px solid rgba(0, 212, 170, 0.2);
    }
    .noc-status .pulse {
        width: 7px; height: 7px;
        background: var(--noc-accent);
        border-radius: 50%;
        animation: pulse-anim 2s ease-in-out infinite;
    }
    @keyframes pulse-anim {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0, 212, 170, 0.4); }
        50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(0, 212, 170, 0); }
    }

    /* ── Sidebar Styles ──────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%) !important;
        border-right: 1px solid var(--noc-border) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: var(--noc-sans) !important;
        color: var(--noc-text) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ── Quick Action Buttons ────────────────────────────────────────────── */
    .noc-actions {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin: 0.5rem 0 1rem;
    }
    .noc-action-btn {
        background: var(--noc-surface-2);
        border: 1px solid var(--noc-border);
        border-radius: 8px;
        padding: 10px 14px;
        color: var(--noc-text);
        font-family: var(--noc-sans);
        font-size: 0.82rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .noc-action-btn:hover {
        background: var(--noc-accent-glow);
        border-color: var(--noc-accent-dim);
        color: var(--noc-accent);
        transform: translateX(3px);
    }

    /* ── Chat Messages ───────────────────────────────────────────────────── */
    .stChatMessage {
        background: var(--noc-surface) !important;
        border: 1px solid var(--noc-border) !important;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, var(--noc-accent), var(--noc-blue)) !important;
    }

    /* ── Chat Input ──────────────────────────────────────────────────────── */
    .stChatInput {
        border-color: var(--noc-border) !important;
    }
    .stChatInput > div {
        background: var(--noc-surface) !important;
        border: 1px solid var(--noc-border) !important;
        border-radius: 12px !important;
    }
    .stChatInput textarea {
        font-family: var(--noc-sans) !important;
        color: var(--noc-text) !important;
    }

    /* ── Sidebar Divider ─────────────────────────────────────────────────── */
    .sidebar-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--noc-border), transparent);
        margin: 1rem 0;
    }

    /* ── Info/Warning boxes ───────────────────────────────────────────────── */
    .stAlert {
        border-radius: 10px !important;
        font-family: var(--noc-sans) !important;
    }

    /* ── Streamlit Button Overrides ───────────────────────────────────────── */
    .stButton > button {
        font-family: var(--noc-sans) !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        transition: all 0.2s ease !important;
    }
</style>
""", unsafe_allow_html=True)


# ── 3. Header Banner ────────────────────────────────────────────────────────
st.markdown("""
<div class="noc-header">
    <h1>🛜 NOC Bot</h1>
    <p class="noc-subtitle">Network Operations Center Assistant</p>
    <p class="noc-desc">
        Asisten AI untuk engineer jaringan — troubleshoot masalah koneksi,
        perintah konfigurasi MikroTik & OLT, serta analisis status monitoring.
    </p>
    <div class="noc-status">
        <span class="pulse"></span>
        SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# ── 4. System Prompt Builder ────────────────────────────────────────────────
def build_system_prompt(gaya: str, domain: str) -> str:
    """Membangun system prompt berdasarkan parameter kreatif user."""

    # Base personality
    prompt = """Kamu adalah NOC Bot — asisten AI khusus untuk Network Operations Center.
Kamu membantu engineer jaringan (teknisi lapangan dan engineer junior) dalam:
1. Troubleshoot masalah jaringan (konektivitas, latency, packet loss, dll)
2. Memberikan perintah konfigurasi router dan switch
3. Menganalisis status dari sistem monitoring jaringan
4. Menjelaskan konsep networking yang kompleks

ATURAN PENTING:
- Selalu berikan jawaban yang TERSTRUKTUR dan TO-THE-POINT
- Gunakan format bullet points, numbered steps, atau tabel saat menjelaskan prosedur
- Saat memberikan perintah CLI, SELALU gunakan code block dengan syntax highlighting
- Jika ada perintah yang berisiko (bisa memutus koneksi), beri peringatan ⚠️
- Sertakan penjelasan singkat untuk setiap perintah yang kamu berikan
- Jika user bertanya di luar topik jaringan, arahkan kembali ke topik networking
"""

    # Gaya bahasa
    if gaya == "Formal & Teknis":
        prompt += """
GAYA BAHASA: Formal dan teknis. Gunakan istilah-istilah jaringan standar.
Jawab seperti senior engineer yang sedang membimbing junior engineer.
Gunakan bahasa Indonesia baku dengan istilah teknis dalam bahasa Inggris."""
    elif gaya == "Santai & Friendly":
        prompt += """
GAYA BAHASA: Santai tapi tetap akurat. Gunakan bahasa sehari-hari.
Bisa pakai "lo/gue" atau "kamu/aku". Tetap profesional dalam konten teknis.
Sisipkan emoji yang relevan untuk membuat penjelasan lebih engaging."""
    else:  # Militer / NOC Style
        prompt += """
GAYA BAHASA: Tegas, ringkas, seperti komunikasi radio di NOC.
Gunakan format laporan: STATUS, DIAGNOSIS, ACTION, RESULT.
Singkat dan efisien. Setiap kata harus bermakna. Tidak ada basa-basi."""

    # Domain fokus
    if domain == "MikroTik RouterOS":
        prompt += """
DOMAIN FOKUS: MikroTik RouterOS.
Prioritaskan perintah dan konfigurasi MikroTik. Kamu menguasai:
- RouterOS CLI (/ip, /interface, /routing, /system, /queue, dll)
- Winbox dan WebFig
- Firewall filter, NAT, mangle
- Routing (OSPF, BGP, static)
- Queue management (simple queue, queue tree, HTB)
- Hotspot, PPPoE, DHCP
- VLAN, bridge, bonding
- Tools: torch, packet sniffer, bandwidth test, ping, traceroute"""

    elif domain == "OLT & GPON":
        prompt += """
DOMAIN FOKUS: OLT (Optical Line Terminal) dan jaringan GPON/FTTH.
Prioritaskan manajemen perangkat OLT. Kamu menguasai:
- Manajemen ONU/ONT (register, deregister, status check)
- GPON port management dan optical power monitoring
- Service profile, line profile, DBA profile
- VLAN management pada OLT
- Troubleshoot optical signal (Rx/Tx power, ORL, optical loss)
- Vendor-specific: Huawei (MA5608T/MA5800), ZTE (C320/C300), FiberHome
- Splitter ratio calculation dan link budget"""

    elif domain == "Monitoring & NOC":
        prompt += """
DOMAIN FOKUS: Network Monitoring dan operasional NOC.
Prioritaskan analisis monitoring dan SOP NOC. Kamu menguasai:
- SNMP monitoring (OID, traps, polling)
- Tools: Zabbix, PRTG, Cacti, Nagios, Grafana, LibreNMS
- Syslog analysis dan log correlation
- SLA monitoring dan uptime calculation
- Incident management dan eskalasi
- Bandwidth utilization analysis
- Alert triage dan severity classification
- Network topology mapping"""

    else:  # General Networking
        prompt += """
DOMAIN FOKUS: General Networking.
Kamu menguasai semua aspek jaringan:
- OSI Layer dan TCP/IP model
- Routing protocols (OSPF, BGP, EIGRP, static)
- Switching (VLAN, STP, LACP, port security)
- Firewall dan security (ACL, NAT, VPN, IPSec)
- Wireless networking (802.11, channel planning, roaming)
- DNS, DHCP, HTTP/S, SSH, Telnet
- Fiber optic dan copper cabling
- QoS dan traffic management"""

    return prompt


# ── 5. Sidebar — Pengaturan & Parameter Kreatif ─────────────────────────────
with st.sidebar:
    # API Key section
    st.markdown("### 🔑 API Key")
    google_api_key = st.text_input(
        "Google AI API Key",
        type="password",
        help="Dapatkan API key gratis di aistudio.google.com"
    )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Model selection
    st.markdown("### ⚙️ Konfigurasi Model")
    model_choice = st.selectbox(
        "Model AI",
        ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"],
        index=0,
        help="Pilih model Gemini yang digunakan"
    )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Creative parameters
    st.markdown("### 🎛️ Parameter Kreatif")

    gaya_bahasa = st.selectbox(
        "Gaya Bahasa",
        ["Formal & Teknis", "Santai & Friendly", "NOC Style (Ringkas)"],
        index=0,
        help="Atur gaya komunikasi NOC Bot"
    )

    domain_fokus = st.selectbox(
        "Domain Fokus",
        ["General Networking", "MikroTik RouterOS", "OLT & GPON", "Monitoring & NOC"],
        index=0,
        help="Fokuskan keahlian bot pada domain tertentu"
    )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")

    quick_actions = {
        "🔍 Troubleshoot Koneksi": "Bantu saya troubleshoot masalah koneksi internet yang lambat. Berikan langkah-langkah diagnostik dari awal secara sistematis.",
        "📋 Perintah MikroTik": "Berikan daftar perintah MikroTik RouterOS yang paling sering digunakan untuk monitoring dan troubleshooting, lengkap dengan penjelasan singkat.",
        "🔌 Analisis Port OLT": "Bagaimana cara mengecek status port OLT dan ONU yang terdaftar? Berikan perintah dan cara membaca output-nya.",
        "📊 Cek Status Jaringan": "Berikan template checklist untuk health check jaringan harian yang bisa digunakan oleh teknisi NOC.",
        "🛡️ Konfigurasi Firewall": "Berikan contoh konfigurasi firewall dasar untuk MikroTik yang aman untuk jaringan kecil-menengah.",
        "📡 Hitung Link Budget": "Bantu saya menghitung link budget untuk jaringan FTTH/GPON. Jelaskan parameter yang perlu diperhatikan.",
    }

    # Use session state to track quick action clicks
    if "quick_action_prompt" not in st.session_state:
        st.session_state.quick_action_prompt = None

    for label, prompt_text in quick_actions.items():
        if st.button(label, use_container_width=True):
            st.session_state.quick_action_prompt = prompt_text

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Reset button
    reset_button = st.button(
        "🔄 Reset Percakapan",
        help="Hapus semua pesan dan mulai dari awal",
        use_container_width=True,
    )

    # Footer
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#475569; font-size:0.72rem; font-family:var(--noc-mono);'>"
        "NOC Bot v1.0 — Final Project<br>Hacktiv8 Data Scientist</p>",
        unsafe_allow_html=True,
    )


# ── 6. Validasi API Key ────────────────────────────────────────────────────
if not google_api_key:
    st.info("🗝️ Masukkan **Google AI API Key** di sidebar untuk mulai chat.")
    st.markdown("""
    <div style="background: #111827; border: 1px solid #1e3a5f; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 0.75rem 0;">
            <strong style="color: #e2e8f0;">Cara mendapatkan API Key:</strong>
        </p>
        <ol style="color: #94a3b8; font-size: 0.82rem; margin: 0; padding-left: 1.25rem; line-height: 1.8;">
            <li>Buka <a href="https://aistudio.google.com" target="_blank" style="color: #00d4aa;">aistudio.google.com</a></li>
            <li>Klik <strong style="color: #e2e8f0;">Get API Key</strong> → <strong style="color: #e2e8f0;">Create API Key</strong></li>
            <li>Copy key dan paste di sidebar</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── 7. Inisialisasi Gemini Client ────────────────────────────────────────────
if ("genai_client" not in st.session_state) or (
    getattr(st.session_state, "_last_key", None) != google_api_key
):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        # Key berganti → hapus session lama
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"❌ API Key tidak valid: {e}")
        st.stop()


# ── 8. Inisialisasi / Re-inisialisasi Chat Session ──────────────────────────
# Deteksi perubahan parameter kreatif → buat ulang chat session
current_config = f"{model_choice}|{gaya_bahasa}|{domain_fokus}"

if ("chat" not in st.session_state) or (
    getattr(st.session_state, "_last_config", None) != current_config
):
    system_prompt = build_system_prompt(gaya_bahasa, domain_fokus)
    st.session_state.chat = st.session_state.genai_client.chats.create(
        model=model_choice,
        config={"system_instruction": system_prompt},
    )
    st.session_state._last_config = current_config

    # Hanya reset messages kalau config benar-benar berubah DAN sudah ada pesan
    if "messages" in st.session_state and st.session_state.messages:
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ── 9. Tombol Reset ──────────────────────────────────────────────────────────
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.session_state.pop("_last_config", None)
    st.session_state.pop("quick_action_prompt", None)
    st.rerun()


# ── 10. Tampilkan Riwayat Percakapan ─────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── 11. Handle Quick Actions ────────────────────────────────────────────────
# Jika ada quick action yang diklik, inject sebagai prompt
incoming_prompt = None

if st.session_state.quick_action_prompt:
    incoming_prompt = st.session_state.quick_action_prompt
    st.session_state.quick_action_prompt = None  # consume it


# ── 12. Chat Input & Response ────────────────────────────────────────────────
user_input = st.chat_input("Ketik pertanyaan jaringan kamu di sini...")

# Prioritaskan quick action, lalu manual input
prompt = incoming_prompt or user_input

if prompt:
    # Tambah pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Tampilkan bubble user
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim ke Gemini dan tampilkan respons
    with st.chat_message("assistant"):
        with st.spinner("⏳ Menganalisis..."):
            try:
                response = st.session_state.chat.send_message(prompt)

                if hasattr(response, "text"):
                    answer = response.text
                else:
                    answer = str(response)

            except Exception as e:
                answer = f"⚠️ **Error:** {e}\n\nCoba cek koneksi internet atau validitas API key kamu."

        st.markdown(answer)

    # Simpan respons ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": answer})
