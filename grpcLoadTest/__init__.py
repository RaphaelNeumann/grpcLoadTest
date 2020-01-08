import sys
import os
from pathlib import Path

# Create hidden tempory folder
temp_path = os.getcwd()  + '/.grpcLoadTest'

Path(temp_path).mkdir(parents=True, exist_ok=True)
sys.path.append(temp_path)