#!/bin/bash

# FUNCTION TO SIMULATE USER INPUT
simulate_input() {
    sleep 1
    echo "yes"
}

# CREATE DOWNLOAD DIRECTORY
mkdir -p /data/downloads

echo "Running all AutoTools commands with various options..."

echo -e "\n=== Testing autocaps ==="
# BASIC USAGE
autotools autocaps "test with multiple words"
# SPECIAL CHARACTERS
autotools autocaps "special chars: !@#$%^&*()"
# NUMBERS AND MIXED TEXT
autotools autocaps "123 mixed WITH lowercase 456"
# UNICODE CHARACTERS
autotools autocaps "áccênts ànd émojis 🚀 ⭐"

echo -e "\n=== Testing autolower ==="
# BASIC USAGE
autotools autolower "TEST WITH MULTIPLE WORDS"
# SPECIAL CHARACTERS
autotools autolower "SPECIAL CHARS: !@#$%^&*()"
# NUMBERS AND MIXED TEXT
autotools autolower "123 MIXED with UPPERCASE 456"
# UNICODE CHARACTERS
autotools autolower "ÁCCÊNTS ÀND ÉMOJIS 🚀 ⭐"

echo -e "\n=== Testing autopassword ==="
# BASIC PASSWORD
autotools autopassword
# CUSTOM LENGTH PASSWORD
autotools autopassword --length 32
# PASSWORD WITHOUT SPECIAL CHARS
autotools autopassword --no-special
# PASSWORD WITHOUT NUMBERS
autotools autopassword --no-numbers
# PASSWORD WITHOUT UPPERCASE
autotools autopassword --no-uppercase
# CUSTOM MINIMUM SPECIAL CHARS
autotools autopassword --min-special 3
# CUSTOM MINIMUM NUMBERS
autotools autopassword --min-numbers 3
# PASSWORD WITH ANALYSIS
autotools autopassword --analyze
# GENERATE ENCRYPTION KEY
autotools autopassword --gen-key

echo -e "\n=== Testing autoip ==="
# BASIC NETWORK INFO
autotools autoip --no-ip
# BASIC TESTS
autotools autoip --test
# DNS INFO
autotools autoip --dns
# PORT CHECK (QUICK)
autotools autoip --ports
# COMBINED TESTS WITHOUT LOCATION
autotools autoip --test --dns --no-ip

echo -e "\n=== Testing autotranslate ==="
# BASIC TRANSLATION WITH DETECTION
autotools autotranslate "Hello world" --to fr --detect
# SIMPLE TRANSLATION
autotools autotranslate "Bonjour le monde" --to en
# SPANISH TO ENGLISH
autotools autotranslate "Hola mundo" --from es --to en
# ENGLISH TO GERMAN
autotools autotranslate "Good morning" --to de
# DIRECT TRANSLATIONS (AVOIDING CHAIN ERRORS)
autotools autotranslate "I love programming" --from en --to fr
autotools autotranslate "I love programming" --from en --to es
autotools autotranslate "I love programming" --from en --to de

echo -e "\n=== Testing autospell ==="
# BASIC SPELL CHECK
autotools autospell "This is a test with misspellings"
# FRENCH SPELL CHECK
autotools autospell --lang fr "Ceci est un teste avec des fautes"
# AUTO-FIX WITHOUT CLIPBOARD
autotools autospell "This is a testt"
# JSON OUTPUT
autotools autospell "This is a test" --json
# IGNORE SPECIFIC ERROR TYPES
autotools autospell "this is a test." --ignore style --ignore punctuation
# MULTIPLE TEXTS
autotools autospell "First test" "Second testt" "Third testtt"
# DIFFERENT LANGUAGES
autotools autospell --lang en "Color" --lang fr "Couleur"

echo -e "\n=== Testing autodownload ==="
cd /data/downloads
# YOUTUBE VIDEO IN DIFFERENT QUALITIES
simulate_input | autotools autodownload "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp4 --quality 720p
simulate_input | autotools autodownload "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp4 --quality 1080p
# YOUTUBE AUDIO
simulate_input | autotools autodownload "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3
# DIRECT FILE DOWNLOAD (USING A VALID URL)
autotools autodownload "https://www.gnu.org/licenses/gpl-3.0.txt"

echo -e "\nAll tests completed!" 
