########
# Main #
########


from graph import build_graph
from agent_state import create_initial_state
from agent_registry import register_agent, get_agent
from email_agent import email_agent


def main():

    """
    This function serves as the main entry point for the knowledge agent.
    It builds the state graph, initializes the agent state, and runs the agent.
    After obtaining the final answer, it prompts the user to optionally email the answer.
    """

    # Research Agent
    ################

    # register agents
    register_agent("email", email_agent)

    # ask user for question
    question = input("Question: ")

    # build graph and initial state
    graph = build_graph()
    state = create_initial_state(question)

    # run knowledge agent graph
    result = graph.invoke(state, config={"return_state": True})

    # Print final answer and trace
    print("\n=== ANSWER ===\n")
    answer = result["current_answer"]
    
    # if no answer found --> inform user
    if answer is None:
        print("No confident answer could be determined.")
    # else --> print answer
    else:
        print(answer)

    # Print agent trace
    print("\n=== AGENT TRACE ===\n")
    print(" → ".join(result["trace"]))


    # Email Agent activation
    ########################

    # if answer exists, ask user if they want it emailed
    if answer:
        send_mail = input("\nDo you want this answer emailed to you? (yes/no): ").strip().lower()

        # Send email if user requested it
        if send_mail == "yes":
            email = input("Enter your email address: ").strip()

            email_agent_fn = get_agent("email")

            email_state = {
                "recipient": email,
                "subject": "Your 3DEXPERIENCE Answer",
                "body": answer,
                "done": False,
            }

            email_agent_fn(email_state)

            print("\nEmail sent successfully.")
        else:
            print("\nOkay, no Email has been sent.")

    print("\nThanks for using the agent!")


# Run the main function
if __name__ == "__main__":
    main()


