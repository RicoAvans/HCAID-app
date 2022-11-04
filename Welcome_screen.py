import pandas as pd
import streamlit as st
import pandas
import numpy
import time
import tensorflow as tf
from tensorflow import keras
from PIL import Image

# ========================================= Config =========================================
st.set_page_config(page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items={
    'Get Help': None,
    'Report a bug': "mailto:rr.kronenburg@student.avans.nl",
    'About': "Made by Ricardo Kronenburg, Mechatronica student at Avans Hogeschool Breda "
})

if 'resultsReady' not in st.session_state:
    st.session_state.resultsReady = False

if 'hoeveel' not in st.session_state:
    st.session_state.hoeveel = 0

# ========================================= Images =========================================
koffieplaatje = Image.open('koffie.jpg.')
slapenplaatje = Image.open('slapen.jpg.')

col1, col2 = st.columns([1, 1])
with col1:
    st.image(koffieplaatje, width=328)
with col2:
    st.image(slapenplaatje)


# ========================================= Neural network =========================================
@st.cache(allow_output_mutation=True)
def fetch_model():
    models = tf.keras.models.load_model('model_save/model84')
    return models


# ========================================= Welcome page =========================================
def welcome():
    # -------------------------------- Switching pages --------------------------------
    def switch_to_questionair():
        st.session_state["page"] = "questionair"
        del st.session_state.resultsReady

    # -------------------------------- UI --------------------------------
    st.title('Caffeine and sleeping')

    st.subheader('Welcome')
    st.write("Welcome to the Artificial Intelligence based questionnaire on caffeine intake and sleeping. "
             "Because you are here you are probably having trouble sleeping and would like to find out if your "
             "caffeine intake might have anything to do with that.")

    st.subheader('Explanation questions')
    st.write("The questionnaire consists of 3 questions, the first 2 will be about your caffeine intake, where the "
             "final question will be about your sleeping schedule.*")
    st.caption("*The data you provide in the form is in no way linkable to you and  will be deleted "
               "once you close this tab")
    st.write("")
    st.write("")
    st.write("")

    with st.expander("Explanation Artificial Intelligence"):
        st.write("Artificial Intelligence (AI) is the theory and development of computer systems able to perform "
                 "tasks normally requiring human intelligence, such as visual perception, speech recognition, "
                 "decision-making, and translation between languages.")
        st.write("An AI needs to be trained before it is able to make decisions. This AI has been trained by "
                 "volunteers answering the same questionnaire you will be filling in. The correlation between their "
                 "caffeine intake pattern, sleeping schedule and time it took them to fall asleep was used to "
                 "make a prediction-model. This model is able to, given a set of answers, predict the time it "
                 "will take you to fal asleep*.")
        st.caption("*While testing the used AI model, it scored an accuracy of 84% on the answers from the volunteers. "
                   "This however does not mean that it's prediction is perfect. The time it will take you to fall "
                   "asleep is affected by your caffeine intake, but not limited to it. This time is also affected "
                   "by stress levels, melatonin production, temperature, etc. If you don't consume any caffeine "
                   "and still have trouble falling asleep, please consider contacting a licensed doctor.")

    st.write("")
    st.write("")
    st.button("Start form", on_click=switch_to_questionair)


