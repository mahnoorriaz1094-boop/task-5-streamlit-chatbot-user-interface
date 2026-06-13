# ============================================================
#   CoreTech Support Chatbot — Streamlit Web App
#   File : app.py
#   Run  : streamlit run app.py
# ============================================================

import csv
import re
import streamlit as st
from difflib import SequenceMatcher
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoreTech Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — professional dark-tech theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2e 60%, #0a1628 100%);
    color: #e2e8f0;
}

/* ── Hide default Streamlit header/footer ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #0a1628 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── Brand header ── */
.brand-header {
    background: linear-gradient(90deg, #0d1f3c, #0a2a4a);
    border-bottom: 2px solid #1d6fa4;
    padding: 1.2rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    border-radius: 12px;
}
.brand-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.brand-tagline {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 2px;
}
.brand-badge {
    margin-left: auto;
    background: #0f3460;
    color: #38bdf8;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #1d6fa4;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Chat message bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 1rem;
    gap: 0.75rem;
    align-items: flex-start;
}
.msg-row.user  { flex-direction: row-reverse; }

.avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar.bot  { background: linear-gradient(135deg, #1d6fa4, #2563eb); }
.avatar.user { background: linear-gradient(135deg, #7c3aed, #4f46e5); }

.bubble {
    max-width: 72%;
    padding: 0.85rem 1.1rem;
    border-radius: 14px;
    font-size: 0.92rem;
    line-height: 1.6;
}
.bubble.bot {
    background: #0d2240;
    border: 1px solid #1e3a5f;
    border-top-left-radius: 4px;
    color: #e2e8f0;
}
.bubble.user {
    background: linear-gradient(135deg, #1d4ed8, #4f46e5);
    border-top-right-radius: 4px;
    color: #ffffff;
}

.msg-time {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 4px;
    text-align: right;
}
.category-tag {
    display: inline-block;
    background: #0f3460;
    color: #38bdf8;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Chat input area ── */
.input-wrapper {
    background: #0d1f3c;
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
}
[data-testid="stTextInput"] input {
    background: #0a1628 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.15) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #475569 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, #1d6fa4, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Quick chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0 1rem; }
.chip {
    background: #0d2240;
    border: 1px solid #1e3a5f;
    color: #94a3b8;
    font-size: 0.78rem;
    padding: 5px 13px;
    border-radius: 20px;
    cursor: pointer;
}

/* ── Info cards in sidebar ── */
.info-card {
    background: #0d2240;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
    font-size: 0.82rem;
    color: #94a3b8;
}
.info-card strong { color: #38bdf8; display: block; margin-bottom: 4px; }

/* ── Divider ── */
hr { border-color: #1e3a5f !important; }

/* ── Scrollable chat area ── */
.chat-area {
    max-height: 480px;
    overflow-y: auto;
    padding: 1rem;
    background: #07111f;
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FAQ ENGINE  (same rule-based logic as coretech_chatbot.py)
# ─────────────────────────────────────────────────────────────

@st.cache_data
def load_faq(filepath="coretech_faq.csv"):
    faqs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["keywords"] = [k.strip().lower() for k in row["keywords"].split("|")]
            faqs.append(row)
    return faqs


def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def keyword_score(user_input, keywords):
    return sum(1 for kw in keywords if kw in user_input)


def fuzzy_score(user_input, question):
    return SequenceMatcher(None, user_input, normalize(question)).ratio()


def find_best_match(user_input, faqs, threshold=0.35):
    best, best_score = None, 0.0
    for row in faqs:
        score = keyword_score(user_input, row["keywords"]) * 2 + fuzzy_score(user_input, row["question"])
        if score > best_score:
            best_score, best = score, row
    return best if best_score >= threshold else None


FALLBACKS = [
    "I'm sorry, I didn't quite catch that. Could you rephrase?",
    "That's outside my knowledge base. Try asking about services, pricing, or support.",
    "I couldn't find a match. Please email **support@coretech.io** for further help.",
    "Hmm, not sure about that one. Try: 'What cloud services do you offer?'",
]
_fb_idx = 0

def get_fallback():
    global _fb_idx
    msg = FALLBACKS[_fb_idx % len(FALLBACKS)]
    _fb_idx += 1
    return msg, None


def get_response(user_input, faqs):
    """Returns (answer_text, category_or_None)."""
    c = normalize(user_input)

    if any(w in c for w in ["exit","quit","bye","goodbye","stop"]):
        return "Thank you for chatting with CoreTech Support. Have a great day! 👋", None

    if any(w in c for w in ["hi","hello","hey","howdy","good morning","good evening"]):
        return (
            "Hello! 👋 Welcome to **CoreTech Support**.\n\n"
            "I can answer questions about our cloud, cybersecurity, software development, "
            "pricing, DevOps, AI/ML services, and more. How can I help you today?",
            None
        )

    if any(w in c for w in ["thank","thanks","thank you","thx"]):
        return "You're welcome! 😊 Feel free to ask anything else.", None

    match = find_best_match(c, faqs)
    if match:
        return match["answer"], match["category"]

    return get_fallback()


# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "text": (
                "Hello! 👋 Welcome to **CoreTech Support**.\n\n"
                "I'm your AI assistant, ready to help with questions about our "
                "cloud infrastructure, cybersecurity, software development, pricing, "
                "DevOps, data analytics, and more.\n\n"
                "Type your question below to get started!"
            ),
            "category": None,
            "time": datetime.now().strftime("%H:%M"),
        }
    ]

if "input_key" not in st.session_state:
    st.session_state.input_key = 0


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏢 CoreTech")
    st.markdown("*Empowering businesses through innovative technology since 2010.*")
    st.markdown("---")

    st.markdown("#### 📞 Contact Information")
    st.markdown("""
<div class='info-card'><strong>📧 General Support</strong>support@coretech.io</div>
<div class='info-card'><strong>🔒 Security Incidents</strong>security@coretech.io</div>
<div class='info-card'><strong>💰 Billing</strong>billing@coretech.io</div>
<div class='info-card'><strong>🤝 Partnerships</strong>partners@coretech.io</div>
<div class='info-card'><strong>📱 Phone</strong>1-800-CORETECH</div>
<div class='info-card'><strong>🌐 Website</strong>www.coretech.io</div>
<div class='info-card'><strong>🕐 Support Hours</strong>24/7 for critical issues<br>Mon–Fri 9AM–6PM PST (standard)</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🗂️ Service Categories")
    categories = ["☁️ Cloud", "🔐 Cybersecurity", "💻 Software Dev",
                  "📊 Data & AI", "⚙️ DevOps", "💲 Pricing", "🎓 Training"]
    for cat in categories:
        st.markdown(f"- {cat}")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()


# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────────────────────

# Brand header
st.markdown("""
<div class='brand-header'>
    <div>
        <div class='brand-logo'>⚡ CoreTech</div>
        <div class='brand-tagline'>Intelligent Support Assistant</div>
    </div>
    <div class='brand-badge'>AI Powered</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    # ── Chat history ──
    chat_html = "<div class='chat-area'>"
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            cat_tag = f"<span class='category-tag'>{msg['category']}</span><br>" if msg.get("category") else ""
            # convert **bold** markdown to <strong>
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', msg["text"])
            text = text.replace("\n", "<br>")
            chat_html += f"""
            <div class='msg-row bot'>
                <div class='avatar bot'>🤖</div>
                <div>
                    <div class='bubble bot'>{cat_tag}{text}</div>
                    <div class='msg-time'>{msg.get('time','')}</div>
                </div>
            </div>"""
        else:
            chat_html += f"""
            <div class='msg-row user'>
                <div class='avatar user'>👤</div>
                <div>
                    <div class='bubble user'>{msg['text']}</div>
                    <div class='msg-time'>{msg.get('time','')}</div>
                </div>
            </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Quick suggestion chips ──
    st.markdown("<div class='chip-row'>" +
        "".join(f"<span class='chip'>💬 {q}</span>" for q in [
            "What services do you offer?",
            "Cloud pricing?",
            "Cybersecurity help",
            "Contact support",
        ]) + "</div>", unsafe_allow_html=True)

    # ── Input row ──
    st.markdown("<div class='input-wrapper'>", unsafe_allow_html=True)
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input(
            label="",
            placeholder="Ask me anything about CoreTech services...",
            key=f"chat_input_{st.session_state.input_key}",
            label_visibility="collapsed",
        )
    with btn_col:
        send = st.button("Send ➤")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Handle send ──
    if (send or user_input) and user_input.strip():
        faqs = load_faq("coretech_faq.csv")
        now  = datetime.now().strftime("%H:%M")

        st.session_state.messages.append({
            "role": "user", "text": user_input.strip(), "time": now
        })

        answer, category = get_response(user_input.strip(), faqs)
        st.session_state.messages.append({
            "role": "bot", "text": answer, "category": category, "time": now
        })

        st.session_state.input_key += 1
        st.rerun()

with col2:
    st.markdown("#### 💡 Suggested Questions")
    suggestions = [
        "What is CoreTech?",
        "Cloud migration help?",
        "Free trial available?",
        "AI/ML services?",
        "How to raise a ticket?",
        "SLA guarantee?",
        "DevOps services?",
        "Cancel subscription?",
        "Partner program?",
        "GDPR compliance?",
    ]
    faqs = load_faq("coretech_faq.csv")
    for s in suggestions:
        if st.button(s, key=f"sug_{s}"):
            now = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({"role": "user", "text": s, "time": now})
            answer, category = get_response(s, faqs)
            st.session_state.messages.append({"role": "bot", "text": answer, "category": category, "time": now})
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#334155;font-size:0.78rem;'>"
    "© 2024 CoreTech Inc. · support@coretech.io · 1-800-CORETECH · www.coretech.io"
    "</p>",
    unsafe_allow_html=True
)
