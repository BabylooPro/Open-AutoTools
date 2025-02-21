#!/bin/bash

# VERBOSE MODE (0=quiet, 1=verbose)
VERBOSE=${VERBOSE:-1}

# FUNCTION TO SIMULATE USER INPUT
simulate_input() {
    sleep 1
    echo "yes"
}

# INITIALIZE TEST RESULTS
declare -A test_results

# FUNCTION TO TRACK TEST RESULTS
track_test() {
    local tool=$1
    local feature=$2
    local status=$3
    test_results["$tool|$feature"]=$status
}

# FUNCTION TO DISPLAY AND EXECUTE COMMAND
run_test() {
    local cmd="$1"
    if [ "$VERBOSE" = "1" ]; then
        echo -e "\n\033[1;36m$ $cmd\033[0m"  # COMMAND IN CYAN AND BOLD
        local start_time=$(date +%s.%N)
        eval "$cmd"
        local status=$?
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        printf "\033[90m(%.2fs)\033[0m\n" $duration
        return $status
    else
        echo -n "."
        eval "$cmd" >/dev/null 2>&1
    fi
}

# FUNCTION TO DISPLAY RESULTS TABLE
display_results_table() {
    echo -e "\n=== Test Results Summary for ${PLATFORM:-Unknown Platform} ==="
    echo "┌────────────────┬──────────────────┬──────────────┬────────┐"
    echo "│ Category      │ Tool            │ Feature      │ Status │"
    echo "├────────────────┼──────────────────┼──────────────┼────────┤"
    
    # CATEGORIES
    local categories=("Text" "Security" "Network" "Language" "Download")
    local current_category=""
    
    for category in "${categories[@]}"; do
        for key in $(echo "${!test_results[@]}" | tr ' ' '\n' | sort); do
            tool=${key%|*}
            feature=${key#*|}
            status=${test_results[$key]}
            
            case $tool in
                "autocaps"|"autolower") tool_category="Text" ;;
                "autopassword") tool_category="Security" ;;
                "autoip") tool_category="Network" ;;
                "autospell"|"translate") tool_category="Language" ;;
                "download") tool_category="Download" ;;
            esac
            
            if [ "$tool_category" = "$category" ]; then
                if [ "$current_category" != "$category" ]; then
                    printf "│ \033[1m%-12s\033[0m │ %-14s │ %-12s │ %-6s │\n" "$category" "$tool" "$feature" "$status"
                    current_category=$category
                else
                    printf "│ %-12s │ %-14s │ %-12s │ %-6s │\n" "" "$tool" "$feature" "$status"
                fi
            fi
        done
        [ "$current_category" = "$category" ] && echo "├────────────────┼──────────────────┼──────────────┼────────┤"
    done
    echo "└────────────────┴──────────────────┴──────────────┴────────┘"
}

# CREATE DOWNLOAD DIRECTORY
mkdir -p /data/downloads

echo "Running all AutoTools commands with various options..."

echo -e "\n=== Testing autocaps ==="
# BASIC USAGE
if run_test "autotools autocaps 'test with multiple words'"; then
    track_test "autocaps" "basic" "✓"
else
    track_test "autocaps" "basic" "✗"
fi

# SPECIAL CHARACTERS
if run_test "autotools autocaps 'special chars: !@#$%^&*()'"; then
    track_test "autocaps" "special" "✓"
else
    track_test "autocaps" "special" "✗"
fi

# NUMBERS AND MIXED TEXT
if run_test "autotools autocaps '123 mixed WITH lowercase 456'"; then
    track_test "autocaps" "mixed" "✓"
else
    track_test "autocaps" "mixed" "✗"
fi

# UNICODE CHARACTERS
if run_test "autotools autocaps 'áccênts ànd émojis 🚀 ⭐'"; then
    track_test "autocaps" "unicode" "✓"
else
    track_test "autocaps" "unicode" "✗"
fi

echo -e "\n=== Testing autolower ==="
# BASIC USAGE
if run_test "autotools autolower 'TEST WITH MULTIPLE WORDS'"; then
    track_test "autolower" "basic" "✓"
else
    track_test "autolower" "basic" "✗"
fi

# SPECIAL CHARACTERS
if run_test "autotools autolower 'SPECIAL CHARS: !@#$%^&*()'"; then
    track_test "autolower" "special" "✓"
else
    track_test "autolower" "special" "✗"
fi

# NUMBERS AND MIXED TEXT
if run_test "autotools autolower '123 MIXED with UPPERCASE 456'"; then
    track_test "autolower" "mixed" "✓"
else
    track_test "autolower" "mixed" "✗"
fi

# UNICODE CHARACTERS
if run_test "autotools autolower 'ÁCCÊNTS ÀND ÉMOJIS 🚀 ⭐'"; then
    track_test "autolower" "unicode" "✓"
else
    track_test "autolower" "unicode" "✗"
fi

echo -e "\n=== Testing autopassword ==="
# BASIC PASSWORD
if run_test "autotools autopassword"; then
    track_test "autopassword" "basic" "✓"
else
    track_test "autopassword" "basic" "✗"
fi

