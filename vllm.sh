#!/bin/bash

apt-get update && apt-get install -y build-essential && pip install vllm

echo 'Build Done. Starting server...'

CMD="python -m vllm.entrypoints.openai.api_server --model $MODEL --chat-template ../DeploIt/chat_template/$CHAT_TEMPLATE.jinja --host 0.0.0.0 --dtype float16"

if [ -n "$QUANTIZATION" ]; then
    CMD="$CMD --quantization $QUANTIZATION"
fi

exec $CMD
