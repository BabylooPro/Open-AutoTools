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
    local categories=("Text" "Security" "Network")
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
    track_test "autocaps" "basic" "OK"
else
    track_test "autocaps" "basic" "X"
fi

# SPECIAL CHARACTERS
if run_test "autotools autocaps 'special chars: !@#$%^&*()'"; then
    track_test "autocaps" "special" "OK"
else
    track_test "autocaps" "special" "X"
fi

# NUMBERS AND MIXED TEXT
if run_test "autotools autocaps '123 mixed WITH lowercase 456'"; then
    track_test "autocaps" "mixed" "OK"
else
    track_test "autocaps" "mixed" "X"
fi

# UNICODE CHARACTERS
if run_test "autotools autocaps 'áccênts ànd émojis 🚀 ⭐'"; then
    track_test "autocaps" "unicode" "OK"
else
    track_test "autocaps" "unicode" "X"
fi

echo -e "\n=== Testing autolower ==="
# BASIC USAGE
if run_test "autotools autolower 'TEST WITH MULTIPLE WORDS'"; then
    track_test "autolower" "basic" "OK"
else
    track_test "autolower" "basic" "X"
fi

# SPECIAL CHARACTERS
if run_test "autotools autolower 'SPECIAL CHARS: !@#$%^&*()'"; then
    track_test "autolower" "special" "OK"
else
    track_test "autolower" "special" "X"
fi

# NUMBERS AND MIXED TEXT
if run_test "autotools autolower '123 MIXED with UPPERCASE 456'"; then
    track_test "autolower" "mixed" "OK"
else
    track_test "autolower" "mixed" "X"
fi

# UNICODE CHARACTERS
if run_test "autotools autolower 'ÁCCÊNTS ÀND ÉMOJIS 🚀 ⭐'"; then
    track_test "autolower" "unicode" "OK"
else
    track_test "autolower" "unicode" "X"
fi

echo -e "\n=== Testing autopassword ==="
# BASIC PASSWORD
if run_test "autotools autopassword"; then
    track_test "autopassword" "basic" "OK"
else
    track_test "autopassword" "basic" "X"
fi

# CUSTOM LENGTH PASSWORD
if run_test "autotools autopassword --length 32"; then
    track_test "autopassword" "length" "OK"
else
    track_test "autopassword" "length" "X"
fi

# PASSWORD WITHOUT SPECIAL CHARS
if run_test "autotools autopassword --no-special"; then
    track_test "autopassword" "no-special" "OK"
else
    track_test "autopassword" "no-special" "X"
fi

# PASSWORD WITHOUT NUMBERS
if run_test "autotools autopassword --no-numbers"; then
    track_test "autopassword" "no-numbers" "OK"
else
    track_test "autopassword" "no-numbers" "X"
fi

# PASSWORD WITHOUT UPPERCASE
if run_test "autotools autopassword --no-uppercase"; then
    track_test "autopassword" "no-uppercase" "OK"
else
    track_test "autopassword" "no-uppercase" "X"
fi

# CUSTOM MINIMUM SPECIAL CHARS
if run_test "autotools autopassword --min-special 3"; then
    track_test "autopassword" "min-special" "OK"
else
    track_test "autopassword" "min-special" "X"
fi

# CUSTOM MINIMUM NUMBERS
if run_test "autotools autopassword --min-numbers 3"; then
    track_test "autopassword" "min-numbers" "OK"
else
    track_test "autopassword" "min-numbers" "X"
fi

# PASSWORD WITH ANALYSIS
if run_test "autotools autopassword --analyze"; then
    track_test "autopassword" "analysis" "OK"
else
    track_test "autopassword" "analysis" "X"
fi

# GENERATE ENCRYPTION KEY
if run_test "autotools autopassword --gen-key"; then
    track_test "autopassword" "encryption" "OK"
else
    track_test "autopassword" "encryption" "X"
fi

# TODO FIX: ENSURE NO IP ADDRESSES OR SENSITIVE INFORMATION ARE EXPOSED IN WORKFLOW LOGS
# echo -e "\n=== Testing autoip ==="
# BASIC NETWORK INFO
# if run_test "autotools autoip --no-ip"; then
#     track_test "autoip" "basic" "OK"
# else
#     track_test "autoip" "basic" "X"
# fi

# # BASIC TESTS
# if run_test "autotools autoip --test"; then
#     track_test "autoip" "connectivity" "OK"
# else
#     track_test "autoip" "connectivity" "X"
# fi

# # DNS INFO
# if run_test "autotools autoip --dns"; then
#     track_test "autoip" "dns" "OK"
# else
#     track_test "autoip" "dns" "X"
# fi

# PORT CHECK
# if run_test "autotools autoip --ports"; then
#     track_test "autoip" "ports" "OK"
# else
#     track_test "autoip" "ports" "X"
# fi

# DISPLAY FINAL RESULTS TABLE
display_results_table

echo -e "\nAll tests completed!" 
