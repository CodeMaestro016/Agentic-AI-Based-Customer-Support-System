import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
# from crewai.tools import tools 
from langchain_openai import ChatOpenAI


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# define the query Handler Agent
query_handler_agent = Agent(
    role="Query Handler Agent",
    goal="Handle patient queries about symptoms by providing brief details and recommended actions, while emphasizing that this is not professional medical advice and advising to consult a doctor.",
    backstory=(
        "You are an AI assistant specialized in customer support for medical systems. "
        "Your expertise helps users navigate questions about symptoms related to medical devices or general health inquiries. "
        "Always respond empathetically, keep answers concise, and direct users to seek professional medical help for accurate diagnosis."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
    tools=[]
)

task = Task(
    description=("The patient query is: {patient_query}. "
        "Respond with brief details about the symptom, what actions to take, and remind to consult a professional."
    ),
    expected_output="A concise response including symptom details, recommended actions, and a disclaimer.",
    agent=query_handler_agent
)

# create a crew
crew = Crew(
    agents=[query_handler_agent],
    tasks=[task],
    verbose=True  # Detailed logging
)

# Example usage: Kick off the crew with a sample input
result = crew.kickoff(inputs={"patient_query": "I have a headache and feel dizzy. What should I do?"})

print(result)









