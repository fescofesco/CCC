# Quick check - run collision check and capture just failures
import subprocess
result = subprocess.run(
    ['python', 'check_asteroid_collision.py'],
    capture_output=True,
    text=True,
    cwd=r'c:\Users\felix\CCC\CCC\Challenge 2025\Felix\level5'
)

# Print only lines with COLLISION or ERROR
for line in result.stdout.split('\n'):
    if 'COLLISION' in line or 'ERROR' in line or 'FAILED' in line:
        print(line)
