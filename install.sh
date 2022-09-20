#!/bin/sh

PACKAGE_DIR="./pybooru/src/"

# COLORS
BLACK="\033[0;30m"
RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
NC='\033[0m' # No Color

function error () { printf "${RED}$1${NC}\n"; return 1; }
function success () { printf "${GREEN}$1${NC}\n"; return 0; }

APP=""

function check_if_installed() {
    APP=$(which $1)
    echo -e "\n=================================="
    echo "Checking if $1 is installed..."
    if [ -z "$APP" ]
    then
        error "$1 is not installed. Use your package manager to install it."
    else
        success "$1 installed."
        echo -e "${BLUE}Using: ${APP}${NC}"
    fi
    RESULT=$?
    echo -e "=================================="
    return $RESULT
}   

function run_tests() {
    printf "${CYAN}Run tests? [Y/n]${NC}: "
    local RESPONSE=$(read -n1)
    [ -z "$RESPONSE" ] && RESPONSE="Y"
    printf "\n"
    RESPONSE=$(echo "$RESPONSE" | tr '[:lower:]' '[:upper:]')
    if [ "$RESPONSE" -eq "Y" ]
    then
        $PYTHON ./pybooru/tests/safebooru_test.py
        $PYTHON ./pybooru/tests/wallhaven_test.py
    elif [ "$RESPONSE" -eq "N" ]
    then
        return 0
    fi
    return $?
}

function clone_repository() {
    printf "${CYAN}Clonning $1 ...${NC}\n"
    check_if_installed git && git clone $1
    return $?
}

check_if_installed "python3" && PYTHON=$APP \
clone_repository "https://github.com/GreatestTrain/pybooru.git" && \
printf "${CYAN}Installing package...${NC}\n" && \
$APP -m pip install "${PACKAGE_DIR}" && run_tests

echo -e "\n"