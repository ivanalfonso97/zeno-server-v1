import google.generativeai as genai
from app.core.config import settings
from typing import Generator
import json

def generate_chat_response(messages: list[dict]) -> Generator[str, None, None]:
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

    chat = model.start_chat(history=chat_history)

    # Send the last message
    last_message_content = messages[-1].content # Use dot notation

    try:
        # Synchronous streaming from chat.send_message
        response_chunks = chat.send_message(last_message_content, stream=True)
        for chunk in response_chunks:
            yield f"{json.dumps({'content': chunk.text})}\n\n"
    except Exception as e:
        print(f"Error generating content from Gemini: {e}")
        yield f"{json.dumps({'content': f'Error: {e}'})}\n\n" 