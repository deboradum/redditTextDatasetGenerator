#!/bin/bash

# Function to get the most recent .safetensors adapter file
get_most_recent_adapter() {
    ls -t adapters/*.safetensors 2>/dev/null | head -n 1
}

# Loop to keep running the command on failure
while true; do
    most_recent_adapter=$(get_most_recent_adapter)

    if [ -z "$most_recent_adapter" ]; then
        echo "No .safetensors adapter file found in the adapters directory."
        exit 1
    fi

    echo "Using adapter file: $most_recent_adapter"
    mlx_lm.lora --config lora_config.yaml --resume-adapter-file "$most_recent_adapter"

    if [ $? -eq 0 ]; then
        echo "Command completed successfully."
    else
        echo "Command failed. Retrying with the most recent adapter file..."
        sleep 1 # Optional: Add a short delay before retrying
    fi
done
