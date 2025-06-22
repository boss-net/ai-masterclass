import json
import os
import uuid
from datetime import datetime
from typing import List

import asana
import streamlit as st
from asana.rest import ApiException
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

load_dotenv()

model = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")

configuration = asana.Configuration()
configuration.access_token = os.getenv("ASANA_ACCESS_TOKEN", "")
api_client = asana.ApiClient(configuration)
tasks_api_instance = asana.TasksApi(api_client)


def create_asana_task(task_name: str, due_on: str = "today") -> str:
    """
    Creates a task in Asana given the name of the task and when it is due.

    Args:
        task_name (str): The name of the task in Asana.
        due_on (str): The date the task is due in the format YYYY-MM-DD. If not given, the current day is used.
    Returns:
        str: The API response of adding the task to Asana or an error message if the API call threw an error.
    """
    if due_on == "today":
        due_on = str(datetime.now().date())

    task_body = {"data": {"name": task_name, "due_on": due_on, "projects": [os.getenv("ASANA_PROJECT_ID", "")]}}

    try:
        tasks_api_instance.create_task(task_body, {})
        return "Task created successfully!"
    except ApiException:
        return "Failed to create task!"


@st.cache_resource
def get_local_model():
    if "gpt" in model:
        return model
    return HuggingFaceEndpoint(repo_id=model, task="text-generation", max_new_tokens=1024, do_sample=False)


llm = get_local_model()

available_tools = {"create_asana_task": create_asana_task}

tool_descriptions = [f"{name}:\n{func.__doc__}\n" for name, func in available_tools.items()]


class ToolCall(BaseModel):
    name: str = Field(description="Name of the function to run")
    args: dict = Field(description="Arguments for the function call (empty if no arguments are needed for the tool call)")


class ToolCallOrResponse(BaseModel):
    tool_calls: List[ToolCall] = Field(description="List of tool calls, empty array if you don't need to invoke a tool")
    content: str = Field(description="Response to the user if a tool doesn't need to be invoked")


tool_text = f"""
You always respond with a JSON object that has two required keys.

tool_calls: List[ToolCall] = Field(description="List of tool calls, empty array if you don't need to invoke a tool")
content: str = Field(description="Response to the user if a tool doesn't need to be invoked")

Here is the type for ToolCall (object with two keys):
    name: str = Field(description="Name of the function to run (NA if you don't need to invoke a tool)")
    args: dict = Field(description="Arguments for the function call (empty array if you don't need to invoke a tool or if no arguments are needed for the tool call)")

Don't start your answers with "Here is the JSON response", just give the JSON.

The tools you have access to are:

{"".join(tool_descriptions)}

Any message that starts with "Thought:" is you thinking to yourself. This isn't told to the user so you still need to communicate what you did with them.
Don't repeat an action. If a thought tells you that you already took an action for a user, don't do it again.
"""


def prompt_ai(messages, nested_calls=0, invoked_tools=None):
    if invoked_tools is None:
        invoked_tools = []
    if nested_calls > 3:
        raise Exception("Failsafe - AI is failing too much!")

    parser = JsonOutputParser(pydantic_object=ToolCallOrResponse)
    asana_chatbot = ChatHuggingFace(llm=llm) | parser if "gpt" not in model else ChatOpenAI(model=llm) | parser

    try:
        ai_response = asana_chatbot.invoke(messages)
    except Exception:
        return prompt_ai(messages, nested_calls + 1, invoked_tools)

    has_tool_calls = len(ai_response["tool_calls"]) > 0
    if has_tool_calls:
        for tool_call in ai_response["tool_calls"]:
            tool_call_str = json.dumps(tool_call)
            if tool_call_str not in invoked_tools:
                tool_name = tool_call["name"].lower()
                selected_tool = available_tools.get(tool_name)
                if not selected_tool:
                    continue
                tool_output = selected_tool(**tool_call["args"])
                messages.append(
                    AIMessage(content=f"Thought: - I called {tool_name} with args {tool_call['args']} and got back: {tool_output}.")
                )
                invoked_tools.append(tool_call_str)
            else:
                return ai_response
        return prompt_ai(messages, nested_calls + 1, invoked_tools)
    return ai_response


def main():
    st.title("Asana Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content=f"You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}.\n{tool_text}"
            )
        ]

    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        message_type = message_json["type"]
        message_content = message_json["content"]
        if message_type in ["human", "ai", "system"] and not message_content.startswith("Thought:"):
            with st.chat_message(message_type):
                st.markdown(message_content)

    if prompt := st.chat_input("What would you like to do today?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        with st.chat_message("assistant"):
            ai_response = prompt_ai(st.session_state.messages)
            st.markdown(ai_response["content"])

        st.session_state.messages.append(AIMessage(content=ai_response["content"]))


if __name__ == "__main__":
    main()
