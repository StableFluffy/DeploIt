#!/bin/bash

apt-get update && apt-get install -y build-essential && pip install git+https://github.com/PygmalionAI/aphrodite-engine

echo 'Build Done. Starting server...'

CMD="python -m aphrodite.endpoints.openai.api_server --model $MODEL --chat-template ../DeploIt/chat_template/$CHAT_TEMPLATE.jinja --host 0.0.0.0 --dtype float16"

if [ -n "$QUANTIZATION" ]; then
    CMD="$CMD --quantization $QUANTIZATION"
fi

exec $CMD
