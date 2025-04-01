#!/bin/bash

# Path to the install script
apt-get install -y curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
curl -LsSf https://raw.githubusercontent.com/griptape-ai/griptape-nodes/refs/heads/main/install.sh | bash -s
