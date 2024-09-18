#!/bin/bash

# URL of the GitHub release
MODEL_URL="https://github.com/harrycallahan117/mri-tumor-analysis/releases/download/v1.0.0/variables.data-00000-of-00001"

# Destination folder for the model
MODEL_DIR="./backend/new_model_saved/variables"

# Create the directory if it doesn't exist
mkdir -p $MODEL_DIR

# Download the model file
echo "Downloading the model from GitHub..."
curl -L $MODEL_URL -o $MODEL_DIR/variables.data-00000-of-00001

echo "Model downloaded and saved to $MODEL_DIR"