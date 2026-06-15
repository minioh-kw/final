import streamlit as st
import requests
import os

st.set_page_config(
    page_title="🎵 무드 기반 노래 추천",
    page_icon="🎵",
    layout="centered",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://back:8000")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #ffffff;
}
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #f472b6, #fb923c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #c4b5fd;
    font-size: 1rem;
    margin: 0;
}
.input-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
    backdrop-filter: blur(10px);
}
.input-card h3 {
    color: #e9d5ff;
    font-size: 1rem;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.stRadio > div {
    flex-direction: row !important;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.stRadio label {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 20px !important;
    padding: 0.4rem 1rem !important;
    color: #e9d5ff !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-size: 0.9rem !important;
}
.stRadio label:hover {
    background: rgba(167,139,250,0.2) !important;
    border-color: #a78bfa !important;
}
.stRadio label p,
.stRadio label span,
.stRadio div[role="radiogroup"] label p,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span,
[data-testid="stWidgetLabel"] p {
    color: #e9d5ff !important;
    font-size: 0.9rem !important;
}
[data-testid="stRadio"] > div > div > label {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 20px !important;
    padding: 0.4rem 1rem !important;
    color: #e9d5ff !important;
}
[data-testid="stRadio"] > div > div > label:hover {
    background: rgba(167,139,250,0.2) !important;
    border-color: #a78bfa !important;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    margin-top: 1rem !important;
    transition: opacity 0.2s ease !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}
.playlist-header {
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(219,39,119,0.4));
    border: 1px solid rgba(167,139,250,0.5);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin: 1.5rem 0 1rem;
    text-align: center;
}
.playlist-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f3e8ff;
    margin: 0 0 0.3rem;
}
.playlist-header p {
    color: #c4b5fd;
    margin: 0;
    font-size: 0.95rem;
}
.genre-badge {
    display: inline-block;
    background: rgba(167,139,250,0.25);
    border: 1px solid #a78bfa;
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    color: #e9d5ff;
    font-size: 0.82rem;
    margin-top: 0.6rem;
}
.song-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    transition: background 0.2s;
}
.song-card:hover {
    background: rgba(167,139,250,0.12);
}
.song-num {
    font-size: 1.5rem;
    min-width: 2rem;
    line-height: 1.2;
}
.song-info h4 {
    color: #f3e8ff;
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 0.15rem;
}
.song-info .artist {
    color: #a78bfa;
    font-size: 0.85rem;
    margin: 0 0 0.2rem;
}
.song-info .reason {
    color: #9ca3af;
    font-size: 0.82rem;
    margin: 0;
}
.genre-pill {
    background: rgba(251,146,60,0.15);
    border: 1px solid rgba(251,146,60,0.4);
    border-radius: 10px;
    padding: 0.15rem 0.6rem;
    font-size: 0.75rem;
    color: #fb923c;
    margin-top: 0.3rem;
    display: inline-block;
}
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: 1.5rem 0;
}
.stSelectbox label, .stRadio label span {
    color: #e9d5ff !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎵 무드 노래 추천</h1>
    <p>지금 기분을 알려주세요 — 딱 맞는 플레이리스트를 만들어드릴게요</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card"><h3>🎭 지금 기분이 어때요?</h3>', unsafe_allow_html=True)
mood = st.radio("", ["행복", "우울", "설렘", "피곤", "집중"],
                horizontal=True, key="mood", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-card"><h3>🎯 지금 뭐 하고 있어요?</h3>', unsafe_allow_html=True)
activity = st.radio("", ["공부", "운동", "드라이브", "휴식", "작업"],
                    horizontal=True, key="activity", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="input-card"><h3>⏱️ 원하는 템포</h3>', unsafe_allow_html=True)
    tempo = st.radio("", ["느림", "보통", "빠름"],
                     key="tempo", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-card"><h3>🎼 선호 장르</h3>', unsafe_allow_html=True)
    genre = st.radio("", ["K-Pop", "J-Pop", "Pop", "R&B", "인디"],
                     key="genre", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🎵 플레이리스트 추천받기"):
    with st.spinner("나만의 플레이리스트를 만드는 중..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/recommend",
                json={
                    "mood": mood,
                    "activity": activity,
                    "tempo": tempo,
                    "genre": genre,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            st.markdown(f"""
            <div class="playlist-header">
                <h2>{data['playlist_name']}</h2>
                <p>{data['description']}</p>
                <span class="genre-badge">🎼 {data['genre_tag']}</span>
            </div>
            """, unsafe_allow_html=True)

            emojis = ["🥇", "🥈", "🥉", "🎵", "🎶"]
            for i, song in enumerate(data["songs"]):
                st.markdown(f"""
                <div class="song-card">
                    <div class="song-num">{emojis[i]}</div>
                    <div class="song-info">
                        <h4>{song['title']}</h4>
                        <p class="artist">🎤 {song['artist']}</p>
                        <span class="genre-pill">{song['genre']}</span>
                        <p class="reason">💬 {song['reason']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown(
                f"<p style='text-align:center; color:#6b7280; font-size:0.8rem;'>"
                f"기분: <b style='color:#a78bfa'>{mood}</b> · "
                f"활동: <b style='color:#a78bfa'>{activity}</b> · "
                f"템포: <b style='color:#a78bfa'>{tempo}</b> · "
                f"장르: <b style='color:#a78bfa'>{genre}</b></p>",
                unsafe_allow_html=True,
            )

        except requests.exceptions.ConnectionError:
            st.error("❌ 백엔드 서버에 연결할 수 없어요. FastAPI가 실행 중인지 확인해주세요.")
        except requests.exceptions.Timeout:
            st.error("⏱️ 요청 시간이 초과되었어요. 잠시 후 다시 시도해주세요.")
        except Exception as e:
            st.error(f"❌ 오류가 발생했어요: {str(e)}")

st.markdown("""
<hr class="divider">
<p style="text-align:center; color:#4b5563; font-size:0.78rem;">
    🎵 Music Mood Recommender · Streamlit + FastAPI + Docker
</p>
""", unsafe_allow_html=True)
