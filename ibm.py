from crewai import LLM, Agent, Crew, Process, Task 
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
#from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

from script import get_quickbooks_customers, ZD_API_TOKEN,QB_ACCESS_TOKEN,QB_BASE_URL
import os
ZD_API_TOKEN
os.environ("QB_BASE_URL") = QB_BASE_URL
os.environ("QB_ACCESS_TOKEN")= QB_ACCESS_TOKEN

def main():
        quickbooks=  get_quickbooks_customers(QB_ACCESS_TOKEN,QB_BASE_URL)
        # Create a knowledge source
        content_source = JSONKnowledgeSource(
            file_paths=[
                quickbooks
            ],chunk_size=400
        )

        # Create an LLM with a temperature of 0 to ensure deterministic outputs
        llm = LLM(
                model="MODEL=ollama/granite3-moe:3b",
                base_url="http://localhost:11434",
                temperature=0
            )
        boss = Agent(
        role="AI system manager",
        goal="devise a series of steps and icons required by the info agent to accomplish the given task",
        backstory="you are an AI assistant manager with  agents  capable of retriving data and infomation from the different sources provided",
        llm=llm,
        allow_delegation=True)

        # Create an agent with the knowledge store
        financial_agent = Agent(
            role="About finances of the startup",
            goal="You know everything about the finances of the startup.",
            backstory="""You are a master at understanding quickbooks and their content about finances and accounting.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            knowledge_sources=[content_source],
            tools=[quickbooks]
            
        )
        customer_agent = Agent(
            role="About customers of the startup",
            goal="You know everything about the customer complaints and all customer  related issues of the startup.",
            backstory="""You are a master at understanding zendesk and their content about customer relation management.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
        finance_task = Task(
            description="Answer the following financial questions about the buiness in a professional way: {question}",
            expected_output="An answer to the question and some recommendations on actions",
            agent=financial_agent,
        )
        customer_retrival = Task(
            description="Answer the following questions about the customer service division of the buiness in a professional way: {question}",
            expected_output="An answer to the question.",
            agent=customer_agent,
        )

        crew = Crew(
            agents=[financial_agent],
            tasks=[finance_task,customer_retrival],
            verbose=True,
            
            knowledge_sources=[
                content_source
            ],
              manager_agent=boss,
                cache=True,
                process=Process.hierarchical,  # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
        )

        result = crew.kickoff(
            inputs={
                "question": "What is the reward hacking paper about? Be sure to provide sources."
            }
        )
        return result