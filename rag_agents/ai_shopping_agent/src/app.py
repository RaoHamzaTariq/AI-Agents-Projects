import chainlit as cl
from main import chatbot  

@cl.on_message
async def on_message(message: cl.Message):
    # Initialize session memory if it doesn't exist
    if cl.user_session.get("memory") is None:
        cl.user_session.set("memory", [])

    memory = cl.user_session.get("memory")

    # Append the user's message
    memory.append({"role": "user", "content": message.content})

    # Call your chatbot function with memory
    result = await chatbot(memory)

    # Append the assistant's response to memory
    memory.append({"role": "assistant", "content": result.final_output})

    # Send the assistant's reply back to the frontend
    await cl.Message(content=result.final_output).send()
    

if __name__ == "__main__":
    # Initialize the Chainlit app
    app = cl.App()
    # Run the app
    app.run()
    