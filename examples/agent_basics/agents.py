import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import asana
from asana.rest import ApiException
from dotenv import load_dotenv
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agents")


def load_environment():
    load_dotenv()
    required_vars = ["ASANA_ACCESS_TOKEN", "ASANA_PROJECT_ID", "OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.warning(f"Missing environment variables: {', '.join(missing)}")


def get_openai_client() -> OpenAI:
    return OpenAI()


def get_asana_client() -> asana.ApiClient:
    configuration = asana.Configuration()
    access_token = os.getenv("ASANA_ACCESS_TOKEN")
    if not access_token:
        logger.error("ASANA_ACCESS_TOKEN is not set in the environment.")
        sys.exit(1)
    configuration.access_token = access_token
    return asana.ApiClient(configuration)


def create_asana_task(task_name: str, due_on: Optional[str] = "today") -> str:
    """
    Create a task in Asana with the given name and due date.

    Args:
        task_name: Name of the task.
        due_on: Due date as YYYY-MM-DD. Defaults to today.

    Returns:
        API response as JSON string, or error message.
    """
    if due_on == "today":
        due_on = str(datetime.now().date())

    project_id = os.getenv("ASANA_PROJECT_ID")
    if not project_id:
        logger.error("ASANA_PROJECT_ID is not set in the environment.")
        return "Environment not configured: ASANA_PROJECT_ID missing."

    task_body = {
        "data": {"name": task_name, "due_on": due_on, "projects": [project_id]}
    }

    try:
        api_client = get_asana_client()
        tasks_api = asana.TasksApi(api_client)
        api_response = tasks_api.create_task(task_body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        logger.exception("Error creating Asana task")
        return f"Exception when calling TasksApi->create_task: {e}"


def get_tools() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "create_asana_task",
                "description": "Creates a task in Asana with a given name and due date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_name": {
                            "type": "string",
                            "description": "The name of the task in Asana",
                        },
                        "due_on": {
                            "type": "string",
                            "description": "Due date in format YYYY-MM-DD. If omitted, uses today.",
                        },
                    },
                    "required": ["task_name"],
                },
            },
        }
    ]


def prompt_ai(messages: List[Dict[str, Any]]) -> str:
    client = get_openai_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    completion = client.chat.completions.create(
        model=model, messages=messages, tools=get_tools()
    )

    response_message = completion.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {"create_asana_task": create_asana_task}
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            if not function_to_call:
                logger.warning(f"No function available for tool: {function_name}")
                continue

            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return second_response.choices[0].message.content

    return response_message.content


def main():
    load_environment()
    messages = [
        {
            "role": "system",
            "content": f"You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}",
        }
    ]

    try:
        while True:
            user_input = input("Chat with AI (q to quit): ").strip()
            if user_input.lower() == "q":
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})
            ai_response = prompt_ai(messages)
            print(ai_response)
            messages.append({"role": "assistant", "content": ai_response})
    except KeyboardInterrupt:
        print("\nExited by user.")


if __name__ == "__main__":
    main()
