import pandas as pd
import streamlit as st
import pandas
import numpy
import time
import tensorflow as tf
from tensorflow import keras

# ========================================= Config =========================================
st.set_page_config(page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items={
    'Get Help': None,
    'Report a bug': "mailto:rr.kronenburg@student.avans.nl",
    'About': "Gemaakt door Ricardo Kronenburg, Mechatronica student aan Avans Hogeschool Breda "
})

if 'resultsReady' not in st.session_state:
    st.session_state.resultsReady = False


# ========================================= Neural network =========================================
@st.cache(allow_output_mutation=True)
def fetch_model():
    models = tf.keras.models.load_model('model_save/model84')
    return models


# ========================================= Start pagina =========================================
def welcome():
    # -------------------------------- Functionaliteit --------------------------------
    def switch_to_questionair():
        st.session_state["page"] = "questionair"
        del st.session_state.resultsReady

    # -------------------------------- UI --------------------------------
    st.title('Caffeïne en slapen')

    st.subheader('Welkom')
    st.subheader('Uitleg vragen')
    st.subheader('Uitleg soort AI')
    st.caption("**Alle data die u invult wordt niet opgeslagen en is op geen enkele manier naar u terug te leiden**")

    st.button("Start", on_click=switch_to_questionair)


# ========================================= Vragenlijst pagina ====================================
def questionair():
    # -------------------------------- Functionaliteit --------------------------------
    def switch_to_results():
        st.session_state["page"] = "results"

    # -------------------------------- UI --------------------------------
    st.title('Vragenlijst')

    # st.subheader('Welkom')

    form = st.form("my_form")
    with form:
        st.subheader('Cafeïne gebruik')
        st.markdown('Hoeveel cafeïnehoudende producten nuttig je?')
        st.write('')


    hoeveel_per_dag = form.radio("Hoeveel cafeïnehoudende producten producten (koffie/thee/cola/energydrank/"
               "preworkout/etc.) nuttig je per dag? Je mag de consumpties per dag bij elkaar "
               "optellen",
               ('Geen', '1 tot 2 per dag', '3 tot 4 per dag', '5 tot 6 per dag', 'Meer dan 6 per dag'))
    def categorise_hoeveel(hoeveel_per_dag):
        if hoeveel_per_dag == "Geen":
            return 0
        elif hoeveel_per_dag == "1 tot 2 per dag":
            return 1
        elif hoeveel_per_dag == "3 tot 4 per dag":
            return 3
        elif hoeveel_per_dag == "5 tot 6 per dag":
            return 5
        elif hoeveel_per_dag == "meer dan 6 per dag":
            return 7
    #st.session_state["data"]["hoeveel"] = [categorise_hoeveel(hoeveel_per_dag)]


    wanneer_laatste = form.radio("Wanneer heb je (meestal) je laatste cafeïnehoudende product van de dag?",
               ('Voor of tijdens de lunch', 'Tussen 15:00 en 17:00', 'Tussen 17:00 en 19:00', 'Tussen 19:00 en 21:00',
                'Tussen 21:00 en 23:00', 'Na 23:00'))
    def categorise_wanneer(wanneer):
        if wanneer == "Voor of tijdens de lunch":
            return 0
        elif wanneer == "Tussen 15:00 en 17:00":
            return 15
        elif wanneer == "Tussen 17:00 en 19:00":
            return 17
        elif wanneer == "Tussen 19:00 en 21:00":
            return 19
        elif wanneer == "Tussen 21:00 en 23:00":
            return 21
        elif wanneer == "Na 23:00":
            return 23
    st.session_state["data"]["wanneer"] = [categorise_wanneer(wanneer_laatste)]

    with form:
        st.write('')
        st.subheader('Slapen')
        st.write('Hoe laat slaap je en hoe hoog is de kwaliteit?')

        laat_bed = form.radio("Hoe laat ga je doordeweeks gemiddeld naar bed?",
               ('Tussen 21:00 en 22:00', 'Tussen 22:00 en 23:00', 'Tussen 23:00 en 00:00', 'Tussen 00:00 en 02:00',
                'Tussen 02:00 en 04:00'))
        def categorise_laat(laat):
            if laat == "Tussen 21:00 en 22:00":
                return 21
            elif laat == "Tussen 22:00 en 23:00":
                return 22
            elif laat == "Tussen 23:00 en 00:00":
                return 23
            elif laat == "Tussen 00:00 en 02:00":
                return 24
            elif laat == "Tussen 02:00 en 04:00":
                return 26

        st.session_state["data"]["laat"] = [categorise_laat(laat_bed)]

        #kwaliteit_slapen = form.radio(
        #"Welk cijfer geef je de kwaliteit van je slaap? Denk aan moeilijk in slaap komen, vaak wakker worden, "
        #"etc. (Hoger is beter)",
        #('1', '2', '3', '4', '5'))


        # Add a submit button to the form:
        form.form_submit_button("Submit")

    # features = {
    #     'hoeveel_per_dag': hoeveel_per_dag,
    #     'wanneer_laatste': wanneer_laatste,
    #     'laat_bed': laat_bed,
    #     'lang_tot_slapen': lang_tot_slapen,
    #     'kwaliteit_slapen': kwaliteit_slapen,
    # }
    #
    # featuresDF = pd.DataFrame([features])
    # featuresDF2 = featuresDF.drop(["hoeveel", "lang", "kwaliteit"])
    # featuresList = featuresDF2.values.tolist()



    st.button("Bereken tijd tot in slaap komen", on_click=switch_to_results)


# ========================================= Resultaat pagina =========================================
def results():
    st.session_state.resultsReady = True

    # -------------------------------- Functionaliteit --------------------------------
    def switch_to_questionair():
        st.session_state["page"] = "questionair"
        del st.session_state.resultsReady

    def switch_to_welcome():
        st.session_state["page"] = "welcome"

    # -------------------------------- Neural network --------------------------------


    #model = fetch_model()
    #Y = model.predict(X, verbose=2)

    # -------------------------------- UI --------------------------------
    st.title("Resultaten")
    df = pd.DataFrame(st.session_state["data"])
    model = fetch_model()

    prediction = model.predict(df)
    st.write(prediction)
    # st.write(prediction[0])
    # st.write(prediction[0][0])
    # st.write(prediction[0][1])
    # st.write(prediction[0][2])
    # st.write(prediction[0][3])

    total = prediction[0][0] + prediction[0][1] + prediction[0][2] + prediction[0][3]
    st.write(total)




    col1, buff, col2 = st.columns([2, 1, 2])
    with col1:
        st.button("Vul de vragenlijst opnieuw in", on_click=switch_to_questionair)

    with col2:
        st.button("Terug naar welkom scherm", on_click=switch_to_welcome)


# ========================================= Sidebar =========================================
sidebar = st.sidebar
sidebar.header('Caffeïne gebruik en slapen')
sidebar.subheader('Wissel hier van tablad')

button_welcome = st.sidebar.button("Welkom")
if button_welcome:
    st.session_state["page"] = "welcome"

button_vragen = st.sidebar.button("Vragenlijst")
if button_vragen:
    st.session_state["page"] = "questionair"

if st.session_state.resultsReady is True:
    button_results = st.sidebar.button("Resultaten")
    if button_results:
        st.session_state["page"] = "results"

# ========================================= Wisselen van pagina =========================================
pages = {
    "welcome": welcome,
    "questionair": questionair,
    "results": results
}

if "page" not in st.session_state:
    st.session_state["page"] = "welcome"
    st.session_state["data"] = {}

pages[st.session_state["page"]]()
