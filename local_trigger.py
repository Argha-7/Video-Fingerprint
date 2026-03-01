import os
from unittest.mock import patch
from modify_fingerprint import main

# The URL provided by the user for local verification
NEW_URL = "https://youtu.be/i61nN7hcbPA?si=Uh5ZYHKCQ4LDtC1T"

if __name__ == "__main__":
    with patch('builtins.input', return_value=NEW_URL):
        main()
