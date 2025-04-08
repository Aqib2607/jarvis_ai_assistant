import cohere #import the cohere library for AI services.
from rich import print #Import the rich library for enhanced console output.
from dotenv import dotenv_values #Import dotenv_values to load environment variables from a .env file.

# Load environment variables from .env file
env_vars = dotenv_values(".env") #Load the environment variables from the .env file.

# Retrive the API key
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the API key
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized funchtions for task categorization.
funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate image",
    "system", "content", "google search", "youtube search", "reminder"
]

# Initialize an empty list to store user massages.
messages = []

# Define the preamble that guides the AI model on how to categorize quieries.
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

#Define a chat history with predefined user-chatbot interactions for context.
ChatHistory = [
    {"role": "USER", "message": "How are you?"},
    {"role": "CHATBOT", "message": "general How are you?"},
    {"role": "USER", "message": "do you like pizza?"},
    {"role": "CHATBOT", "message": "general do you like pizza?"},
    {"role": "USER", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "CHATBOT", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "USER", "message": "open chrome and firefox"},
    {"role": "CHATBOT", "message": "open chrome, open firefox"},
    {"role": "USER", "message": "what is today's date and by the way remind me that i have a dance performance on 5th aug at 11pm"},
    {"role": "CHATBOT", "message": "general what is today's date, reminder 11:00pm 5th aug dance performance"},
    {"role": "USER", "message": "chat with me"},
    {"role": "CHATBOT", "message": "general chat with me"},
]

# Define the main function for decision-making on queries.
def FirstLayerDMM(prompt: str = "test"):
    # Add the user's quires to the massage list.
    messages.append({"role": "User", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,  # corrected from messages=prompt
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble,
    )

    # Initialize an empty string to store generated responses.
    response = ""

    # Iterate over events in the stream and capture generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text #Append the generated text to the response.
        
    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", "")
    response = response.split(",")

    # Strip leading and trailing whitespace from each task.
    response = [i.strip() for i in response]

    # Initialize an empty list to filter valid tasks.
    temp = []

    # Filter the tasks based on recognized functions keywords.
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task) #Append valid tasks to the list.

    # Update the response with the filtered lists of tasks.
    response = temp

    # If '(query)' is in the response, recursively call the function to handle it.
    if "(query)" in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse
    else:
        # Return the final categorized response.
        return response
    
# Entry point for the script.
if __name__ == "__main__":
    # Example usage of the FirstLayerDMM function with a sample query.
    while True:
        print(FirstLayerDMM(input(">>> "))) #Print the categorized response.
