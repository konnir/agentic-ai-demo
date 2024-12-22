import random

class SimpleAgent:
    def __init__(self, name, goals):
        self.name = name
        self.goals = goals

    def perceive(self, environment):
        """
        Simulate gathering data from environment.
        Here, environment might be a simple list or other structure.
        """
        # For demonstration, return a random element or None
        return random.choice(environment) if environment else None

    def decide_action(self, perception):
        """
        Decide an action based on the perception and the agent's goals.
        """
        if perception == "threat":
            return "defend"
        elif perception == "opportunity":
            return "attack"
        else:
            return "wait"

    def act(self, action):
        """
        Execute the chosen action. In a real system, this might mean
        sending requests or controlling hardware.
        """
        print(f"{self.name} performs action: {action}")

# Example usage
if __name__ == "__main__":
    environment = ["opportunity", "threat", "nothing", "opportunity"]
    agent_goals = ["stay safe", "maximize reward"]

    agent = SimpleAgent("AgenticAI", agent_goals)

    for step in range(5):
        perceived = agent.perceive(environment)
        print(f"{agent.name} perceives: {perceived}")
        action = agent.decide_action(perceived)
        agent.act(action)