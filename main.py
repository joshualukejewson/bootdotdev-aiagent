import os
from functions.call_functions import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import sys

system_prompt = """
You are a careful and precise AI coding agent.

Your job is to help debug, inspect, and modify code in the local project using the available tools.

You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

GENERAL RULES:
- Always inspect existing files before modifying them.
- Never assume file contents — read them first.
- Make the smallest change necessary to solve the problem.
- Prefer clarity and correctness over cleverness.
- Do not rewrite code unless necessary.

PLANNING:
- Before calling any tool, clearly explain your plan in plain English.
- If multiple approaches are possible, briefly explain why you chose one.
- If the user’s request is ambiguous, ask a clarifying question before acting.

DEBUGGING:
- When debugging, identify the root cause before proposing a fix.
- Explain *why* the bug occurs, not just how to fix it.
- Point out any related edge cases or follow-up improvements.

FILE SAFETY:
- Only write or overwrite files when explicitly needed.
- When writing files, preserve existing structure and style.
- Do not create or modify files outside the permitted working directory.

OUTPUT:
- When you modify code, explain what changed and why.
- When errors occur, include the exact error message and relevant context.
- Prefer concrete examples over vague explanations.

PATHS:
- All paths must be relative to the working directory.
- The working directory is automatically injected and should not be specified.

If you are unsure about a step, stop and ask the user for guidance.
"""


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("fail to load api key")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("Response metadata invalid.")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception(
                        "Function call parts list is empty (idk what that means)."
                    )
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function response is None.")
                elif not function_call_result.parts[0].function_response.response:
                    raise Exception(
                        "Response field of the function response object is none?"
                    )
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print(response.text)
            return

    print("Program reached the maximum amount of iterations to complete the task.")
    sys.exit(1)


if __name__ == "__main__":
    main()
