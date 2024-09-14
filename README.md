# Telegram Bot to help summarize pages in a group chat or channels

[![Status](https://github.com/DigitalPig/telegram_llm_bot/actions/workflows/lint-deploy.yml/badge.svg)](https://github.com/DigitalPig/telegram_llm_bot/actions/workflows/lint-deploy.yml)

## Why?

Many times I have found that I would love to see a bot in my group chat that can help me summarize/translate
links I shared with my family via Telegram. Not everyone is fluent in English so a quick summary in Chinese
is going to be very helpful for some to decide if he/she needs to spend more time on it.

## Design

It is very simple. Currently it leverages the Anthropic Claude AI to do the summary. Note that Claude does
not get the content of the webpage by itself so there are a helper function to extract the content of the
webpage first. And this helper function does not extract the content correctly everytime so expect occasional 
404 errors.

## Pre-requisites

1. Anthropic API token, which you get get from [here](https://docs.anthropic.com/en/api/getting-started).
2. Telegram Bot token. You can follow the instruction [here](https://core.telegram.org/bots/tutorial).
3. Save those two tokens in a file called `.env`.
4. Build the container either by `docker` or `podman`.
5. Run the container via `podman run --env-file .env`
6. Adding the bot to your group chat.
7. That's it!

## TODOs

- [ ] Headless Chrome to extract the webpage correctly (maybe even a LLM bot for that?)
- [ ] Expanding command list to include other functions like `translate`.
