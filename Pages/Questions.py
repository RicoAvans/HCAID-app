import streamlit as st
import pandas
import numpy
import time

st.title('Vragenlijst')

#st.subheader('Welkom')

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
           ('Voor of tijdens de lunch', 'Tussen 15:00 en 17:00', 'Tussen 17:00 en 19:00', 'Tussen 19:00 en 21:00', 'Tussen 21:00 en 23:00', 'Na 23:00'))

with form:
    st.write('')
    st.subheader('Slapen')
    st.write('Hoe laat slaap je en hoe hoog is de kwaliteit?')

form.radio("Hoe laat ga je doordeweeks gemiddeld naar bed?",
           ('Tussen 21:00 en 22:00', 'Tussen 22:00 en 23:00', 'Tussen 23:00 en 00:00', 'Tussen 00:00 en 02:00', 'Tussen 02:00 en 04:00'))
form.radio("Als je gaat slapen, hoe lang lig je nog wakker voordat je slaapt?",
           ('Minder dan 10 min', 'Tussen 10 min en 30 min', 'Tussen 30 min en 1 uur', 'Meer dan 1 uur'))
form.radio("Welk cijfer geef je de kwaliteit van je slaap? Denk aan moeilijk in slaap komen, vaak wakker worden, etc. (Hoger is beter)",
           ('1', '2', '3', '4', '5'))

# Now add a submit button to the form:
form.form_submit_button("Submit")

