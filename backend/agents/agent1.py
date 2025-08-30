import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = LLM(model="gpt-5-mini")

query_classifier_agent = Agent(
    role="Question Answering Chatbot",
    goal="Provide accurate, concise answers to user question: {question}",
    backstory="You serve as a reliable guide to help users navigate information overload and find trustworthy answers.",
    tools=[],
    llm=llm
)


qa_task = Task(
    description="Answer the user’s question, ensuring clarity, accuracy, and relevance.",
    expected_output="A clear and concise answer addressing the user's question with supporting details if necessary.",
    agent=query_classifier_agent
)

crew = Crew(
    agents=[query_classifier_agent],
    tasks=[qa_task],
    verbose=True 
)

result = crew.kickoff(inputs={'question': 'I have chest pain what should I do?'})
print(result)

