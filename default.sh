#!/bin/bash

apt update
apt install -y screen vim git-lfs git wget bzip2 tar
screen

git clone https://github.com/PygmalionAI/aphrodite-engine
cd aphrodite-engine

./runtime.sh python -m aphrodite.endpoints.openai.api_server --model $MODEL --quantization $QUANTIZATION --chat-template ../DeploIt/chat_template/$CHAT_TEMPLATE.jinja
