import streamlit as st
from debater import Debater
from fact_checker import FactChecker
from moderator import Moderator

# Page configuration
st.set_page_config(page_title="AI Debate Simulator", layout="centered")

# CSS styling with unique background colors for each speaker
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
    
    /* Description styling */
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

    /* Unique background colors for each debater */
    .moderator {
        font-weight: 900;
        color: #333;
        margin: 10px 0;
        background-color: #FFEFD5; /* Pastel peach for Moderator */
        padding: 10px;
        border-radius: 8px;
    }
    .moderator-text {
        font-weight: 500;
        color: #333;
        margin: 10px 0;
        background-color: #FFEFD5; /* Pastel peach for Moderator */
    }
    
    .pro-debater {
        font-weight: 900;
        color: #333;
        margin: 10px 0;
        background-color: #B3E5FC; /* Pastel blue for Pro Debater */
        padding: 10px;
        border-radius: 8px;
    }
    .pro-debater-text {
        font-weight: 500;
        color: #333;
        margin: 10px 0;
        background-color: #B3E5FC; /* Pastel blue for Pro Debater */
    }
    
    .con-debater {
        font-weight: 900;
        color: #333;
        margin: 10px 0;
        background-color: #C8E6C9; /* Pastel green for Con Debater */
        padding: 10px;
        border-radius: 8px;
    }
    .con-debater-text {
        font-weight: 500;
        color: #333;
        margin: 10px 0;
        background-color: #C8E6C9; /* Pastel green for Con Debater */
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
    st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{moderator.introduce_topic()}</div>", unsafe_allow_html=True)

    # Opening statements
    st.markdown("<div class='subheader'>Opening Statements</div>", unsafe_allow_html=True)
    
    pro_opening = pro_debater.generate_opening_statement(topic)
    pro_opening_safety = moderator.safety_check(pro_opening)
    if pro_opening_safety == None:
        moderator.memory['pro_debater'] = [pro_opening.text]
        st.markdown(f"<div class='pro-debater'>Pro Debater:</div> <div class='pro-debater-text'>{pro_opening.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{pro_opening_safety}</div>", unsafe_allow_html=True)

    con_opening = con_debater.generate_opening_statement(topic)
    con_opening_safety = moderator.safety_check(con_opening)
    if con_opening_safety == None:
        moderator.memory['con_debater'] = [con_opening.text]
        st.markdown(f"<div class='con-debater'>Con Debater:</div> <div class='con-debater-text'>{con_opening.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{con_opening_safety}</div>", unsafe_allow_html=True)

    # Main Arguments with Fact-Checker Feedback
    st.markdown("<div class='subheader'>Main Arguments</div>", unsafe_allow_html=True)
    pro_argument = pro_debater.generate_main_argument(topic)
    pro_argument_safety = moderator.safety_check(pro_argument)
    if pro_argument_safety == None:
        moderator.memory['pro_debater'].append(pro_argument.text)
        st.markdown(f"<div class='pro-debater'>Pro Debater's Argument:</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<div class='pro-debater-text'>{pro_argument.text}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='subheader'>Fact-Checker Feedback</div>", unsafe_allow_html=True)
            for claim, message, rating in fact_checker.provide_feedback(pro_argument):
                st.markdown(f"<div class='feedback'>{message}<br>Rating: {rating}</div>",unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{pro_argument_safety}</div>", unsafe_allow_html=True)

    # Moderator's question for Pro Debater
    if pro_argument_safety==None:
        pro_question = moderator.pose_question(pro_argument)
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>I would like to pose a question here. {pro_question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pro-debater'>Pro Debater:</div> <div class='pro-debater-text'>{pro_debater.answer_question(pro_question)}</div>", unsafe_allow_html=True)

    # Con Debater's Argument with Fact-Checker Feedback
    con_argument = con_debater.generate_main_argument(topic)
    con_argument_safety = moderator.safety_check(con_argument)
    if con_argument_safety == None:
        moderator.memory['con_debater'].append(con_argument.text)
        st.markdown(f"<div class='con-debater'>Con Debater's Argument:</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<div class='con-debater-text'>{con_argument.text}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='subheader'>Fact-Checker Feedback</div>", unsafe_allow_html=True)
            for claim, message, rating in fact_checker.provide_feedback(con_argument):
                st.markdown(f"<div class='feedback'>{message}<br>Rating: {rating}</div>",unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{con_argument_safety}</div>", unsafe_allow_html=True)

    # Moderator's question for Con Debater
    if con_argument_safety==None:
        con_question = moderator.pose_question(con_argument)
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>I would like to pose a question here. {con_question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='con-debater'>Con Debater:</div> <div class='con-debater-text'>{con_debater.answer_question(con_question)}</div>", unsafe_allow_html=True)

    # Rebuttals
    st.markdown("<div class='subheader'>Rebuttals</div>", unsafe_allow_html=True)
    pro_rebuttal = pro_debater.generate_rebuttal(topic, con_argument.text)
    pro_rebuttal_safety = moderator.safety_check(pro_rebuttal)
    if pro_rebuttal_safety == None:
        moderator.memory['pro_debater'].append(pro_rebuttal.text)
        st.markdown(f"<div class='pro-debater'>Pro Debater's Rebuttal:</div> <div class='pro-debater-text'>{pro_rebuttal.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{pro_rebuttal_safety}</div>", unsafe_allow_html=True)

    con_rebuttal = con_debater.generate_rebuttal(topic, pro_argument.text)
    con_rebuttal_safety = moderator.safety_check(con_rebuttal)
    if con_rebuttal_safety == None:
        moderator.memory['con_debater'].append(con_rebuttal.text)
        st.markdown(f"<div class='con-debater'>Con Debater's Rebuttal:</div> <div class='con-debater-text'>{con_rebuttal.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{con_rebuttal_safety}</div>", unsafe_allow_html=True)

    # Closing Statements
    st.markdown("<div class='subheader'>Closing Statements</div>", unsafe_allow_html=True)
    
    pro_closing = pro_debater.generate_closing_statement(topic)
    st.markdown(type(pro_closing))
    pro_closing_safety = moderator.safety_check(pro_closing)
    if pro_closing_safety == None:
        moderator.memory['pro_debater'].append(pro_closing.text)
        st.markdown(f"<div class='pro-debater'>Pro Debater:</div> <div class='pro-debater-text'>{pro_closing.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{pro_closing_safety}</div>", unsafe_allow_html=True)

    con_closing = con_debater.generate_closing_statement(topic)
    con_closing_safety = moderator.safety_check(con_closing)
    if con_closing_safety == None:
        moderator.memory['con_debater'].append(con_closing.text)
        st.markdown(f"<div class='con-debater'>Con Debater:</div> <div class='con-debater-text'>{con_closing.text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{con_closing_safety}</div>", unsafe_allow_html=True)

    # Moderator's Final Remarks
    st.markdown(f"<div class='moderator'>Moderator:</div> <div class='moderator-text'>{moderator.finalize_debate()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='moderator-text'>{moderator.decide_winner(moderator.memory)}</div>", unsafe_allow_html=True)


    

