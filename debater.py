from transformers import pipeline

class Debater:
    def __init__(self, position):
        """
        Initialize the Debater with a specific position (e.g., 'Pro' or 'Con').
        """
        self.position = position
        self.memory = []  # Stores arguments and key points
        self.model = pipeline("text2text-generation", model="google/flan-t5-small")  # Using GPT-2

    def generate_opening_statement(self, topic):
        """
        Generate an opening statement based on the debate topic and position.
        """
        if self.position == 'Pro':
            prompt = f"Provide an opening statement for a debate supporting the topic: {topic}."
        else:
            prompt = f"Provide an opening statement for a debate against the topic: {topic}."
        response = self.model(prompt, max_length=100, do_sample=True)
        opening_statement = response[0]['generated_text']
        self.memory.append(opening_statement)
        return opening_statement

    def generate_main_argument(self, previous_points=[]):
        """
        Generate a main argument considering previous points (for coherence).
        """
        prompt = f"As a {self.position} debater, build upon the previous points: {', '.join(previous_points)}"
        response = self.model(prompt, max_length=250, do_sample=True)
        main_argument = response[0]['generated_text']
        self.memory.append(main_argument)
        return main_argument

    def generate_rebuttal(self, opponent_points):
        """
        Generate a rebuttal based on the opponent's points.
        """
        prompt = f"As a {self.position} debater, oppose the following points: {', '.join(opponent_points)}."
        response = self.model(prompt, max_length=75, do_sample=True)
        rebuttal = response[0]['generated_text']
        self.memory.append(rebuttal)
        return rebuttal

    def generate_closing_statement(self):
        """
        Generate a closing statement that summarizes the debater's position.
        """
        prompt = f"As a {self.position} debater, provide a closing statement summarizing your arguments."
        response = self.model(prompt, max_length=50, do_sample=True)
        closing_statement = response[0]['generated_text']
        self.memory.append(closing_statement)
        return closing_statement
