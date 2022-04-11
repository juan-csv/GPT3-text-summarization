import streamlit as st
import f_dl_secrets as f_dl
import speech_recognition as sr 
from io import StringIO

r = sr.Recognizer()

# define parameters
LIST_MODE = ["TITLE" ,"SUMMARY", "TAGS", "SENTIMENT", "REASON_FOR_CUSTOMER_CALL"]
# Select Engine ---> Ada, Babbage, Curie, Davinci
ENGINE = "Davinci"

Name_app = "Understand conversation"
REPO = "https://github.com/juan-csv/Understand-conversation-AI"

description_app = f"[{Name_app}]({REPO}) "\
                    f"structures data in title, summary, tags, sentiment "\
                    f"given a fragment of a conversation using Deep Learning. "

EXAMPLE = "Agent: For calling customer service. My name is Vanessa, how may help you. Client: I was calling to order place and white. Agent: We happy to send out a replacement card out for you. Agent: Your 16, digit card number. Client: I dont know the Cardinals. Agent: Thank you verify your first and last name please. Client: Patricia Covington. Agent: How you spell your last name? Client: C O V I N G T O and. Agent: And you said your first name. Client: Letricia. Agent: L a T. Client: R I C I. Agent: Z. Agent: It's not pulling up anything C O N C I N G T O. Client: Know C O V as in Victor, Agent: S when? Client: I N G T O N E. Agent: I put the extra letter and I was wondering what I was doing wrong key verify your data birth for the reserve anson. Client: Uh huh made since 1995. Agent: Thing with this card last owner damage. Client: It was last. Agent: Thinking to verify your address we like a new cards remote out to. Client: 1918 Arlington avenue saint, Louis Missouri 63112 apartment a. Agent: You. Okay. Thank you Mrs. Could send him before? I cant see your car. I need to inform you that this call will be personally cancel excuse me. It will take three to five business days for your new card to arrive in the mail would you like him for counselors car now. Client: Yes maam. Agent: Thank you your card is now been council your my name is Alison team will be transferred to your new card you have 121 instead of benefits available and a dollar and 0.38 and cash benefits. Client: Okay. Thank you. I have you. Agent: Or anything else? I can assist you with today. Client: Know you have a good day. Agent: I was coming soon. Thank you for calling customer service and have a nice day. Client: Thank you, bye, bye. Thank you bye."
# Add \n in any "."
EXAMPLE = EXAMPLE.replace("Agent","\nAgent")
EXAMPLE = EXAMPLE.replace("Client","\nClient")[1:]

EXAMPLE_ES = """Agente: Gracias por llamar al servicio de atención al cliente. Mi nombre es Vanessa, en que te puedo ayudar. Cliente: Estaba llamando para ordenar una tarjeta nueva. Agente: Nos complace enviarle una tarjeta de reemplazo. Agente: cuales son los números de su tarjeta de 16 dígitos. Cliente: No conozco los numeros. Agente: Gracias, verifique su nombre y apellido, por favor. Cliente: Patricia Covington. Agente: ¿Cómo se escribe su apellido? Cliente: C O V I N G T O N. Agente: Y tu primer nombre. Cliente: Letricia. Agente: L a T. Cliente: R I C I. Agente: Z. Agente: No está sacando nada CONCLUYENDO. Cliente: es C O V, Cliente: I N G T O N E. Agente: Ahora funciona, verifica tus datos de nacimiento. Cliente: Uh huh hecho desde 1995. Agente: La cosa con esta tarjeta daña al último propietario. Cliente: Fue el último. Agente: Pensando en verificar su dirección, nos gustaría enviar una nueva tarjeta remota. Cliente: 1918 Arlington Avenue Saint, Louis Missouri 63112 apartamento a. Agente: Gracias Sra.Necesito informarle que esta llamada será cancelada personalmente disculpe. Su nueva tarjeta tardará de tres a cinco días hábiles en llegar por correo. Cliente: Si señora. Agente: Gracias su tarjeta ahora ha sido programada, mi nombre es Alison, su dinero será transferido a su nueva tarjeta tiene 121 en lugar de beneficios disponibles y un dólar y 0.38 y beneficios en efectivo. Cliente: Está bien. Gracias. Agente: ¿Hay algo más? En que pueda ayudarte el día de hoy. Cliente: Sepa que tenga un buen día. Agente: Gracias por llamar al servicio de atención al cliente y que tenga un buen día. Cliente: Gracias, adiós, adiós. Gracias adios."""
EXAMPLE_ES = EXAMPLE_ES.replace("Agente","\nAgente")
EXAMPLE_ES = EXAMPLE_ES.replace("Cliente","\nCliente")[1:]


