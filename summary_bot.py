from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)
import logging
import aiohttp
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

# Load environment variables from .env file
load_dotenv()
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def call_claude(user_input: str, client=None) -> str:
    if not client:
        raise ValueError("client is not provided")

    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"summarize the following paragraph in chinese: {user_input}",
            }
        ],
        model="claude-3-sonnet-20240229",
    )
    return message.content[0].text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="我是一个可以帮你总结网页内容的机器人"
    )


async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Summarize the content of a webpage"""
    global client
    # First get the message from the chats
    input_message = update.message.text
    input_message_id = update.effective_chat.id
    url_pattern = r"\b(?:(?:https?://)?(?:(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6})|(?:(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}))(?:/[^)\s]*)?"  # Regular expression to match URL
    urls = re.findall(url_pattern, input_message)
    if len(urls) == 0:
        await context.bot.send_message(
            chat_id=input_message_id,
            text=f"消息内没有包含网址。我将会总结翻译这段消息：{input_message}",
        )
        claude_res = await call_claude(input_message, client)
        await context.bot.send_message(chat_id=input_message_id, text=claude_res)
    else:
        separated_urls = "\n".join(urls)
        await context.bot.send_message(
            chat_id=input_message_id,
            text=f"正在提取网页\n{separated_urls}内容，请稍等...",
        )
        for i, url in enumerate(urls):
            try:
                content = await extract_main_content(url)
                logging.info(f"content is {content}")
                claude_res = await call_claude(content, client)
                await context.bot.send_message(
                    chat_id=input_message_id, text=f"第{i+1}个网址总结：\n{claude_res}"
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=input_message_id, text=f"提取网页内容失败：{str(e)}"
                )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def extract_main_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Read the response content
            html = await response.text()

    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # Drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    summary_handler = CommandHandler("summarize", summarize)
    application.add_handler(summary_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()
