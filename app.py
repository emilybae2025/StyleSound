import streamlit as st
import pandas as pd
import cv2
import numpy as np
import colorsys
from collections import Counter
from PIL import Image
import os
import io
import base64
from datetime import datetime

st.set_page_config(
    page_title="StyleSound",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0d1a12;
    --surface: #132019;
    --surface2: #1a2e20;
    --border: #1f3328;
    --green: #4ade80;
    --green-dim: #22c55e;
    --green-muted: rgba(74,222,128,0.12);
    --green-border: rgba(74,222,128,0.25);
    --text: #e8f5e9;
    --muted: #6b9e7a;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(74,222,128,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 100%, rgba(212,242,82,0.05) 0%, transparent 50%),
        var(--bg) !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 780px !important; padding: 1.5rem 1.5rem 4rem !important; }

[data-testid="stTabs"] [role="tablist"] {
    background: var(--surface) !important;
    border-radius: 100px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    color: var(--muted) !important;
    border-radius: 100px !important;
    padding: 6px 20px !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--green) !important;
    color: #0d1a12 !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }
[data-testid="stImage"] img { border-radius: 12px; border: 1px solid var(--border); }
[data-testid="stSpinner"] { color: var(--green) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.logo { font-family: 'DM Serif Display', serif; font-size: 2.8rem; color: var(--text); margin: 0.5rem 0 0; line-height: 1; }
.logo span { color: var(--green); }
.tagline { font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: var(--muted); letter-spacing: 0.08em; margin: 0.4rem 0 1.5rem; }
.upload-label { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.5rem; }

.color-chip { display: inline-flex; align-items: center; gap: 10px; background: var(--surface2); border: 1px solid var(--green-border); border-radius: 100px; padding: 10px 18px 10px 12px; margin: 1rem 0 0.5rem; }
.chip-dot { width: 20px; height: 20px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.15); flex-shrink: 0; }
.chip-label { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; }
.chip-value { font-family: 'DM Serif Display', serif; font-size: 1.15rem; color: var(--text); text-transform: capitalize; }
.vibe-line { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; color: var(--green-dim); margin: 0.25rem 0 1rem; padding-left: 4px; }

.stat-row { display: flex; gap: 8px; margin: 0.75rem 0 1.25rem; }
.stat-box { flex: 1; background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 12px 10px; text-align: center; }
.stat-label { font-family: 'DM Sans', sans-serif; font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); display: block; margin-bottom: 5px; }
.stat-val { font-family: 'DM Serif Display', serif; font-size: 1.15rem; color: var(--green); }
.stat-genre { font-family: 'DM Sans', sans-serif; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--green); }

.section-label { font-family: 'DM Sans', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin: 1.75rem 0 0.75rem; display: flex; align-items: center; gap: 10px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

.track-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 18px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; position: relative; overflow: hidden; }
.track-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--green); border-radius: 3px 0 0 3px; }
.track-num { font-family: 'DM Sans', sans-serif; font-size: 0.58rem; color: var(--muted); letter-spacing: 0.1em; margin-bottom: 3px; }
.track-name { font-family: 'DM Serif Display', serif; font-size: 0.95rem; color: var(--text); margin-bottom: 2px; }
.track-artist { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; color: var(--muted); }
.track-pills { display: flex; flex-direction: column; gap: 4px; align-items: flex-end; }
.pill { font-family: 'DM Sans', monospace; font-size: 0.58rem; color: var(--green-dim); background: var(--green-muted); border: 1px solid var(--green-border); border-radius: 100px; padding: 2px 9px; white-space: nowrap; }