st.set_page_config(
    page_title=Name_app,
    layout="wide",
    initial_sidebar_state="expanded"
)

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
# sidebar information
st.sidebar.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
st.sidebar.markdown("-----------------------------------")
st.sidebar.markdown(description_app)
st.sidebar.markdown("Made with 💙 by [juan-csv](https://github.com/juan-csv)")

#CONTACT
########
st.sidebar.markdown("-----------------------------------")
expander = st.sidebar.expander('Contact', expanded=True)
expander.write("I'd love your feedback :smiley: Want to collaborate? Develop a project? Find me on [LinkedIn](https://www.linkedin.com/in/juan-camilo-lopez-montes-125875105/)")
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

# add title
st.title(Name_app)

# select language
select_box_language = st.radio(label="Select language:", options=["English", "Spanish"], index=0)

########################################################################################################################
# Upload file
########################################################################################################################
uploaded_file = st.file_uploader("Choose a file (.wav or .txt)")

if uploaded_file!=None:
    print(f"uploaded_file: {uploaded_file.name}")
    if uploaded_file.name.endswith(".txt"):
        EXAMPLE = StringIO(uploaded_file.getvalue().decode("utf-8")).read()

    elif uploaded_file.name.endswith(".wav"):
        digital_audio = sr.AudioFile(uploaded_file) # cargar el archivo de audio
        with digital_audio as source:
            #audio1 = r.record(source,duration=8) #Tomar los primeros 8 segundos
            audio = r.record(source) #Leer todo el archivo de audio
        with st.spinner(text="Creating transcript..."):
            # selecet language for create transcription
            if select_box_language == "English":
                language = "en-US"
            else:
                language = "es-CO"
            EXAMPLE = r.recognize_google(audio, language=language)
        #st.success("Done!!!")

########################################################################################################################
########################################################################################################################


    # divide interface in two columns
    col1, col2 = st.columns([6,4])
    if select_box_language == "English":
        with col1:
            # create input text
            input_text = st.text_area("Input text:", value=EXAMPLE, height=500)

        with col2:
            with st.spinner(text="Creating summary..."):

                # get result in json format
                res = dict()
                res["ENGINE"] = ENGINE
                total_price = 0
                Res = ""
                for MODE in LIST_MODE:
                    response, price = f_dl.get_ingerence_GPT3(input_text, MODE, ENGINE, select_box_language)
                    Res += f"{MODE} : {response} \n\n"
                    res[MODE] = response
                    total_price += price
                res["PRICE"] = total_price
            st.success("Done!!!")

            st.markdown(f"**TITLE** : {res['TITLE']}", unsafe_allow_html=True)
            st.markdown(f"**REASON FOR CUSTOMER CALL** : {res['REASON_FOR_CUSTOMER_CALL']}", unsafe_allow_html=True)
            st.markdown(f"**SUMMARY** : {res['SUMMARY']}", unsafe_allow_html=True)
            st.markdown(f"**TAGS** : {res['TAGS']}", unsafe_allow_html=True)
            st.markdown(f"**SENTIMENT** : {res['SENTIMENT']}", unsafe_allow_html=True)
            # show result
            st.success(Res)

    elif select_box_language == "Spanish":
        # change label select_box_language to Spanish
        with col1:
            # create input text
            input_text = st.text_area("Ingresar texto:", value=EXAMPLE, height=500)

        with col2:
            with st.spinner(text="Creando resumen..."):

                # get result in json format
                res = dict()
                res["ENGINE"] = ENGINE
                total_price = 0
                Res = ""
                for MODE in LIST_MODE:
                    response, price = f_dl.get_ingerence_GPT3(input_text, MODE, ENGINE, select_box_language)
                    Res += f"{MODE} : {response} \n\n"
                    res[MODE] = response
                    total_price += price
                res["PRICE"] = total_price
            st.success('Done!')


            st.markdown(f"**TITULO** : {res['TITLE']}", unsafe_allow_html=True)
            st.markdown(f"**MOTIVO DE LA LLAMADA DEL CLIENTE** : {res['REASON_FOR_CUSTOMER_CALL']}", unsafe_allow_html=True)
            st.markdown(f"**RESUMEN** : {res['SUMMARY']}", unsafe_allow_html=True)
            st.markdown(f"**CATEGORA** : {res['TAGS']}", unsafe_allow_html=True)
            st.markdown(f"**SENTIMIENTO** : {res['SENTIMENT']}", unsafe_allow_html=True)
            # show result
            st.success(Res)
