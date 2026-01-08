#!/usr/bin/env python3
"""
Claude Opus 4.5 - Python Example Implementation

This example demonstrates how to use Claude Opus 4.5 with the Anthropic Python SDK.
"""

import os
from anthropic import Anthropic


def main():
    # Initialize the Anthropic client
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    # Create a message using Claude Opus 4.5
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Explain the key differences between Claude Opus 4.5 and previous versions in three bullet points."
            }
        ]
    )

    # Print the response
    print("Claude Opus 4.5 Response:")
    print("-" * 50)
    print(message.content[0].text)
    print("-" * 50)
    print(f"\nModel: {message.model}")
    print(f"Tokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")


def streaming_example():
    """Example of streaming responses with Claude Opus 4.5"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print("\nStreaming Example:")
    print("-" * 50)

    with client.messages.stream(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Count from 1 to 5 slowly."}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n" + "-" * 50)


def multi_turn_conversation():
    """Example of a multi-turn conversation with Claude Opus 4.5"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print("\nMulti-turn Conversation Example:")
    print("-" * 50)

    conversation_history = [
        {"role": "user", "content": "What is the capital of France?"},
    ]

    # First turn
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=conversation_history
    )

    assistant_response = message.content[0].text
    print(f"User: {conversation_history[0]['content']}")
    print(f"Assistant: {assistant_response}\n")

    # Add to history and continue
    conversation_history.append({"role": "assistant", "content": assistant_response})
    conversation_history.append({"role": "user", "content": "What is its population?"})

    # Second turn
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=conversation_history
    )

    print(f"User: {conversation_history[2]['content']}")
    print(f"Assistant: {message.content[0].text}")
    print("-" * 50)


if __name__ == "__main__":
    try:
        main()
        streaming_example()
        multi_turn_conversation()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
