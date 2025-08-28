# Wild Pick 2.0 - Brand Guidelines Color Palette Explorer

## 🎨 Overview

Wild Pick 2.0 is an enhanced color palette extraction tool designed with a clean, brand guidelines aesthetic. It transforms your images into professional color palettes with comprehensive color information and harmony exploration capabilities.

## ✨ Features

### 🎯 Core Features
- **Large Circular Swatches**: Beautiful, professional-looking color swatches in a clean grid layout
- **Complete Color Information**: CMYK, RGB, and HEX values for each color
- **Tint Strips**: Automatic generation of 75% and 50% tints for each color
- **Brand Guidelines Styling**: Minimal, clean design with generous whitespace and subtle dividers

### 🌈 Harmony Playground
- **Complementary Colors**: 180° opposite colors for high contrast
- **Analogous Colors**: ±30° adjacent colors for harmonious schemes
- **Triadic Colors**: ±120° colors for vibrant, balanced palettes
- **Interactive Selection**: Click any color to explore its harmonies
- **JSON Export**: Export harmony data for use in design tools

### 🔧 Technical Features
- **K-Means Clustering**: Advanced color extraction algorithm
- **ColorThief Support**: Alternative extraction method (optional)
- **Responsive Design**: Works on desktop and mobile devices
- **Self-Contained**: All CSS and JavaScript embedded

## 🚀 Quick Start

### Method 1: Using the Run Script (Recommended)
```bash
./run_wild_pick_2.sh
```

### Method 2: Direct Streamlit Command
```bash
streamlit run wild_pick_2.py --server.port 8502
```

### Method 3: Python Command
```bash
python -m streamlit run wild_pick_2.py --server.port 8502
```

## 📋 Requirements

### Required Dependencies
- `streamlit` - Web application framework
- `numpy` - Numerical computing
- `pillow` (PIL) - Image processing
- `scikit-learn` - Machine learning (K-means clustering)
- `colorsys` - Color space conversions (built-in)

### Optional Dependencies
- `colorthief` - Alternative color extraction method

### Installation
```bash
pip install streamlit numpy pillow scikit-learn
# Optional:
pip install colorthief
```

## 🎨 Usage Guide

### 1. Upload an Image
- Click the upload area or drag and drop an image
- Supported formats: PNG, JPG, JPEG, WEBP

### 2. Extract Colors
- Choose extraction method (K-Means or ColorThief)
- Select number of colors (3-12)
- Click "Extract Colors"

### 3. Explore the Palette
- View large circular swatches with complete color information
- See automatic tints (75% and 50%) for each color
- Note the clean, brand guidelines presentation

### 4. Use the Harmony Playground
- Click "Select [Color Name]" for any color
- Toggle harmony types: Complementary, Analogous, Triadic
- View mini color swatches with HEX codes
- Export harmony data as JSON

## 🎯 Design Philosophy

Wild Pick 2.0 follows modern brand guidelines design principles:

- **Minimal Aesthetic**: Clean, uncluttered interface
- **Professional Typography**: Inter font family throughout
- **Generous Whitespace**: Breathing room between elements
- **Subtle Dividers**: Thin rules to separate sections
- **Warm Background**: Light warm-gray (#faf9f7) background
- **Circular Swatches**: Modern, friendly circular color presentations
- **Consistent Spacing**: Systematic spacing and alignment

## 🔧 Technical Details

### Color Extraction
- **K-Means Clustering**: Groups similar pixels to find dominant colors
- **Percentage Calculation**: Shows how much of the image each color represents
- **Smart Sorting**: Colors sorted by dominance in the image

### Color Conversions
- **RGB to CMYK**: Professional print color values
- **RGB to HSV**: Hue, saturation, value for color theory
- **Tint Generation**: Mathematical color lightening
- **Harmony Calculation**: Color wheel mathematics for pleasing combinations

### Export Formats
- **JSON Harmony**: Complete harmony data with base color and relationships
- **Structured Data**: Easy to parse for other applications

## 🌟 What's New in 2.0

Compared to the original Wild Pick:

1. **Brand Guidelines UI**: Complete visual redesign
2. **Circular Swatches**: Large, professional circular color displays
3. **Tint Strips**: Automatic tint generation and display
4. **Harmony Playground**: Interactive color harmony exploration
5. **Enhanced Information**: Complete CMYK, RGB, HEX display
6. **Better Typography**: Professional Inter font family
7. **Improved Layout**: Clean grid system with proper spacing
8. **Export Features**: JSON harmony export functionality

## 📁 File Structure

```
/Users/home/Downloads/moodboard_prototype/
├── wild_pick_2.py              # Main application file
├── run_wild_pick_2.sh          # Run script
├── WILD_PICK_2_README.md       # This documentation
└── requirements.txt            # Dependencies (if using original)
```

## 🎨 Color Theory Integration

Wild Pick 2.0 includes color theory principles:

- **Complementary**: High contrast for emphasis and attention
- **Analogous**: Harmonious colors for peaceful, comfortable designs
- **Triadic**: Vibrant yet balanced colors for dynamic designs
- **Tints**: Lighter variations for subtle accents and backgrounds

## 🚀 Performance

- **Fast Extraction**: Optimized K-means clustering
- **Responsive UI**: Smooth interactions and transitions
- **Memory Efficient**: Proper image handling and cleanup
- **Cross-Platform**: Works on macOS, Windows, and Linux

## 🎯 Use Cases

- **Brand Development**: Create professional brand color palettes
- **Design Systems**: Build comprehensive color guidelines
- **Web Design**: Extract colors for website color schemes
- **Print Design**: Get CMYK values for professional printing
- **Color Inspiration**: Explore harmonious color combinations

## 🔮 Future Enhancements

Potential additions:
- Adobe ASE export
- Pantone color matching
- Color accessibility checking
- Palette comparison tools
- Advanced harmony algorithms

---

**Wild Pick 2.0** - Transform your images into professional brand guidelines color palettes! 🎨✨

