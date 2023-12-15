import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# get the project root path
project_root_path = Path(__file__).parents[1]
