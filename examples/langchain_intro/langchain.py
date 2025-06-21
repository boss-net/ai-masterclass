import json
import logging
import os
import sys
from datetime import datetime

import asana
from asana.rest import ApiException
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from openai import OpenAI

# ----------------- CONFIGURATION & LOGGING -----------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

MODEL = os.getenv("LLM_MODEL", "gpt-4o")
ASANA_PROJECT_ID = os.getenv("ASANA_PROJECT_ID")
ASANA_ACCESS_TOKEN = os.getenv("ASANA_ACCESS_TOKEN")

if not ASANA_PROJECT_ID or not ASANA_ACCESS_TOKEN:
    logging.warning(
        "Missing ASANA_PROJECT_ID or ASANA_ACCESS_TOKEN in environment variables."
    )

configuration = asana.Configuration()
configuration.access_token = ASANA_ACCESS_TOKEN or ""
api_client = asana.ApiClient(configuration)
tasks_api_instance = asana.TasksApi(api_client)

# ----------------- ASANA TOOL -----------------


@tool
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

    if not ASANA_PROJECT_ID:
        return "Error: ASANA_PROJECT_ID is not set."

    task_body = {
        "data": {"name": task_name, "due_on": due_on, "projects": [ASANA_PROJECT_ID]}
    }

    try:
        api_response = tasks_api_instance.create_task(task_body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logging.error(f"Exception when calling TasksApi->create_task: {e}")
        return f"Exception when calling TasksApi->create_task: {e}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"


# ----------------- AI PROMPTING LOGIC -----------------


def get_chatbot(model_name: str):
    if "gpt" in model_name.lower():
        return ChatOpenAI(model=model_name)
    else:
        return ChatAnthropic(model=model_name)


def prompt_ai(messages, nested_calls=0):
    if nested_calls > 5:
        raise Exception("AI is tool calling too much!")

    tools = [create_asana_task]
    chatbot = get_chatbot(MODEL)
    chatbot_with_tools = chatbot.bind_tools(tools)

    ai_response = chatbot_with_tools.invoke(messages)
    logging.info(f"AI response: {ai_response}")

    tool_calls = bool(getattr(ai_response, "tool_calls", []))

    if tool_calls:
        available_functions = {"create_asana_task": create_asana_task}
        messages.append(ai_response)
        for tool_call in ai_response.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = available_functions.get(tool_name)
            if selected_tool:
                tool_output = selected_tool.invoke(tool_call["args"])
                messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
            else:
                logging.warning(f"Unknown tool requested: {tool_name}")
                messages.append(
                    ToolMessage(
                        f"Unknown tool: {tool_name}", tool_call_id=tool_call["id"]
                    )
                )
        # Recurse for further AI response
        return prompt_ai(messages, nested_calls + 1)

    return ai_response


# ----------------- MAIN LOOP -----------------


def main():
    messages = [
        SystemMessage(
            content=f"You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}"
        )
    ]

    print("Welcome to the Asana AI Agent! Type 'q' to quit.")
    while True:
        try:
            user_input = input("Chat with AI (q to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if user_input.lower() == "q":
            break

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))
        try:
            ai_response = prompt_ai(messages)
            print(ai_response.content)
            messages.append(ai_response)
        except Exception as e:
            logging.error(f"Error during AI interaction: {e}")
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
