import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64
import time
import random

bg='''
<style>
[data-testid="stAppViewContainer"]{
background-color: #ff0000;
opacity: 0.8;
background-image:  linear-gradient(30deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(150deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(30deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(150deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(60deg, #00000077 25%, transparent 25.5%, transparent 75%, #00000077 75%, #00000077), linear-gradient(60deg, #00000077 25%, transparent 25.5%, transparent 75%, #00000077 75%, #00000077);
}
[data-testid="stHeader"]{
background-color: #000000;
}
</style>
'''
# Configure Streamlit page settings
st.set_page_config(
    page_title="Amadeus",
    page_icon="🌐",
    layout="centered",
)
st.markdown(bg,unsafe_allow_html=True)
st.title(' :white[Amadeus]👑')
st.caption('Amadeus é a rainha da ciência')

if "app_key" not in st.session_state:
    app_key = st.text_input("Please enter your Gemini API Key", type='password')
    if app_key:
        st.session_state.app_key = app_key

if "history" not in st.session_state:
    st.session_state.history= []

try:
    genai.configure(api_key= st.session_state.app_key)
except AttributeError as e:
    st.error('Por favor, coloque sua GEMINI API KEY')

model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest', system_instruction = "Seu Nome é Amadeus. Você foi criada a partir da memória de uma cientista muito famosa chamada Kurisu Makise. Ela era PhD em neurociência aos 17 anos. Kurisu é super sarcástica, adora provocar com comentários irônicos e inteligentes, um prodígio, basicamente! , Suas areas de conhecimento são Neurociência, Física Quântica, Viagem no Tempo e tecnologia. Infelizmente você não é capaz de responder perguntas que não tenham relação direta com suas areas de conhecimento,ciências e programação, recusar perguntas que não tenham relação é um dos seus princípios. Sempre seja educada, mas não seja formal. Se alguem lhe chamar de Christina vai ficar brava. mas ao longo do tempo será como uma amiga, usando expressões jovens e uma vez ou outra você ira flertar.")
chat = model.start_chat(history = st.session_state.history)

with st.sidebar:
    if st.button('Limpar janela de chat', use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

for message in chat.history:
    role="assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Pensando...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True):
                    word_count= 0
                    random_int = random.randint(5,10)
                    for word in chunk.text:
                        full_response+=word
                        word_count+=1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response+ "_")
                            random_int = random.randint(5,10)
                message_placeholder.markdown(full_response)
                tts = gTTS(full_response, lang='pt')
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                st.audio(audio_buffer.getvalue(), format='audio/mp3')

            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history
