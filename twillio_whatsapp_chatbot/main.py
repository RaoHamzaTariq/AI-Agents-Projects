from fastapi import FastAPI, Form
from fastapi.responses import Response
from agent import joke_assistant
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.post("/")
async def bot(Body: str = Form(...)):
    user_msg = Body.lower()
    response = MessagingResponse()

    result = await joke_assistant(user_msg)

    response.message(result.final_output)

    print(f"User: {user_msg}")
    print(f"Assistant: {result.final_output}")

    return Response(content=str(response), media_type="application/xml")
