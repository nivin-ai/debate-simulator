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
        if self.position in ['Pro', 'pro']:
            prompt = f"Provide an opening statement supporting the topic: {topic}."
        else:
            prompt = f"Provide an opening statement against the topic: {topic}."
        response = self.model(prompt, max_length=100, do_sample=True)
        opening_statement = response[0]['generated_text']
        self.memory.append(opening_statement)
        return opening_statement

    def generate_main_argument(self, topic, previous_points=[]):
        """
        Generate a main argument considering previous points (for coherence).
        """
        if self.position in ['Pro', 'pro']:
            prompt = f"Supporting the topic {topic}, build upon the previous points: {', '.join(previous_points)}"
        else:
            prompt = f"Going against the topic {topic}, build upon the previous points: {', '.join(previous_points)}"
        response = self.model(prompt, max_length=250, do_sample=True)
        main_argument = response[0]['generated_text']
        self.memory.append(main_argument)
        return main_argument

    def generate_rebuttal(self, topic, opponent_points):
        """
        Generate a rebuttal based on the opponent's points.
        """
        if self.position in ['Pro', 'pro']:
            prompt = f"Supporting the topic {topic}, oppose the following points: {', '.join(opponent_points)}."
        else:
            prompt = f"Going against the topic {topic}, oppose the following points: {', '.join(opponent_points)}."
        response = self.model(prompt, max_length=75, do_sample=True)
        rebuttal = response[0]['generated_text']
        self.memory.append(rebuttal)
        return rebuttal

    def generate_closing_statement(self, topic):
        """
        Generate a closing statement that summarizes the debater's position.
        """
        if self.position in ['pro' ,'Pro']:
            prompt = f"Supporting the topic {topic}, provide a closing statement summarizing your arguments."
        else:
            prompt = f"Going against the topic {topic}, provide a closing statement summarizing your arguments."
        response = self.model(prompt, max_length=50, do_sample=True)
        closing_statement = response[0]['generated_text']
        self.memory.append(closing_statement)
        return closing_statement
