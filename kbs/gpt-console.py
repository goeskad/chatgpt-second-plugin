# -*- coding: utf-8 -*-
from kbs import kbsChat, kbsHelper
import asyncio
# from datastore.factory import get_datastore


# Main function that runs the chatbot
# async def init():
#     global datastore
#     datastore = await get_datastore()
#     kbsHelper.kbs_ds = datastore


async def main():
    # init()
    init_promote = "你将担任某个软件系统的客服助理。用户会问你一些使用此软件系统时遇到的问题。用户给你的提问中将包含一些关于此系统的知识，你需要根据这些知识来回答用户的提问。"
    message_log = [
        {"role": "system", "content": init_promote}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    # Start a loop that runs until the user types "quit"
    while True:
        if first_request:
            # If this is not the first request, get the user's input and add it to the conversation history
            user_input = input("You: ")

            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            kbs_queries = kbsChat.generate_kbs_queries(user_input)
            formatted_kbs_queries = kbsChat.format_kbs_queries(kbs_queries)
            print(f"AI assistant: 将为您从知识库中查询以下问题: \n{formatted_kbs_queries}请稍后")

            response = await kbsChat.chat_with_gpt(message_log, user_input, kbs_queries)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

            print(f"AI assistant: {response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    asyncio.run(main())
