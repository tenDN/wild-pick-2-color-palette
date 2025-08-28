import streamlit as st
import numpy as np
from PIL import Image
import io
import json
from typing import List, Tuple, Dict
from sklearn.cluster import KMeans
import colorsys
from datetime import datetime

# Optional libraries
try:
    from colorthief import ColorThief
    COLORTHIEF_AVAILABLE = True
except ImportError:
    COLORTHIEF_AVAILABLE = False

# Set page config
st.set_page_config(
    page_title="Wild Pick 2.0 - Brand Guidelines Color Palette",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Brand Guidelines CSS - Minimal, Clean Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway+Dots&family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300&display=swap');
    
    /* Reset and base styles */
    .stApp {
        background-color: #faf9f7;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        background-color: #faf9f7;
        padding: 10px 3rem 2rem 3rem !important;
        max-width: 100%;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main title */
    .brand-title {
        font-family: 'Raleway Dots', cursive !important;
        font-size: 6rem !important;
        color: #1a1a1a !important;
        text-align: center;
        margin: 0 0 0.5rem 0 !important;
        font-weight: 400 !important;
        letter-spacing: normal;
    }
    
    .brand-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-top: -60px;
        margin-bottom: 3rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.5rem !important;
        color: #1a1a1a !important;
        margin: 3rem 0 2rem 0 !important;
        font-weight: 500 !important;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -0.5rem;
        left: 0;
        width: 3rem;
        height: 1px;
        background-color: #d0d0d0;
    }
    
    /* Color grid - Large circular swatches */
    .color-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 3rem;
        margin: 3rem 0;
        padding: 2rem 0;
    }
    
    .color-swatch-container {
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s ease;
        margin-bottom: 3rem;
        padding-bottom: 2rem;
    }
    
    .color-swatch-container:hover {
        transform: translateY(-4px);
    }
    
    .color-swatch {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: none;
        transition: box-shadow 0.3s ease;
        position: relative;
    }
    
    .color-swatch:hover {
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    }
    
    .color-swatch.selected {
        box-shadow: 0 0 0 4px #007acc;
    }
    
    .color-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .color-values {
        font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        font-size: 0.9rem;
        color: #666;
        line-height: 1.6;
    }
    
    /* Tints strip */
    .tints-strip {
        display: flex;
        justify-content: center;
        gap: 0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        border-radius: 0;
        overflow: hidden;
    }
    
    .tint-swatch {
        width: 60px;
        height: 250px;
        border: none;
        position: relative;
        cursor: pointer;
        flex: 1;
    }
    
    .tint-label {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        white-space: nowrap;
    }
    
    /* Harmony playground */
    .harmony-tray {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
        display: none;
    }
    
    .harmony-tray.expanded {
        display: block;
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .harmony-group {
        margin-bottom: 2rem;
    }
    
    .harmony-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .harmony-colors {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .harmony-mini {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        position: relative;
    }
    
    .harmony-hex {
        font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        font-size: 0.8rem;
        color: #666;
        margin-left: 0.5rem;
    }
    
    /* Upload area */
    .upload-section {
        background: white;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        border: 2px dashed #d0d0d0;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #007acc;
        background: #f8fafe;
    }
    
    /* Buttons */
    .extract-button {
        background: #1a1a1a;
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 2rem 0;
    }
    
    .extract-button:hover {
        background: #333;
        transform: translateY(-1px);
    }
    
    .export-button {
        background: #007acc;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 1rem 0;
    }
    
    .export-button:hover {
        background: #0066aa;
    }
    
    /* Dividers */
    .section-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #d0d0d0, transparent);
        margin: 4rem 0;
    }
    
    /* Responsive - Mobile Optimized */
    @media (max-width: 768px) {
        .color-grid {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 3rem;
        }
        
        .brand-title {
            font-size: 3rem !important;
            margin-bottom: 1rem !important;
            margin-top: 0.5rem !important;
            white-space: nowrap !important;
        }
        
        .brand-subtitle {
            font-size: 1.1rem !important;
            margin-bottom: 3rem !important;
            margin-top: -20px !important;
        }
        
        .section-header {
            font-size: 2rem !important;
            margin: 3rem 0 2rem 0 !important;
        }
        
        .color-swatch {
            width: 160px !important;
            height: 160px !important;
            margin: 0 auto 2rem auto !important;
        }
        
        .color-name {
            font-size: 1.6rem !important;
            margin-bottom: 1rem !important;
        }
        
        .color-values {
            font-size: 1.2rem !important;
            line-height: 1.8 !important;
        }
        
        .tints-strip {
            margin: 1.5rem 0 !important;
        }
        
        .tint-swatch {
            width: 80px !important;
            height: 300px !important;
        }
        
        .tint-label {
            font-size: 1rem !important;
            bottom: 12px !important;
        }
        
        .harmony-mini {
            width: 70px !important;
            height: 70px !important;
        }
        
        .harmony-hex {
            font-size: 1rem !important;
        }
        
        .harmony-title {
            font-size: 1.4rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .main .block-container {
            padding: 0.5rem 1rem 2rem 1rem !important;
        }
        
        /* Make buttons bigger on mobile */
        .stButton > button {
            font-size: 1.2rem !important;
            padding: 1rem 2rem !important;
            min-height: 3rem !important;
        }
        
        /* Bigger file uploader on mobile */
        .stFileUploader {
            font-size: 1.1rem !important;
        }
        
        .stFileUploader label {
            font-size: 1.3rem !important;
        }
        
        .stFileUploader > div {
            padding: 3rem 1rem !important;
        }
        
        /* Bigger slider on mobile */
        .stSlider label {
            font-size: 1.3rem !important;
        }
    }
    
    /* Form styling */
    .stSelectbox > div > div {
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        background: white;
    }
    
    /* Simple slider styling */
    .stSlider {
        text-align: center;
    }
    
    .stSlider > div {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .stSlider label {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        color: #333 !important;
    }
    
    .stFileUploader {
        background: transparent;
    }
    
    .stFileUploader > div {
        border: 2px dashed #007acc !important;
        background: #f8fafe !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #0066aa !important;
        background: #f0f7ff !important;
    }
    
    .stFileUploader label {
        font-weight: 500 !important;
        color: #007acc !important;
        font-size: 1.1rem !important;
    }
    
    .stFileUploader button {
        border-radius: 0 !important;
    }
    
    /* Make the X button 2X larger */
    .stFileUploader button[title="Remove file"] {
        font-size: 2rem !important;
        width: 2rem !important;
        height: 2rem !important;
        border-radius: 0 !important;
    }
    
    .stFileUploader button[title="Remove file"] svg {
        width: 1.5rem !important;
        height: 1.5rem !important;
    }
    
    /* Button styling - square corners */
    .stButton > button {
        border-radius: 0 !important;
        border: 1px solid #d0d0d0 !important;
        background: white !important;
        color: #333 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        border-color: #d65745 !important;
        background: #faf8f7 !important;
    }
    
    .stButton > button:focus {
        border-color: #d65745 !important;
        box-shadow: 0 0 0 2px rgba(214, 87, 69, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Color math and helper functions
def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_rgb(hex_color):
    """Convert hex string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_cmyk(r, g, b):
    """Convert RGB values to CMYK"""
    if r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 100
    
    # Normalize RGB values to 0-1 range
    r_norm = r / 255.0
    g_norm = g / 255.0 
    b_norm = b / 255.0
    
    # Calculate K (black)
    k = 1 - max(r_norm, g_norm, b_norm)
    
    # Calculate CMY
    c = (1 - r_norm - k) / (1 - k) if (1 - k) != 0 else 0
    m = (1 - g_norm - k) / (1 - k) if (1 - k) != 0 else 0
    y = (1 - b_norm - k) / (1 - k) if (1 - k) != 0 else 0
    
    # Convert to percentages
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def get_color_name(rgb):
    """Get approximate color name based on RGB values"""
    r, g, b = rgb
    
    # Convert to HSV for better color classification
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h *= 360
    s *= 100
    v *= 100
    
    if v < 20:
        return "Black"
    elif v > 80 and s < 20:
        return "White"
    elif s < 20:
        return "Gray"
    elif h < 15 or h > 345:
        return "Red"
    elif h < 45:
        return "Orange"
    elif h < 75:
        return "Yellow"
    elif h < 150:
        return "Green"
    elif h < 210:
        return "Cyan"
    elif h < 270:
        return "Blue"
    elif h < 330:
        return "Purple"
    else:
        return "Pink"

def create_tint(rgb, percentage):
    """Create a tint (lighter version) of a color"""
    r, g, b = rgb
    # Mix with white
    factor = percentage / 100
    new_r = r + (255 - r) * (1 - factor)
    new_g = g + (255 - g) * (1 - factor)
    new_b = b + (255 - b) * (1 - factor)
    return (int(new_r), int(new_g), int(new_b))

def create_color_harmony(base_color, harmony_type="complementary"):
    """Generate color harmony based on a base color"""
    r, g, b = base_color
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    
    harmonies = []
    
    if harmony_type == "complementary":
        # Complementary color (180 degrees opposite)
        comp_h = (h + 0.5) % 1.0
        comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_h, s, v)
        harmonies.append((int(comp_r*255), int(comp_g*255), int(comp_b*255)))
        
    elif harmony_type == "triadic":
        # Triadic colors (120 degrees apart)
        for offset in [1/3, 2/3]:
            tri_h = (h + offset) % 1.0
            tri_r, tri_g, tri_b = colorsys.hsv_to_rgb(tri_h, s, v)
            harmonies.append((int(tri_r*255), int(tri_g*255), int(tri_b*255)))
            
    elif harmony_type == "analogous":
        # Analogous colors (30 degrees apart)
        for offset in [-30/360, 30/360]:
            ana_h = (h + offset) % 1.0
            ana_r, ana_g, ana_b = colorsys.hsv_to_rgb(ana_h, s, v)
            harmonies.append((int(ana_r*255), int(ana_g*255), int(ana_b*255)))
    
    return harmonies

def extract_colors_kmeans(image, n_colors=5):
    """Extract dominant colors using K-means clustering"""
    # Convert image to RGB array
    img_array = np.array(image.convert('RGB'))
    img_array = img_array.reshape((-1, 3))
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(img_array)
    
    colors = kmeans.cluster_centers_
    
    # Get the percentage of each color
    labels = kmeans.labels_
    label_counts = np.bincount(labels)
    percentages = label_counts / len(labels) * 100
    
    # Sort by percentage (most dominant first)
    sorted_indices = np.argsort(percentages)[::-1]
    
    return [(colors[i], percentages[i]) for i in sorted_indices]

def extract_colors_colorthief(image, n_colors=5):
    """Extract colors using ColorThief library"""
    if not COLORTHIEF_AVAILABLE:
        return []
    
    # Save image temporarily
    temp_buffer = io.BytesIO()
    image.convert('RGB').save(temp_buffer, format='JPEG')
    temp_buffer.seek(0)
    
    try:
        color_thief = ColorThief(temp_buffer)
        palette = color_thief.get_palette(color_count=n_colors, quality=1)
        
        # Calculate approximate percentages (ColorThief doesn't provide this)
        # We'll use a simple approach based on order
        total = sum(range(1, len(palette) + 1))
        percentages = [(len(palette) - i) / total * 100 for i in range(len(palette))]
        
        return [(color, percentages[i]) for i, color in enumerate(palette)]
    except:
        return []

# Initialize session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'extracted_colors' not in st.session_state:
    st.session_state.extracted_colors = []
if 'selected_color_index' not in st.session_state:
    st.session_state.selected_color_index = None
if 'expanded_harmony' not in st.session_state:
    st.session_state.expanded_harmony = {}

# Main title - Updated layout
st.markdown('<h1 class="brand-title">Wild Pick 2.0</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">Your Color Palette Explorer</p>', unsafe_allow_html=True)

# Upload section (no title)
uploaded_file = st.file_uploader(
    "Upload/Browse Images",
    type=['png', 'jpg', 'jpeg', 'webp'],
    help="Drag & drop an image here or click to browse your files. Supports PNG, JPG, JPEG, WEBP formats."
)

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)

# Extraction controls (simplified and centered)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("")  # Empty space for balance

with col2:
    # Centered slider
    num_colors = st.slider("Number of Colors", 3, 12, 6)
    
    # Add some spacing
    st.write("")
    
    # Extract Colors button - always visible but only functional with image
    button_disabled = st.session_state.uploaded_image is None
    button_text = "Extract Colors" if not button_disabled else "Upload Image First"
    
    if st.button(button_text, type="primary", use_container_width=True, disabled=button_disabled):
        if st.session_state.uploaded_image:
            with st.spinner("Extracting colors..."):
                # Always use K-Means Clustering (default method)
                colors = extract_colors_kmeans(st.session_state.uploaded_image, num_colors)
                
                st.session_state.extracted_colors = colors
                st.session_state.selected_color_index = None
                st.session_state.expanded_harmony = {}
                st.success(f"✓ Extracted {len(colors)} colors")

with col3:
    st.write("")  # Empty space for balance

# Core Colors section
if st.session_state.extracted_colors:
    st.markdown('<div class="section-header">Your Image Palette</div>', unsafe_allow_html=True)
    
    # Display color grid using Streamlit columns
    cols_per_row = 3
    colors = st.session_state.extracted_colors
    
    for i in range(0, len(colors), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(colors):
                color, percentage = colors[i + j]
                r, g, b = [int(c) for c in color]
                hex_color = rgb_to_hex((r, g, b))
                color_name = get_color_name((r, g, b))
                c, m, y, k = rgb_to_cmyk(r, g, b)
                
                # Create tints
                tint_75 = create_tint((r, g, b), 75)
                tint_50 = create_tint((r, g, b), 50)
                
                selected_class = "selected" if st.session_state.selected_color_index == (i + j) else ""
                
                with cols[j]:
                    # Color swatch container
                    st.markdown(f'''
                    <div class="color-swatch-container">
                        <div class="color-swatch {selected_class}" style="background-color: {hex_color};"></div>
                        <div class="color-name">{color_name}</div>
                        <div class="color-values">
                            CMYK: {c}, {m}, {y}, {k}<br>
                            RGB: {r}, {g}, {b}<br>
                            HEX: {hex_color}
                        </div>
                        <div class="tints-strip">
                            <div class="tint-swatch" style="background-color: {hex_color};">
                                <div class="tint-label">100%</div>
                            </div>
                            <div class="tint-swatch" style="background-color: {rgb_to_hex(tint_75)};">
                                <div class="tint-label">75%</div>
                            </div>
                            <div class="tint-swatch" style="background-color: {rgb_to_hex(tint_50)};">
                                <div class="tint-label">50%</div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    
    # Color selection buttons (fallback for when JavaScript doesn't work)
    st.markdown("**Select a color to explore harmonies:**")
    
    cols = st.columns(len(st.session_state.extracted_colors))
    for i, (color, percentage) in enumerate(st.session_state.extracted_colors):
        r, g, b = [int(c) for c in color]
        color_name = get_color_name((r, g, b))
        
        with cols[i]:
            if st.button(f"Select {color_name}", key=f"select_{i}"):
                st.session_state.selected_color_index = i
                st.rerun()
    
    # Harmony Playground
    if st.session_state.selected_color_index is not None:
        selected_color, _ = st.session_state.extracted_colors[st.session_state.selected_color_index]
        r, g, b = [int(c) for c in selected_color]
        hex_color = rgb_to_hex((r, g, b))
        color_name = get_color_name((r, g, b))
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">Harmony Playground - {color_name}</div>', unsafe_allow_html=True)
        
        # Harmony controls
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            show_complementary = st.checkbox("Complementary", value=True)
        with col2:
            show_analogous = st.checkbox("Analogous (±30°)", value=True)
        with col3:
            show_triadic = st.checkbox("Triadic (±120°)", value=True)
        
        # Display harmonies using Streamlit components
        st.markdown('<div class="harmony-tray expanded">', unsafe_allow_html=True)
        
        if show_complementary:
            complementary = create_color_harmony((r, g, b), "complementary")
            st.markdown('<div class="harmony-group">', unsafe_allow_html=True)
            st.markdown('<div class="harmony-title">Complementary</div>', unsafe_allow_html=True)
            
            harmony_cols = st.columns([1, 3, 1])
            with harmony_cols[1]:
                comp_cols = st.columns(len(complementary))
                for i, comp_color in enumerate(complementary):
                    comp_hex = rgb_to_hex(comp_color)
                    with comp_cols[i]:
                        st.markdown(f'''
                        <div style="text-align: center;">
                            <div class="harmony-mini" style="background-color: {comp_hex}; margin: 0 auto;"></div>
                            <span class="harmony-hex">{comp_hex}</span>
                        </div>
                        ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if show_analogous:
            analogous = create_color_harmony((r, g, b), "analogous")
            st.markdown('<div class="harmony-group">', unsafe_allow_html=True)
            st.markdown('<div class="harmony-title">Analogous</div>', unsafe_allow_html=True)
            
            harmony_cols = st.columns([1, 3, 1])
            with harmony_cols[1]:
                ana_cols = st.columns(len(analogous))
                for i, ana_color in enumerate(analogous):
                    ana_hex = rgb_to_hex(ana_color)
                    with ana_cols[i]:
                        st.markdown(f'''
                        <div style="text-align: center;">
                            <div class="harmony-mini" style="background-color: {ana_hex}; margin: 0 auto;"></div>
                            <span class="harmony-hex">{ana_hex}</span>
                        </div>
                        ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if show_triadic:
            triadic = create_color_harmony((r, g, b), "triadic")
            st.markdown('<div class="harmony-group">', unsafe_allow_html=True)
            st.markdown('<div class="harmony-title">Triadic</div>', unsafe_allow_html=True)
            
            harmony_cols = st.columns([1, 3, 1])
            with harmony_cols[1]:
                tri_cols = st.columns(len(triadic))
                for i, tri_color in enumerate(triadic):
                    tri_hex = rgb_to_hex(tri_color)
                    with tri_cols[i]:
                        st.markdown(f'''
                        <div style="text-align: center;">
                            <div class="harmony-mini" style="background-color: {tri_hex}; margin: 0 auto;"></div>
                            <span class="harmony-hex">{tri_hex}</span>
                        </div>
                        ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Harmony button
        if st.button("Export Harmony (JSON)", key="export_harmony"):
            harmony_data = {
                "base_color": {
                    "name": color_name,
                    "hex": hex_color,
                    "rgb": [r, g, b],
                    "cmyk": list(rgb_to_cmyk(r, g, b))
                },
                "harmonies": {}
            }
            
            if show_complementary:
                complementary = create_color_harmony((r, g, b), "complementary")
                harmony_data["harmonies"]["complementary"] = [
                    {"hex": rgb_to_hex(c), "rgb": list(c)} for c in complementary
                ]
            
            if show_analogous:
                analogous = create_color_harmony((r, g, b), "analogous")
                harmony_data["harmonies"]["analogous"] = [
                    {"hex": rgb_to_hex(c), "rgb": list(c)} for c in analogous
                ]
            
            if show_triadic:
                triadic = create_color_harmony((r, g, b), "triadic")
                harmony_data["harmonies"]["triadic"] = [
                    {"hex": rgb_to_hex(c), "rgb": list(c)} for c in triadic
                ]
            
            st.download_button(
                "Download Harmony JSON",
                json.dumps(harmony_data, indent=2),
                file_name=f"wild_pick_2_harmony_{color_name.lower()}.json",
                mime="application/json"
            )

    # Export Palette Section
    if st.session_state.extracted_colors:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Export Your Palette</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            export_format = st.selectbox(
                "Choose Export Format",
                ["JSON (Complete Data)", "PDF Report", "CSS Variables", "Text List"],
                help="Select the format for exporting your color palette"
            )
            
            if st.button("Export Palette", type="primary", use_container_width=True):
                colors = st.session_state.extracted_colors
                
                if export_format == "JSON (Complete Data)":
                    palette_data = {
                        "palette": [],
                        "extracted_from": "Wild Pick 2.0",
                        "timestamp": str(datetime.now())
                    }
                    
                    for color, percentage in colors:
                        r, g, b = int(color[0]), int(color[1]), int(color[2])
                        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                        c, m, y, k = rgb_to_cmyk(r, g, b)
                        
                        palette_data["palette"].append({
                            "name": get_color_name(color),
                            "hex": rgb_to_hex(color),
                            "rgb": [r, g, b],
                            "hsv": [int(h*360), int(s*100), int(v*100)],
                            "cmyk": [c, m, y, k],
                            "percentage": round(percentage, 1),
                            "tints": {
                                "75%": rgb_to_hex(create_tint((r, g, b), 75)),
                                "50%": rgb_to_hex(create_tint((r, g, b), 50))
                            }
                        })
                    
                    st.download_button(
                        "Download JSON",
                        json.dumps(palette_data, indent=2),
                        file_name="wild_pick_2_palette.json",
                        mime="application/json"
                    )
                
                elif export_format == "PDF Report":
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        from reportlab.lib.units import inch
                        from reportlab.lib import colors as rl_colors
                        from reportlab.lib.enums import TA_CENTER, TA_LEFT
                        
                        # Generate PDF with image and color data
                        buffer = io.BytesIO()
                        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                                              rightMargin=0.7*inch, leftMargin=0.7*inch,
                                              topMargin=0.8*inch, bottomMargin=0.8*inch)
                        
                        styles = getSampleStyleSheet()
                        title_style = ParagraphStyle(
                            'CustomTitle',
                            parent=styles['Heading1'],
                            fontSize=24,
                            spaceAfter=30,
                            alignment=TA_CENTER,
                            fontName='Helvetica-Bold'
                        )
                        
                        story = []
                        story.append(Paragraph("Wild Pick 2.0", title_style))
                        story.append(Paragraph("Color Palette Analysis Report", styles['Normal']))
                        story.append(Spacer(1, 20))
                        
                        # Add source image if available
                        if st.session_state.uploaded_image:
                            story.append(Paragraph("Source Image", styles['Heading2']))
                            img_buffer = io.BytesIO()
                            img_copy = st.session_state.uploaded_image.copy()
                            img_copy.thumbnail((400, 300), Image.Resampling.LANCZOS)
                            img_copy.save(img_buffer, format='PNG')
                            img_buffer.seek(0)
                            
                            img = RLImage(img_buffer, width=400, height=300)
                            story.append(img)
                            story.append(Spacer(1, 20))
                        
                        # Color palette table
                        story.append(Paragraph("Extracted Color Palette", styles['Heading2']))
                        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
                        story.append(Spacer(1, 15))
                        
                        table_data = [['Color', 'Name', 'HEX', 'RGB', 'CMYK', 'Coverage', 'Tints']]
                        
                        for color, percentage in colors:
                            r, g, b = int(color[0]), int(color[1]), int(color[2])
                            hex_color = rgb_to_hex(color)
                            color_name = get_color_name(color)
                            c, m, y, k = rgb_to_cmyk(r, g, b)
                            tint_75 = rgb_to_hex(create_tint((r, g, b), 75))
                            tint_50 = rgb_to_hex(create_tint((r, g, b), 50))
                            
                            color_cell = f'<font color="{hex_color}">●●●●●</font>'
                            
                            table_data.append([
                                Paragraph(color_cell, styles['Normal']),
                                color_name,
                                hex_color,
                                f"rgb({r}, {g}, {b})",
                                f"cmyk({c}%, {m}%, {y}%, {k}%)",
                                f"{percentage:.1f}%",
                                f"75%: {tint_75}\n50%: {tint_50}"
                            ])
                        
                        table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.4*inch, 0.6*inch, 1.4*inch])
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), rl_colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 9),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), rl_colors.beige),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 8),
                            ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        
                        story.append(table)
                        story.append(Spacer(1, 20))
                        
                        # Footer
                        story.append(Paragraph("Generated by Wild Pick 2.0 - Your Color Palette Explorer", styles['Normal']))
                        
                        doc.build(story)
                        buffer.seek(0)
                        
                        st.download_button(
                            "Download PDF Report",
                            buffer.getvalue(),
                            file_name="wild_pick_2_palette_report.pdf",
                            mime="application/pdf"
                        )
                    except ImportError:
                        # Fallback if reportlab not available
                        st.error("PDF generation requires the 'reportlab' library. Install with: pip install reportlab")
                        st.info("Alternatively, use JSON or Text List export formats.")
                
                elif export_format == "CSS Variables":
                    css_vars = ":root {\n"
                    for i, (color, _) in enumerate(colors):
                        color_name = get_color_name(color).lower()
                        css_vars += f"  --color-{color_name}-{i+1}: {rgb_to_hex(color)};\n"
                        # Add tints
                        css_vars += f"  --color-{color_name}-{i+1}-75: {rgb_to_hex(create_tint(color, 75))};\n"
                        css_vars += f"  --color-{color_name}-{i+1}-50: {rgb_to_hex(create_tint(color, 50))};\n"
                    css_vars += "}"
                    
                    st.download_button(
                        "Download CSS",
                        css_vars,
                        file_name="wild_pick_2_palette.css",
                        mime="text/css"
                    )
                
                elif export_format == "Text List":
                    text_list = "Wild Pick 2.0 - Color Palette\n"
                    text_list += "=" * 30 + "\n\n"
                    
                    for i, (color, percentage) in enumerate(colors, 1):
                        r, g, b = int(color[0]), int(color[1]), int(color[2])
                        hex_color = rgb_to_hex(color)
                        color_name = get_color_name(color)
                        
                        text_list += f"{i}. {color_name}\n"
                        text_list += f"   {hex_color}\n"
                        text_list += f"   RGB({r}, {g}, {b})\n"
                        text_list += f"   {percentage:.1f}% coverage\n\n"
                    
                    st.download_button(
                        "Download Text List",
                        text_list,
                        file_name="wild_pick_2_palette.txt",
                        mime="text/plain"
                    )

else:
    # Show sample colors when no image is uploaded
    st.markdown('<div class="section-header">Sample Palette</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Upload an image above to extract its color palette and explore harmonies</p>', unsafe_allow_html=True)
    
    # Sample brand colors
    sample_colors = [
        ((231, 76, 60), "Red"),     # #E74C3C
        ((52, 152, 219), "Blue"),   # #3498DB
        ((46, 204, 113), "Green"),  # #2ECC71
        ((243, 156, 18), "Orange"), # #F39C12
        ((155, 89, 182), "Purple")  # #9B59B6
    ]
    
    # Display sample colors using Streamlit columns
    cols = st.columns(len(sample_colors))
    
    for i, (color, name) in enumerate(sample_colors):
        r, g, b = color
        hex_color = rgb_to_hex(color)
        c, m, y, k = rgb_to_cmyk(r, g, b)
        
        tint_75 = create_tint(color, 75)
        tint_50 = create_tint(color, 50)
        
        with cols[i]:
            st.markdown(f'''
            <div class="color-swatch-container">
                <div class="color-swatch" style="background-color: {hex_color};"></div>
                <div class="color-name">{name}</div>
                <div class="color-values">
                    CMYK: {c}, {m}, {y}, {k}<br>
                    RGB: {r}, {g}, {b}<br>
                    HEX: {hex_color}
                </div>
                <div class="tints-strip">
                    <div class="tint-swatch" style="background-color: {hex_color};">
                        <div class="tint-label">100%</div>
                    </div>
                    <div class="tint-swatch" style="background-color: {rgb_to_hex(tint_75)};">
                        <div class="tint-label">75%</div>
                    </div>
                    <div class="tint-swatch" style="background-color: {rgb_to_hex(tint_50)};">
                        <div class="tint-label">50%</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
