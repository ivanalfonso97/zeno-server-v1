import json
from typing import AsyncGenerator
from fastapi import HTTPException
import google.generativeai as genai

from app.core.config import settings
from app.schemas.chat import ChatMessage
from app.core.prompts import CALENDAR_SCHEDULE_PROMPT
from app.services.integrations.google_calendar import get_google_calendar_events, get_google_credentials

def is_greeting_or_calendar_query(query: str) -> bool:
    """
    Checks if the query is a greeting or a general calendar-related question.
    """
    normalized_query = query.lower()
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    calendar_keywords = ["calendar", "schedule", "events", "what's on", "what is on", "appointments", "today", "tomorrow", "this week", "next week"]

    if any(greeting in normalized_query for greeting in greetings):
        return True
    
    # Check for general calendar queries (excluding specific date/time questions that LLM should handle)
    if any(keyword in normalized_query for keyword in calendar_keywords):
        return True
        
    return False

async def generate_chat_response(messages: list[ChatMessage], current_user: str) -> AsyncGenerator[str, None]:
    """
    Generates a streaming chat response using the Gemini 1.5 Flash model.
    Args:
        messages: A list of chat messages, each with 'role' and 'content'.
    Yields:
        Chunks of the streamed response content.
    """
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

    # Convert messages to the format expected by start_chat
    # Note: Gemini API typically expects alternating roles, starting with 'user'.
    chat_history = []
    # All messages except the last one are history
    for msg in messages[:-1]:
        chat_history.append({
            'role': msg.role,
            'parts': [{'text': msg.content}]
        })

    # Get the last message
    last_message = messages[-1]
    last_message_content = last_message.content

    # Check if the last message is a greeting or general calendar query
    if is_greeting_or_calendar_query(last_message_content):
        calendar_info = ""
        if current_user:
            try:
                credentials = await get_google_credentials(current_user)
                # TODO: Fileter based on time
                # today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                # today_end = today_start + timedelta(days=1)
                events = await get_google_calendar_events(credentials)
                if events is None or len(events) == 0:
                    calendar_info = "No events found on your Google Calendar for today."
                calendar_info = json.dumps(events)
            except HTTPException as e:
                calendar_info = f"Error fetching calendar events: {e.detail}"
            except Exception as e:
                calendar_info = f"An unexpected error occurred while fetching calendar events: {e}"
        else:
            calendar_info = "User not authenticated. Please log in to fetch calendar events."
        
        # Override last_message_content with the generated calendar query
        last_message_content = CALENDAR_SCHEDULE_PROMPT.format(calendar_info=calendar_info)
    try:
        # Create the chat session
        chat = model.start_chat(history=chat_history)

        # Send the last message
        response_chunks = chat.send_message(last_message_content, stream=True)
        for chunk in response_chunks:
            yield f"{json.dumps({'content': chunk.text})}\n\n"
    except Exception as e:
        print(f"Error generating content from Gemini: {e}")
        yield f"{json.dumps({'content': f'Error: {e}'})}\n\n" 