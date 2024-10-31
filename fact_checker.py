
import json
import random

class FactChecker:
    def __init__(self, fact_db_path, misconceptions_path):
        """
        Initialize the FactChecker with a database of facts and misconceptions.
        """
        # Load verified facts and misconceptions from JSON files
        with open(fact_db_path, 'r') as f:
            self.fact_db = json.load(f)
        with open(misconceptions_path, 'r') as f:
            self.misconceptions = json.load(f)

    def verify_claim(self, claim):
        """
        Verify the accuracy of a given claim by comparing it to known facts.
        Returns a feedback message and accuracy rating.
        """
        # Check if claim is in the fact database
        if claim in self.fact_db:
            return f"The claim '{claim}' is accurate.", "accurate"
        
        # Check if claim is a common misconception
        if claim in self.misconceptions:
            correct_fact = self.misconceptions[claim]
            return f"The claim '{claim}' is inaccurate. Correct information: {correct_fact}", "inaccurate"
        
        # If claim is not found, mark as uncertain
        return f"The accuracy of the claim '{claim}' cannot be verified.", "uncertain"

    def provide_feedback(self, debater_statement):
        """
        Extract and verify claims from a debater's statement, providing feedback.
        """
        # This is a placeholder for claim extraction logic.
        # Assume statements are split by punctuation for simplicity.
        claims = debater_statement.split('. ')
        
        feedback = []
        for claim in claims:
            if claim:  # Ignore empty claims
                verification_result, rating = self.verify_claim(claim)
                feedback.append((claim, verification_result, rating))
        
        return feedback

    def add_to_fact_db(self, new_fact):
        """
        Add a new verified fact to the database (simulating learning).
        """
        self.fact_db[new_fact] = "verified"
        # Here, you would save the updated fact_db back to a file if needed.

