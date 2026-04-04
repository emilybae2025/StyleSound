import streamlit as st
import pandas as pd
import cv2
import numpy as np
import colorsys
from collections import Counter
from PIL import Image
import os
import io

# Page Config 
st.set_page_config(
    page_title="CHROMABEATS",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --border: #1e1e2e;
    --accent: #c8f25c;
    --accent2: #ff6b6b;
    --text: #f0f0f5;
    --muted: #6b6b8a;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 20% 20%, rgba(200, 242, 92, 0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(255, 107, 107, 0.04) 0%, transparent 60%),
        var(--bg) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main content width */
.block-container {
    max-width: 720px !important;
    padding: 2rem 1.5rem !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
}

p, div, span, label {
    font-family: 'Space Mono', monospace !important;
}

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0;
}

.hero-title span {
    color: var(--accent);
    font-family: 'Syne', sans-serif;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.75rem;
    margin-bottom: 0;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
    margin: 2rem 0;
    opacity: 0.4;
}

/* Upload zone */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
}

/* Image display */
[data-testid="stImage"] img {
    border-radius: 2px;
    border: 1px solid var(--border);
}

/* Color badge */
.color-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 12px 20px;
    margin: 1.5rem 0 0.5rem;
}

.color-swatch {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
    flex-shrink: 0;
}

.color-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
}

.color-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    text-transform: capitalize;
}

/* Section header */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Song card */
.song-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 16px 20px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: border-color 0.15s;
    position: relative;
    overflow: hidden;
}

.song-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--accent);
}

.song-info {}

.song-number {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}

.song-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 2px;
}

.song-artist {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
}

.song-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
}

.stat-pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    color: var(--muted);
    background: rgba(200, 242, 92, 0.06);
    border: 1px solid rgba(200, 242, 92, 0.12);
    border-radius: 1px;
    padding: 2px 8px;
}

/* Genre tag */
.genre-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(200, 242, 92, 0.08);
    border: 1px solid rgba(200, 242, 92, 0.2);
    border-radius: 1px;
    padding: 3px 10px;
    margin-left: 8px;
    vertical-align: middle;
}

/* Upload instruction */
.upload-hint {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
}

/* Spinner / loading */
[data-testid="stSpinner"] {
    color: var(--accent) !important;
}

/* Metric / info boxes */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 1rem 0;
}

.info-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 14px 16px;
    text-align: center;
}

.info-box-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    display: block;
    margin-bottom: 6px;
}

.info-box-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--accent);
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); }
</style>
""", unsafe_allow_html=True)


# Color Utilities 
COLOR_SWATCHES = {
    'red':    '#e63946',
    'orange': '#f4a261',
    'yellow': '#f9c74f',
    'green':  '#52b788',
    'blue':   '#4895ef',
    'purple': '#9b5de5',
    'pink':   '#f72585',
    'brown':  '#8b5e3c',
    'black':  '#1a1a2e',
    'white':  '#f8f9fa',
    'gray':   '#8d99ae',
    'other':  '#adb5bd',
}

COLOR_VIBE = {
    'red':    'High-energy anthems',
    'orange': 'Upbeat rap & hip-hop',
    'yellow': 'Sunny pop hits',
    'green':  'Latin rhythms',
    'blue':   'Smooth R&B',
    'purple': 'Groovy R&B',
    'pink':   'Feel-good pop',
    'brown':  'Chill rap vibes',
    'black':  'Dark electronic',
    'white':  'Clean pop sounds',
    'gray':   'Atmospheric EDM',
    'other':  'Eclectic mix',
}


def get_color_name(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = h * 360
    if v < 0.15:
        return "black"
    if v > 0.85 and s < 0.25:
        return "white"
    if s < 0.2:
        return "gray"
    if (h >= 0 and h < 15) or (h >= 345 and h <= 360):
        return "red"
    elif h >= 15 and h < 45:
        return "orange"
    elif h >= 45 and h < 70:
        return "yellow"
    elif h >= 70 and h < 165:
        return "green"
    elif h >= 165 and h < 250:
        return "blue"
    elif h >= 250 and h < 290:
        return "purple"
    elif h >= 290 and h < 330:
        return "pink"
    else:
        return "other"


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
        return "other"
    return Counter(colors).most_common(1)[0][0]


# Music Data 
@st.cache_data
def load_music_data():
    path = r"C:\Users\saanv\.cache\kagglehub\datasets\joebeachcapital\30000-spotify-songs\versions\2\spotify_songs.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


COLOR_MUSIC_MAP = {
    'red':    {'valence': 0.8, 'energy': 0.9, 'genre': 'rock'},
    'blue':   {'valence': 0.5, 'energy': 0.4, 'genre': 'r&b'},
    'black':  {'valence': 0.3, 'energy': 0.7, 'genre': 'edm'},
    'white':  {'valence': 0.7, 'energy': 0.5, 'genre': 'pop'},
    'pink':   {'valence': 0.9, 'energy': 0.6, 'genre': 'pop'},
    'green':  {'valence': 0.6, 'energy': 0.5, 'genre': 'latin'},
    'purple': {'valence': 0.7, 'energy': 0.8, 'genre': 'r&b'},
    'orange': {'valence': 0.8, 'energy': 0.7, 'genre': 'rap'},
    'yellow': {'valence': 0.9, 'energy': 0.8, 'genre': 'pop'},
    'gray':   {'valence': 0.4, 'energy': 0.5, 'genre': 'edm'},
    'brown':  {'valence': 0.5, 'energy': 0.4, 'genre': 'rap'},
    'other':  {'valence': 0.6, 'energy': 0.6, 'genre': 'pop'},
}


def recommend_music_by_color(color, df_music):
    params = COLOR_MUSIC_MAP.get(color, {'valence': 0.6, 'energy': 0.6, 'genre': 'pop'})
    songs = df_music[
        (df_music['valence'] > params['valence'] - 0.1) &
        (df_music['valence'] < params['valence'] + 0.1) &
        (df_music['energy'] > params['energy'] - 0.1) &
        (df_music['energy'] < params['energy'] + 0.1)
    ].drop_duplicates(subset=['track_name']).head(5)
    return songs, params.get('genre', 'pop')


# App Layout 

# Header
st.markdown("""
<div>
    <p class="hero-sub">Color-driven music discovery</p>
    <h1 class="hero-title">CHROMA<span>BEATS</span></h1>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Load data
