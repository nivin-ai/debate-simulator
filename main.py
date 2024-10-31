
from agents.debater import Debater
from agents.fact_checker import FactChecker
from agents.moderator import Moderator

def run_debate(topic):
    # Initialize the agents
    fact_checker = FactChecker('data/facts_db.json', 'data/misconceptions.json')
    moderator = Moderator(topic)
    pro_debater = Debater("Pro")
    con_debater = Debater("Con")

    # Debate Introduction
    print(moderator.introduce_topic())

    # Opening Statements
    print("\nOpening Statements:")
    pro_opening = pro_debater.generate_opening_statement(topic)
    print(f"Pro Debater: {pro_opening}")

    con_opening = con_debater.generate_opening_statement(topic)
    print(f"Con Debater: {con_opening}")

    # Main Arguments with Fact-Checker Feedback
    print("\nMain Arguments:")
    pro_argument = pro_debater.generate_main_argument()
    print(f"Pro Debater's Argument: {pro_argument}")
    
    # Fact-Checker Feedback
    pro_feedback = fact_checker.provide_feedback(pro_argument)
    print("Fact-Checker Feedback for Pro Debater:")
    for claim, message, rating in pro_feedback:
        print(f"Claim: {claim} - {message} (Rating: {rating})")

    con_argument = con_debater.generate_main_argument()
    print(f"Con Debater's Argument: {con_argument}")
    
    # Fact-Checker Feedback
    con_feedback = fact_checker.provide_feedback(con_argument)
    print("Fact-Checker Feedback for Con Debater:")
    for claim, message, rating in con_feedback:
        print(f"Claim: {claim} - {message} (Rating: {rating})")

    # Moderator Summary and Question
    print("\nModerator's Interventions:")
    print(moderator.pose_question())
    moderator.add_key_point(pro_argument)
    moderator.add_key_point(con_argument)
    print(moderator.summarize_debate())

    # Rebuttals
    print("\nRebuttals:")
    pro_rebuttal = pro_debater.generate_rebuttal([con_argument])
    print(f"Pro Debater's Rebuttal: {pro_rebuttal}")

    con_rebuttal = con_debater.generate_rebuttal([pro_argument])
    print(f"Con Debater's Rebuttal: {con_rebuttal}")

    # Closing Statements
    print("\nClosing Statements:")
    pro_closing = pro_debater.generate_closing_statement()
    print(f"Pro Debater: {pro_closing}")

    con_closing = con_debater.generate_closing_statement()
    print(f"Con Debater: {con_closing}")

    # Final remarks
    print("\nModerator's Final Remarks:")
    print(moderator.finalize_debate())

# Running the debate with a sample topic
if __name__ == "__main__":
    run_debate("The impact of AI on employment")