.history-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 16px; margin-bottom: 12px; display: flex; gap: 14px; align-items: flex-start; }
.history-thumb { width: 60px; height: 60px; border-radius: 8px; object-fit: cover; flex-shrink: 0; border: 1px solid var(--border); }
.history-date { font-family: 'DM Sans', sans-serif; font-size: 0.6rem; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }
.history-color { font-family: 'DM Serif Display', serif; font-size: 1rem; color: var(--text); text-transform: capitalize; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.h-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.history-songs { font-family: 'DM Sans', sans-serif; font-size: 0.68rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.wrapped-card { background: var(--surface2); border: 1px solid var(--green-border); border-radius: 16px; padding: 20px; margin-bottom: 12px; }
.wrapped-title { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--green); margin-bottom: 4px; }
.wrapped-sub { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; color: var(--muted); margin-bottom: 16px; }

.color-bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.color-bar-label { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; color: var(--text); text-transform: capitalize; width: 55px; flex-shrink: 0; }
.color-bar-track { flex: 1; height: 8px; background: var(--surface); border-radius: 100px; overflow: hidden; }
.color-bar-fill { height: 100%; border-radius: 100px; }
.color-bar-count { font-family: 'DM Sans', sans-serif; font-size: 0.65rem; color: var(--muted); width: 24px; text-align: right; flex-shrink: 0; }

.empty-state { border: 1.5px dashed var(--border); border-radius: 16px; padding: 52px 24px; text-align: center; margin-top: 1rem; }
.empty-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.3; }
.empty-text { font-family: 'DM Sans', sans-serif; font-size: 0.78rem; color: var(--muted); letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)


# ---- Session state ----
if "history" not in st.session_state:
    st.session_state.history = []


def save_to_history(image_pil, color, songs, genre):
    buf = io.BytesIO()
    thumb = image_pil.copy()
    thumb.thumbnail((120, 120))
    thumb.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    song_list = [{"name": s.get("track_name", ""), "artist": s.get("track_artist", "")} for _, s in songs.iterrows()]
    st.session_state.history.insert(0, {
        "date": datetime.now().strftime("%b %d, %Y  %I:%M %p"),
        "color": color,
        "genre": genre,
        "songs": song_list,
        "img_b64": img_b64,
    })


# ---- Color utils ----
COLOR_SWATCHES = {
    "red": "#e63946", "orange": "#f4a261", "yellow": "#f9c74f",
    "green": "#52b788", "blue": "#4895ef", "purple": "#9b5de5",
    "pink": "#f72585", "brown": "#8b5e3c", "black": "#3d405b",
    "white": "#e9ecef", "gray": "#8d99ae", "other": "#adb5bd",
}
COLOR_VIBE = {
    "red": "High-energy anthems", "orange": "Upbeat rap & hip-hop",
    "yellow": "Sunny pop hits", "green": "Latin rhythms",
    "blue": "Smooth R&B", "purple": "Groovy R&B", "pink": "Feel-good pop",
    "brown": "Chill rap vibes", "black": "Dark electronic",
    "white": "Clean pop sounds", "gray": "Atmospheric EDM", "other": "Eclectic mix",
}
COLOR_MUSIC_MAP = {
    "red":    {"valence": 0.8, "energy": 0.9, "genre": "rock"},
    "blue":   {"valence": 0.5, "energy": 0.4, "genre": "r&b"},
    "black":  {"valence": 0.3, "energy": 0.7, "genre": "edm"},
    "white":  {"valence": 0.7, "energy": 0.5, "genre": "pop"},
    "pink":   {"valence": 0.9, "energy": 0.6, "genre": "pop"},
    "green":  {"valence": 0.6, "energy": 0.5, "genre": "latin"},
    "purple": {"valence": 0.7, "energy": 0.8, "genre": "r&b"},
    "orange": {"valence": 0.8, "energy": 0.7, "genre": "rap"},
    "yellow": {"valence": 0.9, "energy": 0.8, "genre": "pop"},
    "gray":   {"valence": 0.4, "energy": 0.5, "genre": "edm"},
    "brown":  {"valence": 0.5, "energy": 0.4, "genre": "rap"},
    "other":  {"valence": 0.6, "energy": 0.6, "genre": "pop"},
}


