import asana
from asana.rest import ApiException
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
import json
import os
import logging

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage

# ----------------- SETUP & LOGGING -----------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

MODEL = os.getenv('LLM_MODEL', 'gpt-4o')
ASANA_ACCESS_TOKEN = os.getenv('ASANA_ACCESS_TOKEN', '')
WORKSPACE_GID = os.getenv("ASANA_WORKSPACE_ID", "")  # Corrected variable name

if not ASANA_ACCESS_TOKEN or not WORKSPACE_GID:
    logging.warning("Missing ASANA_ACCESS_TOKEN or ASANA_WORKSPACE_ID in environment variables.")

configuration = asana.Configuration()
configuration.access_token = ASANA_ACCESS_TOKEN
api_client = asana.ApiClient(configuration)
projects_api_instance = asana.ProjectsApi(api_client)
tasks_api_instance = asana.TasksApi(api_client)

# ----------------- TOOL FUNCTIONS -----------------

@tool
def create_asana_task(task_name: str, project_gid: str, due_on: str = "today") -> str:
    """Create a task in Asana."""
    if due_on == "today":
        due_on = str(datetime.now().date())
    task_body = {
        "data": {
            "name": task_name,
            "due_on": due_on,
            "projects": [project_gid]
        }
    }
    try:
        api_response = tasks_api_instance.create_task(task_body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logging.error(f"TasksApi->create_task: {e}")
        return f"Exception when calling TasksApi->create_task: {e}"

@tool
def get_asana_projects() -> str:
    """Get all the projects in the user's Asana workspace."""
    opts = {
        'limit': 50,
        'workspace': WORKSPACE_GID,
        'archived': False
    }
    try:
        api_response = projects_api_instance.get_projects(opts)
        return json.dumps(list(api_response), indent=2)
    except ApiException as e:
        logging.error(f"ProjectsApi->get_projects: {e}")
        return f"Exception when calling ProjectsApi->get_projects: {e}"

@tool
def create_asana_project(project_name: str, due_on: str = None) -> str:
    """Create a project in Asana."""
    body = {
        "data": {
            "name": project_name,
            "due_on": due_on,
            "workspace": WORKSPACE_GID
        }
    }
    try:
        api_response = projects_api_instance.create_project(body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logging.error(f"ProjectsApi->create_project: {e}")
        return f"Exception when calling ProjectsApi->create_project: {e}"

@tool
def get_asana_tasks(project_gid: str) -> str:
    """Get all tasks in a specified Asana project."""
    opts = {
        'limit': 50,
        'project': project_gid,
        'opt_fields': "created_at,name,due_on"
    }
    try:
        api_response = tasks_api_instance.get_tasks(opts)
        return json.dumps(list(api_response), indent=2)
    except ApiException as e:
        logging.error(f"TasksApi->get_tasks: {e}")
        return f"Exception when calling TasksApi->get_tasks: {e}"

@tool
def update_asana_task(task_gid: str, data: dict) -> str:
    """Update a task in Asana."""
    body = {"data": data}
    try:
        api_response = tasks_api_instance.update_task(body, task_gid, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logging.error(f"TasksApi->update_task: {e}")
        return f"Exception when calling TasksApi->update_task: {e}"

@tool
def delete_task(task_gid: str) -> str:
    """Delete a task in Asana."""
    try:
        api_response = tasks_api_instance.delete_task(task_gid)
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logging.error(f"TasksApi->delete_task: {e}")
        return f"Exception when calling TasksApi->delete_task: {e}"

available_functions = {
    "create_asana_task": create_asana_task,
    "get_asana_projects": get_asana_projects,
    "create_asana_project": create_asana_project,
    "get_asana_tasks": get_asana_tasks,
    "update_asana_task": update_asana_task,
    "delete_task": delete_task
}

# ----------------- AI PROMPTING FUNCTION -----------------

def get_chatbot(model_name: str):
    return ChatOpenAI(model=model_name) if "gpt" in model_name.lower() else ChatAnthropic(model=model_name)

def prompt_ai(messages, nested_calls=0):
    if nested_calls > 5:
        raise Exception("AI is tool calling too much!")

    tools = list(available_functions.values())
    chatbot = get_chatbot(MODEL)
    chatbot_with_tools = chatbot.bind_tools(tools)

    stream = chatbot_with_tools.stream(messages)
    first = True
    for chunk in stream:
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk
        yield chunk

    has_tool_calls = len(getattr(gathered, "tool_calls", [])) > 0

    if has_tool_calls:
        messages.append(gathered)
        for tool_call in gathered.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = available_functions.get(tool_name)
            if not selected_tool:
                logging.warning(f"Unknown tool requested: {tool_name}")
                messages.append(ToolMessage(f"Unknown tool: {tool_name}", tool_call_id=tool_call["id"]))
                continue
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
        additional_stream = prompt_ai(messages, nested_calls + 1)
        for additional_chunk in additional_stream:
            yield additional_chunk

# ----------------- MAIN & UI -----------------

system_message = (
    "You are a personal assistant who helps manage tasks in Asana. "
    "You never give IDs to the user since those are just for you to keep track of. "
    "When a user asks to create a task and you don't know the project to add it to for sure, clarify with the user. "
    f"The current date is: {datetime.now().date()}"
)

def main():
    st.title("Asana Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=system_message)]

    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])

    prompt = st.chat_input("What would you like to do today?")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("assistant"):
            stream = prompt_ai(st.session_state.messages)
            response = st.write_stream(stream)
        st.session_state.messages.append(AIMessage(content=response))


if __name__ == "__main__":
    main()
