import torch

if torch.cuda.is_available():
    print(f"{torch.cuda.get_device_name(0)} is available for use.")
else:
    print("No GPU available. Training will run on CPU.")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"GPU Acceleration devcie: {device}")
