#!/bin/bash

CONTAINER_NAME="computer-agent"
IMAGE_NAME="computer-agent"

function start_container() {
    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Container ${CONTAINER_NAME} already exists. Starting it..."
        docker start ${CONTAINER_NAME}
    else
        echo "Building and starting new container..."
        # Build the agent container
        docker build -t ${IMAGE_NAME} -f Dockerfile.agent .

        # Run the container with necessary environment variables and volume mounts
        docker run -d \
            --name ${CONTAINER_NAME} \
            -e API_PROVIDER=bedrock \
            -e AWS_PROFILE=$AWS_PROFILE \
            -e AWS_REGION=us-west-2 \
            -v $HOME/.aws:/home/computeruse/.aws \
            -v $HOME/.anthropic:/home/computeruse/.anthropic \
            -p 8000:8000 \
            ${IMAGE_NAME}
    fi
}

function stop_container() {
    echo "Stopping container..."
    docker stop ${CONTAINER_NAME}
}

function restart_container() {
    stop_container
    start_container
}

function send_instructions() {
    if [ -z "$1" ]; then
        echo "Please provide instructions as an argument"
        echo "Usage: $0 send 'your instructions here'"
        exit 1
    fi

    # Send instructions to the container's API
    curl -X POST "http://localhost:8000/execute" \
         -H "Content-Type: application/json" \
         -d "{\"text\": \"$1\"}"
}

case "$1" in
    "start")
        start_container
        ;;
    "stop")
        stop_container
        ;;
    "restart")
        restart_container
        ;;
    "send")
        shift  # Remove the "send" argument
        send_instructions "$*"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|send 'instructions'}"
        exit 1
        ;;
esac 