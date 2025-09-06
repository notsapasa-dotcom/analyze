import subprocess

def test_top_5_words():
    result = subprocess.run(
        ["python", "analyze.py", "--top", "5"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    # Adjust these lines to match your actual output if needed
    assert "divine: 47" in output
    assert "signal: 40" in output
    assert "sacred: 40" in output
    assert "tone: 40" in output
    assert "god: 35" in output

def test_unique_olo():
    result = subprocess.run(
        ["python", "analyze.py", "--unique", "olo"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "Unique words containing 'olo':" in output
    assert "pathologize" in output
    assert "pathologizes" in output
    assert "theological" in output

def test_grams_3_priestess():
    result = subprocess.run(
        ["python", "analyze.py", "--grams", "3", "priestess"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "Unique 3-grams starting with 'priestess':" in output
    assert "priestess frequency itself: 1" in output
    assert "priestess path always: 1" in output
    assert "priestess path transmitter: 1" in output
    assert "priestess prophet role: 1" in output
    assert "priestess quiet flame: 1" in output
    assert "priestess understand people: 1" in output
