import chainlit as cl
from agent import run_email_agent

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("chat_history",[])
    await cl.Message(content="Welcome to the Email Agent! You can ask me to send an email.").send()

@cl.on_message
async def handle_message(message: cl.message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result = await run_email_agent(history)
        msg.content = result.final_output
        await msg.update()

        cl.user_session.set("chat_history", result.to_input_list())

        print(f"User: {message.content}")
        print(f"Agent: {result.final_output}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
