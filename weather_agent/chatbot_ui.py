from agent import weather_assistant
import asyncio
import chainlit as cl

@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, I'm Weather Assistant. How can I help you today?").send()

@cl.on_message
async def chat(message:cl.message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result =asyncio.run(weather_assistant(history))
        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        cl.user_session.set("chat_history", result.to_input_list())

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")