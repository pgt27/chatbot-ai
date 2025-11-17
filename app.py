import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.ui.chat_ui import main_ui 

if __name__ == "__main__":
    main_ui()
