import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyAvgIy_Ckc8o7aSc4I2NlRBPAFgmksXGVs"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

class Moderator:
    def __init__(self, topic):
        """
        Initialize the Moderator with a debate topic and set up flow tracking.
        """
        self.topic = topic
        self.current_stage = "Opening"
        self.time_limit = 60  # Time limit for each stage in seconds
        self.key_points = []  # Stores important points for summarization
        self.turn = "Pro"     # Tracks which debater's turn it is (Pro or Con)
        self.memory = {
            'pro_debater': [],
            'con_debater': []
        }   # to store the content from the debaters
        self.model = genai.GenerativeModel('gemini-pro')

    def introduce_topic(self):
        """
        Introduce the debate topic and structure.
        """
        intro = f"Welcome to today's debate on the topic: '{self.topic}'. Let's begin with opening statements."
        print(intro)
        return intro

    def manage_turn(self):
        """
        Switches turns between debaters.
        """
        self.turn = "Con" if self.turn == "Pro" else "Pro"
        return f"It's now {self.turn} debater's turn."

    def allocate_time(self):
        """
        Allocate time for each debater's turn. Placeholder for timing logic.
        """
        print(f"{self.turn} debater has {self.time_limit} seconds.")
        time.sleep(2)  # Simulate timing with a short sleep
        return f"{self.turn} debater's time is up."

    def pose_question(self, statement):
        """
        Pose a question to both debaters to encourage deeper discussion.
        """
        prompt = f"Based on the following statement by the debater: [{statement}], pose a single sentence question to the debater."
        question = self.model.generate_content(prompt).text
        #print(f"Moderator: {question}")
        return question

    def intervene(self, statement):
        """
        Intervene if a debater goes off-topic or repeats points.
        """
        intervention = f"Moderator: Let's keep the discussion focused on new points relevant to '{self.topic}'."
        print(intervention)
        return intervention

    def summarize_debate(self):
        """
        Provide a summary of key points raised so far.
        """
        summary = "In summary, we’ve covered the following key points:\n" + "\n".join(self.key_points)
        print(f"Moderator: {summary}")
        return summary

    def add_key_point(self, point):
        """
        Add a key point from the debate for future summarization.
        """
        self.key_points.append(point)

    def finalize_debate(self):
        """
        Conclude the debate with final remarks.
        """
        conclusion = f"Thank you both for an engaging debate. That concludes our session on '{self.topic}'."
        print(conclusion)
        return conclusion

    def decide_winner(self, memory):
        prompt = f"The following is the debate content from each debater-        {list(self.memory.keys())[0]}:    {self.memory[list(self.memory.keys())[0]]},        {list(self.memory.keys())[1]}:    {self.memory[list(self.memory.keys())[1]]}. From this content, decide a winner."
        result = self.model.generate_content(prompt).text
        return result
