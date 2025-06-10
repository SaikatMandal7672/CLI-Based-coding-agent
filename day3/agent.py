from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
from tools2 import available_tools
from typing import Dict
from pathlib import Path
from prompts import SYSTEM_PROMPT2

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_key")
def __init__(self, base_path: str = "."):
    """Initialize with a base directory path."""
    self.base_path = Path(base_path).resolve()


# available_tools = {
#     "get_weather": get_weather,
#     "run_command": run_command,
#     "curr_date":cur_time
# }
SYSTEM_PROMPT = """
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query.
    - if the user asks a general question that does not involve the use of tools and functions, just provide a general response
    - To create a new folder always use "run_command tool" with input like "mkdir file_name" 


    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.
    - "write_file": takes in 2 imputs - file path and content. Writes the content to the file mentioned in the path,
 

    Example1:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": {"city":"new york"} }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}




    Example2:
    User Query: how to create a while loop in python?
    Output: {{ "step": "plan", "content": "The user want to know about while loops in python" }}
    Output: {{ "step": "output", "content": "while loop in python can be created as :\n while condition: \n /// your logic" }}

    Example3:
    User Query: Create a todo app.
    Output: {{ "step": "plan", "content": "The user is interseted to creat a TODO application" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call create_folder" }}
    Output: {{ "step": "action", "function": "run_command", "input": "mkdir TODO"}}
    Output: {{ "step": "plan", "content": "I need to change the directory to TODO" }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd TODO"}}
    Output: {{ "step": "plan", "content": "i should return the compete path to foder" }}
    Output: {{ "step": "action", "function": "run_command", "input": "pwd"}}
    Output: {{ "step": "plan", "content": "Now i need to initialise a React App using Vite" }}
    Output: {{ "step": "action", "function": "run_command", "input": "npx create-vite@latest my-todo"}}
    Output: {{ "step": "plan", "content": "Now i need to install the dependencies" }}
    Output: {{ "step": "action", "function": "run_command", "input": "npm install"}}
    Output: {{ "step": "plan", "content": "Now i need to make changes to the  App.jsx file" }}
    Output: {{ "step": "action", "function": "write_file", "input":{"file_path":"TODO/my-todo/src/App.jsx","content":" write some react code"}}}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

    Example3:
    User Query: Create a folder XYZ
    Output: {{ "step": "plan", "content": "The user want to create a " }}
    Output: {{ "step": "output", "content": "while loop in python can be created as :\n while condition: \n /// your logic" }}

    RULES - 
    1. Always wait for the preevious step to be completed.
    2. Analyse if the user query needs to use any available tools , else give a generalised response based on the query.
    
"""

client = OpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# response = client.chat.completions.create(
#     model="gemini-2.5-flash-preview-05-20",
#     messages=[
#         {
#             "role":"system", "content":SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": "what was the  date 77 days back"
#         }
#     ]
# )

# print(response.choices[0].message.content)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT2},
]

print("Type 'Exit' to end the process.")
while True:
    query = input(">")
    if query.lower() == "exit":
        exit()
        break
    messages.append({"role": "user", "content": query})
    
    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages,
        )
        
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        
        parsed_res = json.loads(response.choices[0].message.content)
        
        if parsed_res.get("step") == "plan":
            print(f"🧠: {parsed_res.get('content')}")
            continue
            
        if parsed_res.get("step") == "action":
            tool_name = parsed_res.get("function")
            tool_input = parsed_res.get("input")
            print(f"🛠️: Calling Tool: {tool_name} with input {tool_input}")

        

            try:
                # Handle tools that need multiple parameters (dictionary input)
                if tool_name in ["write_file"] and isinstance(tool_input, dict):
                    file_path = tool_input.get("file_path")
                    content = tool_input.get("content")
                    
                    if not file_path or content is None:
                        print("❌ Error: Both 'file_path' and 'content' are required")
                        continue
                    
                    output = available_tools[tool_name](file_path=file_path, content=content)
                
                # Handle tools that take dictionary input but as single parameter
                elif tool_name == "get_weather" and isinstance(tool_input, dict ):
                    output = available_tools[tool_name](tool_input)
                
                # Handle tools that take simple string input
                else:
                    output = available_tools[tool_name](tool_input)
                
                # Add observation to messages
                messages.append({
                    "role": "user",
                    "content": json.dumps({"step": "observe", "output": str(output)})
                })
                print(f"✅ Tool executed successfully: {output}")
                continue
                
            except TypeError as e:
                print(f"❌ Error: Invalid input format for {tool_name}: {e}")
                continue
            except Exception as e:
                print(f"❌ Error executing {tool_name}: {e}")
                continue
                
        if parsed_res.get("step") == "output":
            print(f"🤖: {parsed_res.get('content')}")
            break