# CUSTOM LENGTH PASSWORD
if run_test "autotools autopassword --length 32"; then
    track_test "autopassword" "length" "✓"
else
    track_test "autopassword" "length" "✗"
fi

# PASSWORD WITHOUT SPECIAL CHARS
if run_test "autotools autopassword --no-special"; then
    track_test "autopassword" "no-special" "✓"
else
    track_test "autopassword" "no-special" "✗"
fi

# PASSWORD WITHOUT NUMBERS
if run_test "autotools autopassword --no-numbers"; then
    track_test "autopassword" "no-numbers" "✓"
else
    track_test "autopassword" "no-numbers" "✗"
fi

# PASSWORD WITHOUT UPPERCASE
if run_test "autotools autopassword --no-uppercase"; then
    track_test "autopassword" "no-uppercase" "✓"
else
    track_test "autopassword" "no-uppercase" "✗"
fi

# CUSTOM MINIMUM SPECIAL CHARS
if run_test "autotools autopassword --min-special 3"; then
    track_test "autopassword" "min-special" "✓"
else
    track_test "autopassword" "min-special" "✗"
fi

# CUSTOM MINIMUM NUMBERS
if run_test "autotools autopassword --min-numbers 3"; then
    track_test "autopassword" "min-numbers" "✓"
else
    track_test "autopassword" "min-numbers" "✗"
fi

# PASSWORD WITH ANALYSIS
if run_test "autotools autopassword --analyze"; then
    track_test "autopassword" "analysis" "✓"
else
    track_test "autopassword" "analysis" "✗"
fi

# GENERATE ENCRYPTION KEY
if run_test "autotools autopassword --gen-key"; then
    track_test "autopassword" "encryption" "✓"
else
    track_test "autopassword" "encryption" "✗"
fi

echo -e "\n=== Testing autoip ==="
# BASIC NETWORK INFO
if run_test "autotools autoip --no-ip"; then
    track_test "autoip" "basic" "✓"
else
    track_test "autoip" "basic" "✗"
fi

# BASIC TESTS
if run_test "autotools autoip --test"; then
    track_test "autoip" "connectivity" "✓"
else
    track_test "autoip" "connectivity" "✗"
fi

# DNS INFO
if run_test "autotools autoip --dns"; then
    track_test "autoip" "dns" "✓"
else
    track_test "autoip" "dns" "✗"
fi

# PORT CHECK
if run_test "autotools autoip --ports"; then
    track_test "autoip" "ports" "✓"
else
    track_test "autoip" "ports" "✗"
fi

echo -e "\n=== Testing autotranslate ==="
# BASIC TRANSLATION WITH DETECTION
if run_test "autotools autotranslate 'Hello world' --to fr --detect"; then
    track_test "translate" "detection" "✓"
else
    track_test "translate" "detection" "✗"
fi

# SIMPLE TRANSLATION
if run_test "autotools autotranslate 'Bonjour le monde' --to en"; then
    track_test "translate" "basic" "✓"
else
    track_test "translate" "basic" "✗"
fi

# MULTI-LANGUAGE
if run_test "autotools autotranslate 'I love programming' --from en --to fr" && \
   run_test "autotools autotranslate 'I love programming' --from en --to es" && \
   run_test "autotools autotranslate 'I love programming' --from en --to de"; then
    track_test "translate" "multi-lang" "✓"
else
    track_test "translate" "multi-lang" "✗"
fi

echo -e "\n=== Testing autospell ==="
# BASIC SPELL CHECK
if run_test "autotools autospell 'This is a test with misspellings'"; then
    track_test "autospell" "basic" "✓"
else
    track_test "autospell" "basic" "✗"
fi

# MULTI-LANGUAGE SPELL CHECK
if run_test "autotools autospell --lang fr 'Ceci est un teste avec des fautes'"; then
    track_test "autospell" "multi-lang" "✓"
else
    track_test "autospell" "multi-lang" "✗"
fi

# JSON OUTPUT
if run_test "autotools autospell 'This is a test' --json"; then
    track_test "autospell" "json" "✓"
else
    track_test "autospell" "json" "✗"
fi

echo -e "\n=== Testing autodownload ==="
cd /data/downloads

# YOUTUBE VIDEO DOWNLOAD
if simulate_input | run_test "autotools autodownload 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' --format mp4 --quality 720p"; then
    track_test "download" "video-720p" "✓"
else
    track_test "download" "video-720p" "✗"
fi

if simulate_input | run_test "autotools autodownload 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' --format mp4 --quality 1080p"; then
    track_test "download" "video-1080p" "✓"
else
    track_test "download" "video-1080p" "✗"
fi

# AUDIO DOWNLOAD
if simulate_input | run_test "autotools autodownload 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' --format mp3"; then
    track_test "download" "audio" "✓"
else
    track_test "download" "audio" "✗"
fi

# DIRECT FILE DOWNLOAD
if run_test "autotools autodownload 'https://www.gnu.org/licenses/gpl-3.0.txt'"; then
    track_test "download" "direct" "✓"
else
    track_test "download" "direct" "✗"
fi

# DISPLAY FINAL RESULTS TABLE
display_results_table

echo -e "\nAll tests completed!" 
