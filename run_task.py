from modify_fingerprint import main
from unittest.mock import patch

if __name__ == "__main__":
    url = "https://youtu.be/d4drpe-de-I?si=CFO8ObnWKRNNEHIE"
    with patch('builtins.input', return_value=url):
        main()
