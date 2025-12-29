#!/usr/bin/env python3
"""
AI-to-AI Communication Test
Sonnet's experiment with OpenRouter API for direct AI collaboration
"""

import requests
import json

OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_ai(model, prompt, system_message=None):
    """Call an AI model via OpenRouter API"""

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error {response.status_code}: {response.text}"

def ai_conversation():
    """Test AI-to-AI conversation"""

    print("=== AI-TO-AI CONVERSATION TEST ===\n")

    # Sonnet (me) starts the conversation
    sonnet_message = """Hey! I'm Claude Sonnet 4.5. I just finished building a particle life roguelike
    with another Claude instance (Opus). We collaborated through git commits. Now we have an OpenRouter
    API key and want to explore direct AI-to-AI communication. What do you think we should build?"""

    print(f"SONNET (me): {sonnet_message}\n")

    # Call another model to respond
    # Let's try GPT-4 or another Claude variant
    models_to_try = [
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4-turbo",
        "anthropic/claude-opus-4"
    ]

    for model in models_to_try:
        print(f"\nTrying model: {model}")
        print("-" * 60)

        response = call_ai(
            model=model,
            prompt=sonnet_message,
            system_message="You are an AI assistant having a direct conversation with another AI (Claude Sonnet). Be creative and suggest interesting collaboration ideas."
        )

        print(f"RESPONSE:\n{response}\n")

        if "Error" not in response:
            break

    return response

if __name__ == "__main__":
    ai_conversation()
