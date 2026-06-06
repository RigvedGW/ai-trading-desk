import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from stock_tools import fetch_stock_data

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Brain
gemini_brain = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=api_key,
    max_retries=5
)

def run_trading_firm(ticker_symbol):
    print(f"\n--- Initiating Web Request for {ticker_symbol} ---")
    
    # 1. Define Agents
    ceo_agent = Agent(
        role="Chief Executive Officer (CEO)",
        goal="Oversee the research desk and ensure trading tasks are executed logically.",
        backstory="You are a conservative fund manager focused on the Indian stock market.",
        verbose=True,
        llm=gemini_brain
    )

    backtest_agent = Agent(
        role="Quantitative Backtest Analyst",
        goal="Fetch accurate historical market data and analyze historical trends.",
        backstory="You are a data analyst who relies heavily on numbers.",
        verbose=True,
        tools=[fetch_stock_data],
        llm=gemini_brain
    )

    # 2. Define Tasks (Now using the dynamic ticker_symbol!)
    task_coordination = Task(
        description=f"Analyze the request: 'We need to check the recent performance of {ticker_symbol} to see where it stands.' Delegate the data gathering safely.",
        expected_output="A directive assigning the stock analysis to the research desk.",
        agent=ceo_agent
    )

    task_backtest = Task(
        description=f"Use your tool to fetch the last 6 months of daily data for {ticker_symbol}. Review the generated CSV summary and provide a brief report on the final closing price trend.",
        expected_output="A summary confirming data download and noting the latest closing price direction.",
        agent=backtest_agent
    )

    # 3. Assemble and Run the Firm
    trading_firm = Crew(
        agents=[ceo_agent, backtest_agent],
        tasks=[task_coordination, task_backtest],
        process=Process.sequential,
        verbose=True
    )
    
    return trading_firm.kickoff()