df_music = load_music_data()

if df_music is None:
    st.markdown("""
    <div style="background:#1a0a0a;border:1px solid #3a1515;border-radius:2px;padding:16px 20px;margin:1rem 0;">
        <p style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#ff6b6b;margin:0;">
            ⚠ &nbsp; Could not load Spotify dataset. Place <code>spotify_songs.csv</code> 
            in the same folder as this script, or run from Colab with kagglehub.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Upload section
st.markdown('<div class="section-header">Upload outfit</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your photo here",
    type=['jpg', 'jpeg', 'png'],
    label_visibility="collapsed",
)

st.markdown('<p class="upload-hint">→ Works best with full-body or clothing shots on a plain background</p>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown('<div class="section-header">Your outfit</div>', unsafe_allow_html=True)
        # Resize for display
        display_img = image.copy()
        display_img.thumbnail((400, 500))
        st.image(display_img, use_column_width=True)

    with col2:
        st.markdown('<div class="section-header">Analysis</div>', unsafe_allow_html=True)

        with st.spinner("Analyzing colors..."):
            detected_color = color_detection(image_array)

        swatch = COLOR_SWATCHES.get(detected_color, '#888')
        vibe = COLOR_VIBE.get(detected_color, 'Mixed sounds')

        st.markdown(f"""
        <div class="color-badge">
            <div class="color-swatch" style="background:{swatch};"></div>
            <div>
                <div class="color-label">Dominant color</div>
                <div class="color-value">{detected_color}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Get recommendations to show genre
        songs, genre = recommend_music_by_color(detected_color, df_music)

        st.markdown(f"""
        <div class="info-grid">
            <div class="info-box">
                <span class="info-box-label">Genre</span>
                <span class="info-box-value" style="font-size:0.85rem;text-transform:uppercase;">{genre}</span>
            </div>
            <div class="info-box">
                <span class="info-box-label">Valence</span>
                <span class="info-box-value">{COLOR_MUSIC_MAP.get(detected_color,{}).get('valence',0.6):.1f}</span>
            </div>
            <div class="info-box">
                <span class="info-box-label">Energy</span>
                <span class="info-box-value">{COLOR_MUSIC_MAP.get(detected_color,{}).get('energy',0.6):.1f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#6b6b8a;margin-top:0.5rem;">
            ↳ {vibe}
        </p>
        """, unsafe_allow_html=True)

    # Song recommendations
    st.markdown('<div class="section-header" style="margin-top:2rem;">Recommended tracks</div>', unsafe_allow_html=True)

    if songs.empty:
        st.markdown("""
        <div style="background:var(--surface,#12121a);border:1px solid #1e1e2e;padding:16px 20px;border-radius:2px;">
            <p style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#6b6b8a;margin:0;">
                No tracks found for this color profile. Try a different image.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cards_html = ""
        for i, (_, song) in enumerate(songs.iterrows(), 1):
            name = song.get('track_name', 'Unknown')
            artist = song.get('track_artist', 'Unknown')
            valence = song.get('valence', 0)
            energy = song.get('energy', 0)
            cards_html += f"""
            <div class="song-card">
                <div class="song-info">
                    <div class="song-number">Track {i:02d}</div>
                    <div class="song-name">{name}</div>
                    <div class="song-artist">{artist}</div>
                </div>
                <div class="song-stats">
                    <span class="stat-pill">V {valence:.2f}</span>
                    <span class="stat-pill">E {energy:.2f}</span>
                </div>
            </div>
            """
        st.markdown(cards_html, unsafe_allow_html=True)

    # Footer note
    st.markdown("""
    <div class="divider" style="margin-top:2.5rem;"></div>
    <p style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-align:center;letter-spacing:0.1em;">
        CHROMABEATS — outfit color × music mood
    </p>
    """, unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div style="
        border: 1px dashed #1e1e2e;
        border-radius: 2px;
        padding: 48px 24px;
        text-align: center;
        margin-top: 1rem;
    ">
        <p style="font-family:'Syne',sans-serif;font-size:2rem;margin:0 0 8px;opacity:0.15;">🎨</p>
        <p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a5a;letter-spacing:0.1em;margin:0;">
            UPLOAD AN OUTFIT TO BEGIN
        </p>
    </div>
    """, unsafe_allow_html=True)
