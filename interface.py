
import streamlit as st
from streamlit import markdown

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
        margin: 10px 0;
        padding: 10px;
        background-color: #F0F8FF;
        border-left: 5px solid #007ACC;
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
    .debater-text {
        font-weight: 500;
        color: #333;
        margin: 10px 0;
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
st.markdown("<div class='header'>This is an AI-driven debate simulator. Give in any topic of your choice and witness two AI bots face off!</div>", unsafe_allow_html=True)
topic = st.text_input("Enter the debate topic:", "The impact of AI on employment")

# Start Debate Button
if st.button("Start Debate"):
    st.markdown("<div class='header'>Debate Topic:</div>", unsafe_allow_html=True)
    st.write(topic)
    moderator.topic = topic
    moderator.introduce_topic()

    # Opening statements
    st.markdown("<div class='subheader'>Opening Statements</div>", unsafe_allow_html=True)
    pro_opening = pro_debater.generate_opening_statement(topic)
    con_opening = con_debater.generate_opening_statement(topic)
    st.markdown(f"<div class='debater-text'>**Pro Debater:** {pro_opening}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater-text'>**Con Debater:** {con_opening}</div>", unsafe_allow_html=True)

    # Main Arguments
    st.markdown("<div class='subheader'>Main Arguments</div>", unsafe_allow_html=True)
    pro_argument = pro_debater.generate_main_argument()
    st.markdown(f"<div class='debater-text'>**Pro Debater's Argument:** {pro_argument}</div>", unsafe_allow_html=True)

    # Fact-Checker Feedback for Pro's Argument
    pro_feedback = fact_checker.provide_feedback(pro_argument)
    st.markdown("<div class='subheader'>Fact-Checker Feedback for Pro Debater:</div>", unsafe_allow_html=True)
    for claim, message, rating in pro_feedback:
        st.markdown(
            f"<div class='feedback'>**Claim:** {claim} - {message} (Rating: {rating})</div>",
            unsafe_allow_html=True
        )

    con_argument = con_debater.generate_main_argument()
    st.markdown(f"<div class='debater-text'>**Con Debater's Argument:** {con_argument}</div>", unsafe_allow_html=True)

    # Fact-Checker Feedback for Con's Argument
    con_feedback = fact_checker.provide_feedback(con_argument)
    st.markdown("<div class='subheader'>Fact-Checker Feedback for Con Debater:</div>", unsafe_allow_html=True)
    for claim, message, rating in con_feedback:
        st.markdown(
            f"<div class='feedback'>**Claim:** {claim} - {message} (Rating: {rating})</div>",
            unsafe_allow_html=True
        )

    # Moderator's intervention and summary
    st.markdown("<div class='subheader'>Moderator's Interventions</div>", unsafe_allow_html=True)
    moderator.pose_question()
    moderator.add_key_point("Pro Debater's main argument")
    moderator.add_key_point("Con Debater's main argument")
    moderator.summarize_debate()

    # Closing Statements
    st.markdown("<div class='subheader'>Closing Statements</div>", unsafe_allow_html=True)
    pro_closing = pro_debater.generate_closing_statement()
    con_closing = con_debater.generate_closing_statement()
    st.markdown(f"<div class='debater-text'>**Pro Debater:** {pro_closing}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='debater-text'>**Con Debater:** {con_closing}</div>", unsafe_allow_html=True)

    # Final remarks
    moderator.finalize_debate()
