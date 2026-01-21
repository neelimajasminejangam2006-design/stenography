
import pyttsx3
import os

import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Image Steganography System",
    layout="centered"
)

# ---------- HEADER ----------
st.title("🔐 Image Steganography – Secure Data Hiding")
st.write(
    "This application demonstrates **image steganography and reverse steganography** "
    "using the **Least Significant Bit (LSB)** technique."
)

st.divider()

# ---------- STEP DESCRIPTION ----------
with st.expander("📘 Steganography Process Overview", expanded=True):
    st.markdown("""
    **1. Input Image:** User uploads a JPEG image  
    **2. Preprocessing:** Image is converted to grayscale and resized to standard size (256×256)  
    **3. Steganography:** A single character is hidden using LSB technique  
    **4. Stego Image:** Image containing hidden data is generated  
    **5. Reverse Steganography:** Stego image is analyzed to retrieve the hidden character  
    """)

# ---------- IMAGE PREPROCESS ----------
def preprocess_image(image):
    gray = np.array(image.convert("L"))
    resized = cv2.resize(gray, (256, 256))
    return resized

# ---------- HIDE CHARACTER ----------
def hide_character(image, character):
    binary = format(ord(character), '08b')
    flat = image.flatten()

    for i in range(8):
        flat[i] = (flat[i] & 254) | int(binary[i])

    stego = flat.reshape(image.shape)
    cv2.imwrite("stego_image.png", stego)
    return stego

# ---------- EXTRACT CHARACTER ----------
def extract_character():
    image = cv2.imread("stego_image.png", cv2.IMREAD_GRAYSCALE)
    flat = image.flatten()

    bits = ""
    for i in range(8):
        bits += str(flat[i] & 1)

    return bits, chr(int(bits, 2))
#---------------audio-----------
def generate_speech(character):
    engine = pyttsx3.init()
    engine.save_to_file(character, "speech.wav")
    engine.runAndWait()


# ---------- UI ----------
st.subheader("📁 Step 1: Upload JPEG Image")
uploaded_file = st.file_uploader(
    "Select a JPEG image",
    type=["jpg", "jpeg"]
)

if uploaded_file:
    original_image = Image.open(uploaded_file)

    st.markdown("### Original Input Image")
    st.image(original_image, width=320)

    st.divider()

    st.subheader("✍️ Step 2: Enter Character to Hide")
    char = st.text_input("Enter ONE character", max_chars=1)

    if st.button("🔒 Perform Steganography"):
        if len(char) != 1:
            st.error("Please enter exactly one character.")
        else:
            processed = preprocess_image(original_image)

            st.markdown("### Preprocessed Image (Grayscale & Standard Size)")
            st.image(processed, width=320)

            stego = hide_character(processed, char)

            st.success("Steganography completed successfully.")
            st.markdown("### Stego Image (Contains Hidden Character)")
            st.image(stego, width=320)

    st.divider()

    st.subheader("🔍 Step 3: Reverse Steganography (Extraction)")
    st.write(
        "The stego image generated above is now used as input "
        "for reverse steganography to retrieve the hidden character."
    )

if st.button("🔓 Perform Reverse Steganography"):
    try:
        bits, extracted = extract_character()

        st.markdown("**Extracted LSB Bits:**")
        st.code(bits)

        st.success(f"Retrieved Character: **{extracted}**")

        # --- AUTOMATIC TEXT TO SPEECH ---
        generate_speech(extracted)

        if os.path.exists("speech.wav"):
            st.audio("speech.wav", format="audio/wav", autoplay=True)

    except:
        st.error("Stego image not found. Perform steganography first.")
