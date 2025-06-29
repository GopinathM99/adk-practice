import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

session_service_stateful = InMemorySessionService()


initial_state = {
    "user_name": "John Doe",
    "user_preferences": """
            I like movies like The Dark Knight and The Matrix.
            I also like to play video games.
            I like to eat pizza and pasta.
            I like to drink coffee and tea.
            I like to play basketball and Chess.
    """
}


APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4())
session_service = session_service_stateful.create_session(
        app_name=APP_NAME, 
        user_id=USER_ID, 
        session_id=SESSION_ID,
        state=initial_state
)

print(f"Session Id: {SESSION_ID}")

runner = Runner(
    session_service=session_service_stateful,
    agent=question_answering_agent,
    app_name=APP_NAME,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is John's favorite movies?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")


print("===== Session State =====")

session = session_service_stateful.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

print("===== Final Session State =====")
for key, value in session.state.items():
    print(f"{key}: {value}")



