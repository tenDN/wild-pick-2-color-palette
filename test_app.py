import streamlit as st
import numpy as np
from PIL import Image
import io

# Simple test app to verify deployment
st.set_page_config(page_title="Test Wild Pick 2.0", layout="wide")

st.title("🎨 Wild Pick 2.0 - Test Version")
st.write("If you can see this, the deployment is working!")

# Simple file uploader test
uploaded_file = st.file_uploader("Test file upload", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Upload successful!", width=300)
    st.success("✅ File upload and image processing works!")

# Test basic functionality
if st.button("Test Button"):
    st.balloons()
    st.write("✅ Button interactions work!")

st.write("---")
st.write("**Dependencies loaded successfully:**")
st.write("- ✅ Streamlit")
st.write("- ✅ NumPy")
st.write("- ✅ PIL (Pillow)")
st.write("- ✅ IO")

st.write("**Next step:** If this works, we'll activate the full Wild Pick 2.0 features!")
