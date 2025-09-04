import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tools 
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = LLM(model="gpt-5-mini", temperature=0.3) 


query_classifier_agent = Agent(
    role="Query Parser and Intent Classifier",
    goal="Accurately parse user queries related to common healthcare problems, classify their intent, and prepare data for routing to appropriate agents while ensuring security and ethical considerations: {question}",
    backstory="You are a highly skilled AI assistant in a healthcare support system, trained to interpret patient queries with precision. With a background in natural language processing and large language models, you act as the first point of contact, breaking down complex queries into actionable insights while safeguarding user privacy and ensuring fair, transparent responses.",
    tools=[],
    llm=llm
)


query_classifier_task = Task(
    description="Parse the user’s healthcare-related query by extracting entities (e.g., symptoms, dates, persons) using NLP, classify the intent (e.g., symptom triage, appointment booking) using the LLM, sanitize the input for security, and determine the next action (e.g., direct response or routing to another agent). Ensure the process is logged for transparency and checked for fairness.",
    expected_output="A structured response containing the parsed entities (e.g., {'symptoms': ['chest pain'], 'dates': ['tomorrow']}), the classified intent with a brief reason (e.g., 'symptom_triage: Reason - Query mentions a symptom'), a sanitized summary of the query, and an action decision (e.g., 'direct_response' with a general answer or 'route_to_retrieval' with data for another agent).",
    agent=query_classifier_agent
)

crew = Crew(
    agents=[query_classifier_agent],
    tasks=[query_classifier_task],
    verbose=True 
)

result = crew.kickoff(inputs={'question': 'I have chest pain what should I do?'})
print(result)