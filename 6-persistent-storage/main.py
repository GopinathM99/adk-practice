import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent import memory_agent
from utils import call_agent_async

load_dotenv()


db_url = "sqlite:///./memory-agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

initial_state = {
    "user_name": "John Doe",
    "reminders": [],
}


async def main_async():

    APP_NAME = "memory agent"
    USER_ID = "john_doe"

    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME, user_id=USER_ID
    )

    print(f"Existing sessions: {existing_sessions}")

    if (existing_sessions and len(existing_sessions.sessions) > 0):
        session_id = existing_sessions.sessions[0].id
        print(f"Resuming session {session_id}")
    else:
        new_session = session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, state=initial_state
        )
        print(f"Created new session {new_session.id}")
        session_id = new_session.id

    runner = Runner(
        app_name=APP_NAME,
        session_service=session_service,
        agent=memory_agent,
    )
    
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        query = input("Enter a query: ")

        if query.lower() in ["exit", "quit"]:
            print("Thank you for using Memory Agent Chat!")
            break

        await call_agent_async(runner, USER_ID, session_id, query)

if __name__ == "__main__":
    asyncio.run(main_async())
