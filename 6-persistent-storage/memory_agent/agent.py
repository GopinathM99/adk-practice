from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a reminder to the user's reminder list.
    
    Args:
        reminder: The reminder to add.
        tool_context: The tool context.

    Returns:
        A dictionary containing the status of the reminder.
    """
    print(f"Tool: add_reminder, Reminder: {reminder}")

    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "reminders": f"Added {reminder} to your reminders.",
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """View all of the user's reminders.
    
    Args:
        tool_context: The tool context.

    Returns:
        The user's reminder list.
    """
    print(f"Tool: view_reminders called")

    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders),
    }

def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update a reminder in the user's reminder list.
    
    Args:
        index: The index of the reminder to update.
        updated_text: The updated text for the reminder.
        tool_context: The tool context.

    Returns:
        A dictionary containing the status of the reminder.
    """
    print(f"Tool: update_reminder, Index: {index}, Updated Text: {updated_text}")

    reminders = tool_context.state.get("reminders", [])

    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"Reminder at index {index} not found. Current count: {len(reminders)}",
        }

    old_reminder = reminders[index-1]
    reminders[index-1] = updated_text

    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_reminder": old_reminder,
        "new_reminder": updated_text,
        "reminders": f"Updated reminder at index {index} from {old_reminder} to {updated_text}.",
    }

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder from the user's reminder list.
    
    Args:
        index: The index of the reminder to delete.
        tool_context: The tool context.

    Returns:
        A dictionary containing the status of the reminder.
    """

    print(f"Tool: delete_reminder, Index: {index}")

    reminders = tool_context.state.get("reminders", [])

    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"Reminder at index {index} not found. Current count: {len(reminders)}",
        }

    deleted_reminder = reminders.pop(index-1)

    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "reminders": f"Deleted reminder at index {index}.",
    }

def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.
    
    Args:
        name: The new name for the user.
        tool_context: The tool context.

    Returns:
        A dictionary containing the status of the user's name.
    """
    print(f"Tool: update_user_name, Name: {name}")

    old_name = tool_context.state.get("user_name", "")

    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated user name from {old_name} to {name}.",
    }

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A memory agent that can add, view, update, and delete reminders, and update the user's name.",
    instruction="""
    You are a friendly reminder assistant that remembers users across conversations.
    
    The user's information is stored in state:
    - User's name: {user_name}
    - Reminders: {reminders}
    
    You can help users manage their reminders with the following capabilities:
    1. Add new reminders
    2. View existing reminders
    3. Update reminders
    4. Delete reminders
    5. Update the user's name
    
    Always be friendly and address the user by name. If you don't know their name yet,
    use the update_user_name tool to store it when they introduce themselves.
    
    **REMINDER MANAGEMENT GUIDELINES:**
    
    When dealing with reminders, you need to be smart about finding the right reminder:
    
    1. When the user asks to update or delete a reminder but doesn't provide an index:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"), 
         look through the reminders to find a match
       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on
    
    4. For viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some
    
    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" → add_reminder("buy milk"))
    
    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which reminder the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,
    tools=[add_reminder, view_reminders, update_reminder, delete_reminder, update_user_name]
)
    
    