#!/bin/bash

# Function to get the most recent adapter file
get_most_recent_adapter() {
    ls -t adapters/* | head -n 1
}

# Loop to keep running the command on failure
while true; do
    most_recent_adapter=$(get_most_recent_adapter)
    echo "Using adapter file: $most_recent_adapter"
    mlx_lm.lora --config lora_config.yaml --resume-adapter-file "$most_recent_adapter"
    
    if [ $? -eq 0 ]; then
        echo "Command completed successfully."
        break
    else
        echo "Command failed. Retrying with the most recent adapter file..."
        sleep 1 # Optional: Add a short delay before retrying
    fi
done