# ========================================= Questionnaire page ====================================
def questionair():
    # -------------------------------- Switching pages --------------------------------
    def switch_to_results():
        st.session_state["page"] = "results"

    # -------------------------------- UI --------------------------------
    st.title('Questionnaire')

    form = st.form("Caffeine intake")
    with form:
        st.subheader('Caffeine intake')
        st.markdown(
            'How many caffeine holding products you you consume and when? For instance coffee and energy drink, '
            'but this also includes preworkout, chocolate and some thea as they can also hold caffeine.')
        st.write('')

    hoeveel_per_dag = form.radio("How many caffeine holding products do you consume per day?",
                                 ('None', '1 to 2 per day', '3 to 4 per day', '5 to 6 per day', 'More than 6 per day'))

    def categorise_hoeveel(hoeveel_per_dag):
        if hoeveel_per_dag == "None":
            return 0
        elif hoeveel_per_dag == "1 to 2 per day":
            return 1
        elif hoeveel_per_dag == "3 to 4 per day":
            return 3
        elif hoeveel_per_dag == "5 to 6 per day":
            return 5
        elif hoeveel_per_dag == "More than 6 per day":
            return 7

    st.session_state.hoeveel = categorise_hoeveel(hoeveel_per_dag)

    wanneer_laatste = form.radio("When do you usually have your last caffeine holding product of the day?",
                                 ('Before or during lunch', 'Between 15:00 and 17:00', 'Between 17:00 and 19:00',
                                  'Between 19:00 and 21:00',
                                  'Between 21:00 and 23:00', 'After 23:00'))

    def categorise_wanneer(wanneer):
        if wanneer == "Before or during lunch":
            return 0
        elif wanneer == "Between 15:00 and 17:00":
            return 15
        elif wanneer == "Between 17:00 and 19:00":
            return 17
        elif wanneer == "Between 19:00 and 21:00":
            return 19
        elif wanneer == "Between 21:00 and 23:00":
            return 21
        elif wanneer == "After 23:00":
            return 23

    st.session_state["data"]["wanneer"] = [categorise_wanneer(wanneer_laatste)]

    with form:
        st.write('')
        st.subheader('Sleeping')
        st.write('Let us find out about your sleeping schedule.')

        laat_bed = form.radio("At what time do you usually go to bed?",
                              ('Between 21:00 and 22:00', 'Between 22:00 and 23:00', 'Between 23:00 and 00:00',
                               'Between 00:00 and 02:00',
                               'Between 02:00 and 04:00'))

        def categorise_laat(laat):
            if laat == "Between 21:00 and 22:00":
                return 21
            elif laat == "Between 22:00 and 23:00":
                return 22
            elif laat == "Between 23:00 and 00:00":
                return 23
            elif laat == "Between 00:00 and 02:00":
                return 24
            elif laat == "Between 02:00 and 04:00":
                return 26

        st.session_state["data"]["laat"] = [categorise_laat(laat_bed)]

        st.write("")
        st.write("")
        # Add a submit button to the form:
        st.form_submit_button("Save")

    st.write("")
    st.write("")
    st.button("Predict estimated time to fall asleep", on_click=switch_to_results)


