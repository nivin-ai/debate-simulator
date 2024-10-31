import streamlit as st
from debater import Debater
from fact_checker import FactChecker
from moderator import Moderator

# Page configuration
st.set_page_config(page_title="AI Debate Simulator", layout="centered")

# CSS styling for enhanced appearance
st.markdown(
    """
    <style>
    /* Overall page styling */
    body {
        font-family: "Arial", sans-serif;
        color: #333;
        background-color: #F5F5F5;
    }
    
    /* Title styling */
    .title {
        font-size: 2.5em;
        font-weight: 700;
        color: #333399;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Subtle description styling */
    .description {
        font-size: 1em;
        font-weight: 400;
        color: #666;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Header styling */
    .header {
        font-size: 1.5em;
        font-weight: 600;
        color: #333399;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }

    /* Text input styling */
    input[type="text"] {
        border-radius: 5px;
        border: 1px solid #333399;
        padding: 10px;
        width: 100%;
        font-size: 1em;
        color: #333;
        background-color: #EFEFEF;
    }
    
    /* Section subheaders */
    .subheader {
        font-size: 1.3em;
        font-weight: 600;
        color: #333399;
        margin-top: 20px;
        border-bottom: 2px solid #333399;
        padding-bottom: 5px;
    }

    /* Fact-Checker feedback styling */
    .feedback {
        padding: 10px;
        background-color: #F0F8FF;
        border-left: 5px solid #007ACC;
        font-size: 0.9em;
    }

    /* Button styling */
    .stButton>button {
        background-color: #333399;
        color: white;
        font-weight: bold;
        font-size: 1em;
        padding: 8px 20px;
        border-radius: 5px;
        border: 1px solid #333399;
    }

    /* Moderator and debater styling */
    .debater {
        font-weight: 900;
        color: #333;
        margin: 10px 0;
    }
    .debater-text {
        font-weight: 500;
        color: #333;
        margin: 10px 0;
    }

    /* Debate Topic styling */
    .debate-topic {
        font-weight: bold;
        font-size: 1.2em;
        color: #333399;
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
st.markdown("<div class='description'>This is an AI-driven debate simulator. Provide a topic, and watch two AI bots face off!</div>", unsafe_allow_html=True)
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

    # Main Arguments with Fact-Checker Feedback
    st.markdown("<div class='subheader'>Main Arguments</div>", unsafe_allow_html=True)
    
    # Pro Debater's Argument and Fact-Checker Feedback
    pro_argument = pro_debater.generate_main_argument(topic)
    st.markdown(f"<div class='debater'>Pro Debater's Argument:</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='debater-text'>{pro_argument}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='subheader'>Fact-Checker Feedback</div>", unsafe_allow_html=True)
        for claim, message, rating in fact_checker.provide_feedback(pro_argument):
            st.markdown(f"<div class='feedback'>Claim: {claim} - \n{message} \n(Rating: {rating})</div>",unsafe_allow_html=True)

    # Con Debater's Argument and Fact-Checker Feedback
    con_argument = con_debater.generate_main_argument(topic)
    st.markdown(f"<div class='debater'>Con Debater's Argument:</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='debater-text'>{con_argument}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='subheader'>Fact-Checker Feedback</div>", unsafe_allow_html=True)
        for claim, message, rating in fact_checker.provide_feedback(con_argument):
            st.markdown(f"<div class='feedback'>Claim: {claim} - \n{message} \n(Rating: {rating})</div>",unsafe_allow_html=True)

    # Rebuttals
    st.markdown("<div class='subheader'>Rebuttals</div>", unsafe_allow_html=True)
    pro_rebuttal = pro_debater.generate_rebuttal(topic, con_argument)
    st.markdown(f"<div class='debater'>Pro Debater's Rebuttal:</div> <div class='debater-text'>{pro_rebuttal}</div>", unsafe_allow_html=True)

    con_rebuttal = con_debater.generate_rebuttal(topic, pro_argument)
    st.markdown(f"<div class='debater'>Con Debater's Rebuttal:</div> <div class='debater-text'>{con_rebuttal}</div>", unsafe_allow_html=True)
    
    # Closing Statements
    st.markdown("<div class='subheader'>Closing Statements</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater'>Pro Debater:</div> <div class='debater-text'>{pro_debater.generate_closing_statement(topic)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater'>Con Debater:</div> <div class='debater-text'>{con_debater.generate_closing_statement(topic)}</div>", unsafe_allow_html=True)

    # Moderator's Final Remarks
    st.markdown(f"<div class='debater'>Moderator:</div> <div class='debater-text'>{moderator.finalize_debate()}</div>", unsafe_allow_html=True)

