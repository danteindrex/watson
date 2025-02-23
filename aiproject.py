
from crewai import Agent, Task, Crew,Process,LLM
from crewtools  import auto_move
#from crewtools import auto_move
from multiprocessing import  Process as p
move= auto_move()
def main():
   

    
        

    llm = LLM(
        model="ollama/deepseek-r1:1.5b",
        base_url="http://localhost:11434"
    )



    boss = Agent(
        role="AI manager",
        goal="devise a series of steps and icons required by the info agent to accomplish the given task",
        backstory="you are an AI assistant manager with an agent that is capable of naivagting the user interface by using the auto_move tool to locate an icon or UI element on the user screen",
        llm=llm,
        allow_delegation=True
        
    )
    # Initialize agent
    info_agent = Agent(
        role="AI execute Agent",
        goal="use the auto_move tool to navigate , locate and click on the Icon or element mentioned by ",
        backstory="you are an AI assistant that is capable of naivagting the user interface by using the auto_move tool to locate an icon or UI element on the user screen",
        llm=llm,
        tools=[move]
        
    )

    # Initialize task
    task1 = Task(
        description="locate and reload googel chrome, u can call the tool recurively",
        expected_output="a sucess message after the completion of the task",
        agent=info_agent,
        #human_input=True
    )

    # Debug: Print out parameters before passing them
    #print("Agent:", info_agent)
    #print("Task:", task1)

    # Initialize crew
    crew = Crew(
        agents=[info_agent],
        tasks=[task1],
        verbose=True,
        model="deepseek-r1:1.5b", #<<<<< add model to crew to ensure it uses it
        
        cache=True,
        process=Process.hierarchical,
        manager_agent=boss
        #planning=True, # I see better results with this
        #splanning_llm=llm,

    )

    print("Crew initialized successfully")
    return crew.kickoff()

#def pool_handler():
#    p= Pool(3)
 #   p.imap(main)

if __name__ =='__main__':
    p= p(target=main)
    p.start()
    p.join()
