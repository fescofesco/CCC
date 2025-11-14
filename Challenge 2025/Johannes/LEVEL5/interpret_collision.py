"""
Check if the issue is about WHEN we check the position.

Question: Do we check collision:
A) BEFORE applying the pace movement?
B) AFTER applying the pace movement?
C) BOTH?
"""

x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]
ax, ay = 3, 0

print("Interpretation A: Check BEFORE each pace is applied")
print("="*80)
x_pos, y_pos = 0, 0

# Check initial position
dist = max(abs(x_pos - ax), abs(y_pos - ay))
print(f"Initial: ({x_pos},{y_pos}) dist={dist} {'✅' if dist > 2 else '❌'}")

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    # Apply movement FIRST
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    # Then check position
    dist = max(abs(x_pos - ax), abs(y_pos - ay))
    status = "✅" if dist > 2 else "❌ COLLISION!"
    print(f"After pace {i}: ({x_pos},{y_pos}) dist={dist} {status}")

print("\n" + "="*80)
print("Interpretation B: The spaceship itself has a radius")
print("="*80)
print("Maybe the SPACESHIP has a safety radius, not the asteroid?")
print("Let me re-read the mission...")

with open(r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5\Level5_Mission.txt', 'r') as f:
    content = f.read()
    
# Find the collision section
collision_section = content[content.find("Asteroid Collision"):content.find("Input Format")]
print(collision_section)
