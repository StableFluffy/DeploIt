#!/bin/bash

apt-get update && apt-get install -y build-essential && pip install git+https://github.com/PygmalionAI/aphrodite-engine@dev

python -m aphrodite.endpoints.openai.api_server --model $MODEL --quantization $QUANTIZATION --chat-template ../DeploIt/chat_template/$CHAT_TEMPLATE.jinja
