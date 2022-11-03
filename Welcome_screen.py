import streamlit as st
from turtle import onclick
import pandas
import numpy
import time
import tensorflow as tf
from tensorflow import keras

st.set_page_config(page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items={
    'Get Help': None,
    'Report a bug': "mailto:rr.kronenburg@student.avans.nl",
    'About': "Gemaakt door Ricardo Kronenburg, Mechatronica student aan Avans Hogeschool Breda "
})

if 'resultsReady' not in st.session_state:
    st.session_state.resultsReady = False


# ========================================= Start pagina =========================================

def welcome():

    # -------------------------------- Functionaliteit --------------------------------
    def switch_to_questionair():
        st.session_state["page"] = "questionair"

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
        del st.session_state.resultsReady

    # -------------------------------- UI --------------------------------
    st.title('Vragenlijst')

    # st.subheader('Welkom')

    form = st.form("my_form")
    with form:
        st.subheader('Cafeïne gebruik')
        st.markdown('Hoeveel cafeïnehoudende producten nuttig je?')
        st.write('')

    form.radio("Hoeveel cafeïnehoudende producten producten (koffie/thee/cola/energydrank/"
               "preworkout/etc.) nuttig je per dag? Je mag de consumpties per dag bij elkaar "
               "optellen",
               ('Geen', '1 tot 2 per dag', '3 tot 4 per dag', '5 tot 6 per dag', 'Meer dan 6 per dag'))
    form.radio("Wanneer heb je (meestal) je laatste cafeïnehoudende product van de dag?",
               ('Voor of tijdens de lunch', 'Tussen 15:00 en 17:00', 'Tussen 17:00 en 19:00', 'Tussen 19:00 en 21:00',
                'Tussen 21:00 en 23:00', 'Na 23:00'))

    with form:
        st.write('')
        st.subheader('Slapen')
        st.write('Hoe laat slaap je en hoe hoog is de kwaliteit?')

    form.radio("Hoe laat ga je doordeweeks gemiddeld naar bed?",
               ('Tussen 21:00 en 22:00', 'Tussen 22:00 en 23:00', 'Tussen 23:00 en 00:00', 'Tussen 00:00 en 02:00',
                'Tussen 02:00 en 04:00'))
    form.radio("Als je gaat slapen, hoe lang lig je nog wakker voordat je slaapt?",
               ('Minder dan 10 min', 'Tussen 10 min en 30 min', 'Tussen 30 min en 1 uur', 'Meer dan 1 uur'))
    form.radio(
        "Welk cijfer geef je de kwaliteit van je slaap? Denk aan moeilijk in slaap komen, vaak wakker worden, etc. (Hoger is beter)",
        ('1', '2', '3', '4', '5'))

    # Now add a submit button to the form:
    form.form_submit_button("Submit")

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


    # -------------------------------- UI --------------------------------
    st.title("Resultaten")

    col1, buff, col2 = st.columns([2,1,2])
    with col1:
        st.button("Vul de vragenlijst opnieuw in", on_click=switch_to_questionair)

    with col2:
        st.button("Terug naar welkom scherm", on_click=switch_to_welcome)

# # ========================================= Sidebar =========================================
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
# ========================================= Session state =========================================


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
