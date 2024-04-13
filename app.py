import streamlit as st
import base64


with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html = True)

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Inter', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('bg.png')
