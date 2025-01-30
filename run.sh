./koboldcpp model.gguf --usecublas 0 mmq --multiuser --gpulayers $LAYERS --contextsize $CONTEXT_SIZE --quiet --flashattention --sdmodel imodel.gguf --threads 4 --sdquant --sdclamped --port 8005
