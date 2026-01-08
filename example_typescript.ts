/**
 * Claude Opus 4.5 - TypeScript Example Implementation
 *
 * This example demonstrates how to use Claude Opus 4.5 with the Anthropic TypeScript SDK.
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function main() {
  try {
    // Create a message using Claude Opus 4.5
    const message = await client.messages.create({
      model: 'claude-opus-4-5-20251101',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: 'Explain the key differences between Claude Opus 4.5 and previous versions in three bullet points.'
        }
      ]
    });

    console.log('Claude Opus 4.5 Response:');
    console.log('-'.repeat(50));
    console.log(message.content[0].text);
    console.log('-'.repeat(50));
    console.log(`\nModel: ${message.model}`);
    console.log(`Tokens used: ${message.usage.input_tokens} input, ${message.usage.output_tokens} output`);
  } catch (error) {
    console.error('Error:', error);
    console.log('\nMake sure to set your ANTHROPIC_API_KEY environment variable:');
    console.log('export ANTHROPIC_API_KEY="your-api-key-here"');
  }
}

async function streamingExample() {
  console.log('\nStreaming Example:');
  console.log('-'.repeat(50));

  const stream = await client.messages.stream({
    model: 'claude-opus-4-5-20251101',
    max_tokens: 1024,
    messages: [
      { role: 'user', content: 'Count from 1 to 5 slowly.' }
    ]
  });

  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta' &&
        chunk.delta.type === 'text_delta') {
      process.stdout.write(chunk.delta.text);
    }
  }

  console.log('\n' + '-'.repeat(50));
}

async function multiTurnConversation() {
  console.log('\nMulti-turn Conversation Example:');
  console.log('-'.repeat(50));

  const conversationHistory: Anthropic.MessageParam[] = [
    { role: 'user', content: 'What is the capital of France?' }
  ];

  // First turn
  const message1 = await client.messages.create({
    model: 'claude-opus-4-5-20251101',
    max_tokens: 1024,
    messages: conversationHistory
  });

  const assistantResponse = message1.content[0].text;
  console.log(`User: ${conversationHistory[0].content}`);
  console.log(`Assistant: ${assistantResponse}\n`);

  // Add to history and continue
  conversationHistory.push({ role: 'assistant', content: assistantResponse });
  conversationHistory.push({ role: 'user', content: 'What is its population?' });

  // Second turn
  const message2 = await client.messages.create({
    model: 'claude-opus-4-5-20251101',
    max_tokens: 1024,
    messages: conversationHistory
  });

  console.log(`User: ${conversationHistory[2].content}`);
  console.log(`Assistant: ${message2.content[0].text}`);
  console.log('-'.repeat(50));
}

// Run all examples
main()
  .then(() => streamingExample())
  .then(() => multiTurnConversation())
  .catch(console.error);
