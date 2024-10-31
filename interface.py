import streamlit as st
from debater import Debater
from fact_checker import FactChecker
from moderator import Moderator

# Page configuration
st.set_page_config(page_title="AI Debate Simulator", layout="centered")

# CSS styling for a Netflix-inspired dark theme
st.markdown(
    """
    <style>
    /* Overall page styling */
    body {
        font-family: "Helvetica Neue", sans-serif;
        color: #FFFFFF;
        background-color: #141414;
    }
    
    /* Title styling */
    .title {
        font-size: 3em;
        font-weight: 700;
        color: #E50914;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Description styling */
    .description {
        font-size: 1.1em;
        font-weight: 400;
        color: #B3B3B3;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Header styling */
    .header {
        font-size: 1.8em;
        font-weight: 600;
        color: #E50914;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: left;
    }

    /* Text input styling */
    input[type="text"] {
        border-radius: 5px;
        border: 1px solid #333;
        padding: 10px;
        width: 100%;
        font-size: 1em;
        color: #FFF;
        background-color: #333;
    }

    /* Subheader styling */
    .subheader {
        font-size: 1.5em;
        font-weight: 600;
        color: #E50914;
        margin-top: 20px;
        border-bottom: 2px solid #E50914;
        padding-bottom: 5px;
        text-align: left;
    }

    /* Fact-Checker feedback styling */
    .feedback {
        margin: 10px 0;
        padding: 15px;
        background-color: #333333;
        border-radius: 5px;
        color: #B3B3B3;
    }

    /* Button styling */
    .stButton>button {
        background-color: #E50914;
        color: white;
        font-weight: bold;
        font-size: 1em;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #B20710;
    }

    /* Debater styling */
    .debater {
        font-weight: 900;
        color: #E50914;
        margin: 10px 0;
        font-size: 1.2em;
    }

    .debater-text {
        font-weight: 400;
        color: #FFFFFF;
        margin: 10px 0;
    }

    /* Debate Topic styling */
    .debate-topic {
        font-weight: bold;
        font-size: 1.3em;
        color: #FFFFFF;
        background-color: #333333;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    
    </style>
    """, unsafe_allow_html=True
)

# Initialize agents
fact_checker = FactChecker('facts_db.json', 'misconceptions.json')
moderator = Moderator("Sample Topic")
pro_debater = Debater("Pro")
con_debater = Debater("Con")

# User input for debate topic
st.markdown("<div class='title'>AI Debate Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>An AI-powered debate simulator. Provide a topic, and watch AI-driven arguments unfold!</div>", unsafe_allow_html=True)
topic = st.text_input("Enter the debate topic:", "The impact of AI on employment")

# Start Debate Button
if st.button("Start Debate"):
    st.markdown("<div class='subheader'>Debate Topic:</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debate-topic'>{topic}</div>", unsafe_allow_html=True)
    moderator.topic = topic
    st.markdown(f"<div class='debater'>Moderator:</div> <div class='debater-text'>{moderator.introduce_topic()}</div>", unsafe_allow_html=True)

    # Opening statements
    st.markdown("<div class='subheader'>Opening Statements</div>", unsafe_allow_html=True)
    pro_opening = pro_debater.generate_opening_statement(topic)
    con_opening = con_debater.generate_opening_statement(topic)
    st.markdown(f"<div class='debater'>Pro Debater:</div> <div class='debater-text'>{pro_opening}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater'>Con Debater:</div> <div class='debater-text'>{con_opening}</div>", unsafe_allow_html=True)

    # Main Arguments
    st.markdown("<div class='subheader'>Main Arguments</div>", unsafe_allow_html=True)
    pro_argument = pro_debater.generate_main_argument(topic)
    st.markdown(f"<div class='debater'>Pro Debater's Argument:</div> <div class='debater-text'>{pro_argument}</div>", unsafe_allow_html=True)

    con_rebuttal = con_debater.generate_rebuttal(topic, pro_argument)
    st.markdown(f"<div class='debater'>Con Debater's Rebuttal:</div> <div class='debater-text'>{con_rebuttal}</div>", unsafe_allow_html=True)
    
    # Pro Debater's Feedback
    st.markdown("<div class='subheader'>Fact-Checker Feedback for Pro Debater:</div>", unsafe_allow_html=True)
    for claim, message, rating in fact_checker.provide_feedback(pro_argument):
        st.markdown(f"<div class='feedback'><div class='debater'>Claim:</div> <div class='debater-text'>{claim}</div> <div class='debater-text'>{message}</div> <div class='debater-text'>Rating: {rating}</div></div>", unsafe_allow_html=True)

    con_argument = con_debater.generate_main_argument(topic)
    st.markdown(f"<div class='debater'>Con Debater's Argument:</div> <div class='debater-text'>{con_argument}</div>", unsafe_allow_html=True)
    
    pro_rebuttal = pro_debater.generate_rebuttal(topic, con_argument)
    st.markdown(f"<div class='debater'>Pro Debater's Rebuttal:</div> <div class='debater-text'>{pro_rebuttal}</div>", unsafe_allow_html=True)
    
    # Con debater's feedback
    st.markdown("<div class='subheader'>Fact-Checker Feedback for Con Debater:</div>", unsafe_allow_html=True)
    for claim, message, rating in fact_checker.provide_feedback(con_argument):
        st.markdown(f"<div class='feedback'><div class='debater'>Claim:</div> <div class='debater-text'>{claim}</div> <div class='debater-text'>{message}</div> <div class='debater-text'>Rating: {rating}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='subheader'>Moderator's Interventions</div>", unsafe_allow_html=True)
    moderator.pose_question()
    moderator.add_key_point("Pro Debater's main argument")
    moderator.add_key_point("Con Debater's main argument")
    moderator.summarize_debate()

    st.markdown("<div class='subheader'>Closing Statements</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater'>Pro Debater:</div> <div class='debater-text'>{pro_debater.generate_closing_statement(topic)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater'>Con Debater:</div> <div class='debater-text'>{con_debater.generate_closing_statement(topic)}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='debater'>Moderator:</div> <div class='debater-text'>{moderator.finalize_debate()}</div>", unsafe_allow_html=True)