def get_color_name(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = h * 360
    if v < 0.15: return "black"
    if v > 0.85 and s < 0.25: return "white"
    if s < 0.2: return "gray"
    if (h >= 0 and h < 15) or (h >= 345 and h <= 360): return "red"
    elif h >= 15 and h < 45: return "orange"
    elif h >= 45 and h < 70: return "yellow"
    elif h >= 70 and h < 165: return "green"
    elif h >= 165 and h < 250: return "blue"
    elif h >= 250 and h < 290: return "purple"
    elif h >= 290 and h < 330: return "pink"
    else: return "other"


def remove_skin_and_background(image_array):
    image_rgb = image_array
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([35, 255, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(image_hsv, lower_skin, upper_skin)
    height, width = image_array.shape[:2]
    border_size = int(min(height, width) * 0.05)
    background_mask = np.zeros((height, width), dtype=np.uint8)
    background_mask[:border_size, :] = 255
    background_mask[-border_size:, :] = 255
    background_mask[:, :border_size] = 255
    background_mask[:, -border_size:] = 255
    combined_mask = cv2.bitwise_or(skin_mask, background_mask)
    clothing_mask = cv2.bitwise_not(combined_mask)
    kernel = np.ones((5, 5), np.uint8)
    clothing_mask = cv2.morphologyEx(clothing_mask, cv2.MORPH_OPEN, kernel)
    clothing_mask = cv2.morphologyEx(clothing_mask, cv2.MORPH_CLOSE, kernel)
    clothing_only = cv2.bitwise_and(image_rgb, image_rgb, mask=clothing_mask)
    return clothing_only, clothing_mask


def color_detection(image_array):
    clothing_only, mask = remove_skin_and_background(image_array)
    colors = []
    height, width = clothing_only.shape[:2]
    for i in range(0, width, 10):
        for j in range(0, height, 10):
            if mask[j, i] > 0:
                pixel = clothing_only[j, i]
                if np.mean(pixel) > 15:
                    colors.append(get_color_name(pixel))
    if not colors:
        return "other", {}
    counts = Counter(colors)
    total = sum(counts.values())
    distribution = {color: round((count / total) * 100, 1) for color, count in counts.most_common()}
    dominant = counts.most_common(1)[0][0]
    return dominant, distribution


@st.cache_data
def load_music_data():
    import kagglehub
    import os

    try:
        # 1. This finds the folder where kagglehub just downloaded the data
        dataset_folder = kagglehub.dataset_download("joebeachcapital/30000-spotify-songs")
        
        # 2. We join that folder path with the actual filename
        csv_path = os.path.join(dataset_folder, "spotify_songs.csv")
        
        # 3. Check if the file actually exists there
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            st.error(f"Could not find spotify_songs.csv in {dataset_folder}")
            return None
    except Exception as e:
        st.error(f"Kagglehub error: {e}")
        return None


def recommend_music_by_color(color, df_music):
    params = COLOR_MUSIC_MAP.get(color, {"valence": 0.6, "energy": 0.6, "genre": "pop"})
    songs = df_music[
        (df_music["valence"] > params["valence"] - 0.1) &
        (df_music["valence"] < params["valence"] + 0.1) &
        (df_music["energy"] > params["energy"] - 0.1) &
        (df_music["energy"] < params["energy"] + 0.1)
    ].drop_duplicates(subset=["track_name"]).head(5)
    return songs, params.get("genre", "pop")


# ---- Header ----
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.25rem;">
    <div>
        <div class="logo">Style<span>Sound</span></div>
        <div class="tagline">wear it. hear it.</div>
    </div>
    <div style="font-size:2.2rem;opacity:0.4;">🎵</div>
</div>
""", unsafe_allow_html=True)

df_music = load_music_data()
if df_music is None:
    st.error("Could not load Spotify dataset. Check the CSV path in app.py.")
    st.stop()

tab_scan, tab_history, tab_wrapped = st.tabs(["Scan Outfit", "History", "StyleWrapped"])


# ================================================================
# TAB 1: SCAN
# ================================================================
with tab_scan:
    st.markdown('<div class="upload-label" style="margin-top:1.25rem;">What are you wearing?</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload outfit photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    st.markdown('<p style="font-family:\'DM Sans\',sans-serif;font-size:0.72rem;color:#6b9e7a;margin-top:0.4rem;">Works best with full-body or clothing shots</p>', unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        image_array = np.array(image)

        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.markdown('<div class="section-label" style="margin-top:1.25rem;">Your outfit</div>', unsafe_allow_html=True)
            display_img = image.copy()
            display_img.thumbnail((400, 520))
            st.image(display_img, use_column_width=True)

        with col2:
            st.markdown('<div class="section-label" style="margin-top:1.25rem;">Color analysis</div>', unsafe_allow_html=True)
            with st.spinner("Scanning outfit..."):
                detected_color, color_dist = color_detection(image_array)

            swatch = COLOR_SWATCHES.get(detected_color, "#888")
            vibe = COLOR_VIBE.get(detected_color, "Mixed sounds")
            songs, genre = recommend_music_by_color(detected_color, df_music)
            params = COLOR_MUSIC_MAP.get(detected_color, {})

            st.markdown(f"""
            <div class="color-chip">
                <div class="chip-dot" style="background:{swatch};"></div>
                <div>
                    <div class="chip-label">Detected</div>
                    <div class="chip-value">{detected_color}</div>
                </div>
            </div>
            <div class="vibe-line">&#9834; &nbsp;{vibe}</div>
            <div class="stat-row">
                <div class="stat-box">
                    <span class="stat-label">Genre</span>
                    <span class="stat-genre">{genre}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Valence</span>
                    <span class="stat-val">{params.get('valence', 0.6):.1f}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Energy</span>
                    <span class="stat-val">{params.get('energy', 0.6):.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Color distribution bars
            if color_dist:
                dist_html = '<div style="margin-top:0.5rem;">'
                dist_html += '<div style="font-family:sans-serif;font-size:0.62rem;letter-spacing:0.12em;text-transform:uppercase;color:#6b9e7a;margin-bottom:10px;">Color distribution</div>'
                for cname, pct in list(color_dist.items())[:6]:
                    cswatch = COLOR_SWATCHES.get(cname, "#888")
                    dist_html += f"""
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                        <div style="width:10px;height:10px;border-radius:50%;background:{cswatch};flex-shrink:0;"></div>
                        <div style="font-family:'DM Sans',sans-serif;font-size:0.68rem;color:#e8f5e9;text-transform:capitalize;width:52px;flex-shrink:0;">{cname}</div>
                        <div style="flex:1;height:7px;background:#132019;border-radius:100px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{cswatch};border-radius:100px;opacity:0.85;"></div>
                        </div>
                        <div style="font-family:'DM Sans',sans-serif;font-size:0.62rem;color:#6b9e7a;width:36px;text-align:right;">{pct}%</div>
                    </div>"""
                dist_html += '</div>'
                st.markdown(dist_html, unsafe_allow_html=True)

        save_to_history(image, detected_color, songs, genre)

        st.markdown('<div class="section-label">Recommended tracks</div>', unsafe_allow_html=True)

        if songs.empty:
            st.markdown('<div class="empty-state"><div class="empty-text">No tracks found. Try a different photo.</div></div>', unsafe_allow_html=True)
        else:
            cards_html = ""
            for i, (_, song) in enumerate(songs.iterrows(), 1):
                name = song.get("track_name", "Unknown")
                artist = song.get("track_artist", "Unknown")
                v = song.get("valence", 0)
                e = song.get("energy", 0)
                cards_html += f"""
                <div class="track-card">
                    <div>
                        <div class="track-num">TRACK {i:02d}</div>
                        <div class="track-name">{name}</div>
                        <div class="track-artist">{artist}</div>
                    </div>
                    <div class="track-pills">
                        <span class="pill">valence {v:.2f}</span>
                        <span class="pill">energy {e:.2f}</span>
                    </div>
                </div>"""
            st.markdown(cards_html, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state" style="margin-top:1.5rem;">
            <div class="empty-icon">👗</div>
            <div class="empty-text">Upload a photo of your outfit to get song recommendations</div>
        </div>
        """, unsafe_allow_html=True)


# ================================================================
# TAB 2: HISTORY
# ================================================================
with tab_history:
    st.markdown('<div class="section-label" style="margin-top:1.25rem;">Past outfits</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">&#128336;</div>
            <div class="empty-text">No history yet. Scan an outfit first!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for entry in st.session_state.history:
            swatch = COLOR_SWATCHES.get(entry["color"], "#888")
            song_preview = "  ·  ".join([s["name"] for s in entry["songs"][:3]])
            if len(entry["songs"]) > 3:
                song_preview += f"  +{len(entry['songs'])-3} more"
            img_html = f'<img class="history-thumb" src="data:image/png;base64,{entry["img_b64"]}" />'
            st.markdown(f"""
            <div class="history-card">
                {img_html}
                <div style="flex:1;min-width:0;">
                    <div class="history-date">{entry['date']}</div>
                    <div class="history-color">
                        <span class="h-dot" style="background:{swatch};"></span>
                        {entry['color'].capitalize()}
                        <span style="font-family:'DM Sans',sans-serif;font-size:0.75rem;color:#6b9e7a;">{entry['genre'].upper()}</span>
                    </div>
                    <div class="history-songs">{song_preview}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()


# ================================================================
# TAB 3: STYLEWRAPPED
# ================================================================
with tab_wrapped:
    st.markdown('<div class="section-label" style="margin-top:1.25rem;">Your style recap</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">&#10024;</div>
            <div class="empty-text">Scan some outfits first to see your StyleWrapped!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total = len(st.session_state.history)
        all_colors = [e["color"] for e in st.session_state.history]
        all_genres = [e["genre"] for e in st.session_state.history]
        color_counts = Counter(all_colors)
        genre_counts = Counter(all_genres)
        top_color = color_counts.most_common(1)[0][0]
        top_genre = genre_counts.most_common(1)[0][0]
        top_vibe = COLOR_VIBE.get(top_color, "Mixed sounds")

        st.markdown(f"""
        <div class="wrapped-card">
            <div class="wrapped-title">Your vibe: {top_color.capitalize()}</div>
            <div class="wrapped-sub">Based on {total} outfit{'s' if total != 1 else ''} &nbsp;&middot;&nbsp; {top_vibe}</div>
            <div class="stat-row" style="margin-bottom:0;">
                <div class="stat-box">
                    <span class="stat-label">Outfits scanned</span>
                    <span class="stat-val">{total}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Top color</span>
                    <span class="stat-genre" style="text-transform:capitalize;">{top_color}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Top genre</span>
                    <span class="stat-genre">{top_genre}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Color breakdown</div>', unsafe_allow_html=True)
        max_count = max(color_counts.values())
        bars_html = ""
        for color, count in color_counts.most_common():
            swatch = COLOR_SWATCHES.get(color, "#888")
            pct = int((count / max_count) * 100)
            bars_html += f"""
            <div class="color-bar-row">
                <div class="color-bar-label">{color}</div>
                <div class="color-bar-track">
                    <div class="color-bar-fill" style="width:{pct}%;background:{swatch};"></div>
                </div>
                <div class="color-bar-count">{count}x</div>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Genre breakdown</div>', unsafe_allow_html=True)
        genre_html = ""
        for genre, count in genre_counts.most_common():
            pct = int((count / total) * 100)
            genre_html += f"""
            <div class="color-bar-row">
                <div class="color-bar-label">{genre}</div>
                <div class="color-bar-track">
                    <div class="color-bar-fill" style="width:{pct}%;background:#4ade80;opacity:0.7;"></div>
                </div>
                <div class="color-bar-count">{count}x</div>
            </div>"""
        st.markdown(genre_html, unsafe_allow_html=True)

        all_songs = []
        seen = set()
        for entry in st.session_state.history:
            for s in entry["songs"]:
                key = s["name"] + s["artist"]
                if key not in seen:
                    seen.add(key)
                    all_songs.append(s)

        if all_songs:
            st.markdown('<div class="section-label">All recommended tracks</div>', unsafe_allow_html=True)
            songs_html = ""
            for i, s in enumerate(all_songs[:10], 1):
                songs_html += f"""
                <div class="track-card">
                    <div>
                        <div class="track-num">#{i:02d}</div>
                        <div class="track-name">{s['name']}</div>
                        <div class="track-artist">{s['artist']}</div>
                    </div>
                </div>"""
            st.markdown(songs_html, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-top:1.5rem;border-top:1px solid #1f3328;">
    <p style="font-family:'DM Sans',sans-serif;font-size:0.65rem;color:#2d4a35;letter-spacing:0.1em;">
        StyleSound &nbsp;&middot;&nbsp; by Michelle, Emily, Saanvi &nbsp;&middot;&nbsp; PM: Vili
    </p>
</div>
""", unsafe_allow_html=True)
