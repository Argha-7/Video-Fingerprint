import os
from unittest.mock import patch
from modify_fingerprint import main

# The URL provided by the user for local verification
NEW_URL = "https://youtu.be/5Lyw1XnaFjo?si=tWUsXoxtdwRe32ln"

if __name__ == "__main__":
    with patch('builtins.input', return_value=NEW_URL):
        main()