# ========================================= Resultaat pagina =========================================
def results():
    st.session_state.resultsReady = True

    # -------------------------------- Switching pages --------------------------------
    def switch_to_questionair():
        st.session_state["page"] = "questionair"
        del st.session_state.resultsReady

    def switch_to_welcome():
        st.session_state["page"] = "welcome"

    # -------------------------------- UI --------------------------------
    st.title("Results")

    # ------------- Fetching model and predicting -------------
    df = pd.DataFrame(st.session_state["data"])
    model = fetch_model()
    prediction = model.predict(df)

    result_numbers = pd.DataFrame(prediction[0])
    result_numbers = result_numbers.values.tolist()
    max_pred = max(result_numbers)

    # ------------- Instantiating big result subheader -------------
    big_result = st.container()

    # ------------- Composing result paragraph -------------
    story1 = "The Artificial Intelligence has determined that you will most likely fall asleep "
    resultstring = ""
    story2 = "based on your chosen caffeine intake."
    conclusion = ""

    if max_pred == result_numbers[0]:
        resultstring = "in less than 10 minutes"
        conclusion = "Which is absolutely great, that means that you don't consume any caffeine too close to bedtime!"
        st.write(story1, resultstring, story2, conclusion)
        max_pred = result_numbers[0][0]
        category = 0

    elif max_pred == result_numbers[1]:
        resultstring = "between 10 and 30 minutes"
        conclusion = "Which is not that bad, but there is some room for improvement regarding your caffeine intake."
        st.write(story1, resultstring, story2, conclusion)
        max_pred = result_numbers[1][0]
        category = 1

    elif max_pred == result_numbers[2]:
        resultstring = "between 30 minutes and 1 hour"
        conclusion = "Which is not desirable, you most likely consume caffeine right before you go to bed, there is" \
                     "definitely room for improvement regarding your caffeine intake."
        st.write(story1, resultstring, story2, conclusion)
        max_pred = result_numbers[2][0]
        category = 2

    elif max_pred == result_numbers[3]:
        resultstring = "after more than 1 hour"
        conclusion = "It must be dreadful to have to lay awake for so long, wondering why you can't" \
                     " catch some sleep. You would most likely benefit from a change in your caffeine intake, " \
                     "below are some tips."
        st.write(story1, resultstring, story2, conclusion)
        max_pred = result_numbers[3][0]
        category = 3

    else:
        st.write("We are sorry, an error has occurred, please refresh the page and try again, if the error persists, "
                 "click *report a bug* in the menu on the top right "
                 "corner of your screen to email support. Please include the following error: ")
        st.write(">ERROR: MAX_PRED != RESULT")
        category = 99
        st.stop()

    # ------------- Filling in big result subheader -------------
    big_result_string = "You will most likely fall asleep " + resultstring
    big_result.subheader(big_result_string)

    # ------------- Certainty progress bar -------------
    st.write(f"{(int(max_pred * 100))}%", " certainty")
    st.progress(int(max_pred * 100))
    st.write("See the *Explanation* paragraph for more information about the certainty of the AI.", ':point_down:')
    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: green;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    # ------------- Tips Paragraph composing -------------
    st.subheader("Tips")
    if category == 0:
        st.write("You are doing amazing at not consuming any caffeine before bed, keep up the good work!")
    elif category == 1:
        st.write("You are having almost no caffeine before bed, but at the times you are consuming it, it might"
                 " still be affecting the duration until you fall asleep. Therefore you might consider"
                 " consuming your products earlier, or better yet, not consume them at all.")
    elif category == 2:
        st.write("You are having caffeine close to bed, which is very likely to be affecting your sleep. "
                 "Therefore you might consider consuming your products earlier, or better yet, "
                 "not consume them at all. ")
    elif category == 3:
        st.write("You consume caffeine right before going to bed, maybe a bar of chocolate or you go to the gym "
                 "at night and use preworkout there. This is heavily affecting your sleep, it is recommended you "
                 "stop consuming caffeine before bed. Try to drink a glass of water instead as during the night "
                 "you are losing moisture from your body. Preventing dehydration and good sleep quality "
                 "ups your energy levels during the day. Up to a point where you might not even need caffeine at "
                 "all to stay awake! Good luck!")

    if st.session_state.hoeveel > 2:
        st.write("You are however consuming more than 2 products with caffeine per day, and could"
                 " consider reducing your overall caffeine intake.")
    elif st.session_state.hoeveel == 0:
        st.write("You don't consume any caffeine, that's very good of you and healthy, keep it up!")
    else:
        st.write("You are having 2 or less caffeine holding products per day, quite good!")

    # ------------- Explanation Paragraph composing -------------
    st.subheader("Explanation")
    st.write("The Artificial Intelligence (AI) works based on a percentage of certainty, these percentages are "
             "displayed below.")
    st.write("")

    less, ten, thirty, hour = st.columns([1, 1, 1, 1])

    with less:
        st.write("**Less than 10min**")
        st.write("The AI thinks for ", f"{(int(result_numbers[0][0] * 100))}%", " that you fall in this category.")
        st.write(f"{(int(result_numbers[0][0] * 100))}%")
        st.progress(int(result_numbers[0][0] * 100))

    with ten:
        st.write("**Between 10 and 30mins**")
        st.write("The AI thinks for ", f"{(int(result_numbers[1][0] * 100))}%", " that you fall in this category.")
        st.write(f"{(int(result_numbers[1][0] * 100))}%")
        st.progress(int(result_numbers[1][0] * 100))

    with thirty:
        st.write("**Between 30mins and 1h**")
        st.write("The AI thinks for ", f"{(int(result_numbers[2][0] * 100))}%", " that you fall in this category.")
        st.write(f"{(int(result_numbers[2][0] * 100))}%")
        st.progress(int(result_numbers[2][0] * 100))

    with hour:
        st.write("**More than 1h**")
        st.write("The AI thinks for ", f"{(int(result_numbers[3][0] * 100))}%", " that you fall in this category.")
        st.write(f"{(int(result_numbers[3][0] * 100))}%")
        st.progress(int(result_numbers[3][0] * 100))

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")



    # ------------- Thank you and buttons -------------
    empty1, middle, empty2 = st.columns([1, 2, 1])
    middle.subheader("Thanks for using this AI!")

    left, buff, right = st.columns([2, 1, 2])
    with left:
        st.button("Fill the questionnaire in again", on_click=switch_to_questionair)

    with right:
        st.button("Back to welcome screen", on_click=switch_to_welcome)

    st.caption("The results and tips given by this Artificial Intelligence are not medical advice and should not be "
               "treated as such.")


# ========================================= Sidebar =========================================
sidebar = st.sidebar
sidebar.header('Caffeine intake and sleeping')
sidebar.subheader('Switch tabs here')

button_welcome = st.sidebar.button("Welcome")
if button_welcome:
    st.session_state["page"] = "welcome"

button_vragen = st.sidebar.button("Questionnaire")
if button_vragen:
    st.session_state["page"] = "questionair"

if st.session_state.resultsReady is True:
    button_results = st.sidebar.button("Results")
    if button_results:
        st.session_state["page"] = "results"

# ========================================= Switching pages =========================================
pages = {
    "welcome": welcome,
    "questionair": questionair,
    "results": results
}

if "page" not in st.session_state:
    st.session_state["page"] = "welcome"
    st.session_state["data"] = {}

pages[st.session_state["page"]]()
