git clone https://github.com/GreatestTrain/pybooru.git

cd pybooru

set PYTHON "$(command python | select-object source -expandproperty source)"

if (!$PYTHON) {
    echo "======================================"
    echo "There's no python :c"
    echo "Installing python without your consent"
    echo "======================================"
    winget install python
    set PYTHON "$(command python | select-object source -expandproperty source)"
}

echo "Installing to ${PYTHON}"

# cd ..
echo $(pwd)
set PYTHON_CMD "${PYTHON} -m pip install src/"
# cd ..

Invoke-Expression ${PYTHON_CMD}

cd ..

echo "========================="
echo " run tests?"
echo "========================="
echo "[Y/N]"

set RESPONSE $(Read-Host)
set PYTHON_CMD_ "${PYTHON} ./pybooru/test/safebooru_test.py"
set PYTHON_CMD__ "${PYTHON} ./pybooru/test/wallhaven_test.py"

if ( $RESPONSE -eq "Y" ) {
    echo "Running safebooru_test"
    Invoke-Expression $PYTHON_CMD_
    echo "Running wallhaven_test"
    Invoke-Expression $PYTHON_CMD__
}

echo "Done"

