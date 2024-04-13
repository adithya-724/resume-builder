import streamlit as st
import base64
from langchain_core.prompts import ChatPromptTemplate,HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_groq import ChatGroq




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


def generate_output(summary,model):
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name=model)
    
    system_msg = '''You are a helpful AI resume editor. 
                    You will help users transform a raw summary of their roles and responsibilities into bullet points that succintly highlights their expereiences and achievements
                    Each bullet point should be no more than 30 words, directly focusing on what they did, how they did it, and the positive results achieved.
                    Aim for language that is direct and free of fluff.
                    Strictly create pointers only from the given sumary
                    Given below is the summary in triple quotes
                    '''
    system_template = SystemMessagePromptTemplate.from_template(system_msg)

    human_msg = "'''{summary}'''"
    human_template = SystemMessagePromptTemplate.from_template(human_msg)
    
    prompt = ChatPromptTemplate.from_messages([system_template,human_template])

    chain = prompt | chat
    result =  chain.invoke({"summary": summary})
    return result.content

#markup
st.subheader('Resume Builder Assistant')

with st.form('main'):
    st.markdown('**:violet[__Results may vary based on the model you use__]**')
    model = st.radio('Model', ["mixtral-8x7b-32768","llama2-70b-4096"],horizontal=True)
    
    summary = st.text_area('Summary to analyse',placeholder='I worked here for a period of 3 years with experience in so and so projects',height = 200)
    btn = st.form_submit_button('Analyse')

    if btn and len(summary) > 100:
        with st.spinner('Summarising'):
            summary_final = generate_output(summary,model)
            summary_final = summary_final.replace('/n','</br>')
            st.markdown(summary_final)
    elif btn and summary == '':
        st.error('Please enter a summary ')
    else:
        st.error('Please enter a summary of atleast 100 words')