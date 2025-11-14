# Official Validator - Extracted from visualizer.html

## Summary

This validator implements the **exact same validation logic** used by the official CCC Challenge 2025 visualizer.html tool. It validates:

1. **Pace Sequence Rules**:
   - First and last pace must be 0
   - Paces must be 0 or in range ±1 to ±5
   - Cannot change direction without 0 in between
   - Pace transitions must follow valid progressions

2. **Movement Simulation**:
   - Expands paces (each pace value repeated |pace| times)
   - Simulates tick-by-tick movement using the Entity.move() logic
   - Tracks position history at every step

3. **Collision Detection**:
   - Uses AREA_COLLISION = 2 (from visualizer)
   - Collision occurs when BOTH dx ≤ 2 AND dy ≤ 2
   - Checks every step in the path

4. **Goal Validation**:
   - Verifies final position matches target
   - Ensures ship stops (velocity = 0) at goal

## Key Constants (from visualizer.html)

```javascript
const MIN_PACE = 5;
const MAX_PACE = 1;
const AREA_COLLISION = 2;
```

## Validation Results for level5_1_small.out

**Total Cases**: 20
**Valid Cases**: 19 ✅
**Failed Cases**: 1 ❌

### Failed Case

**Case 15**: Target (11, 4), Asteroid (6, 2)
- ❌ **Collision at step 21**
- Ship position: (4, 4)
- Asteroid position: (6, 2)
- Distance: dx=2, dy=2 (both ≤ 2 → COLLISION)

## Usage

### Test specific case:
```bash
python official_validator.py
```

### Validate entire output file:
```bash
python official_validator.py <input_file> <output_file>
```

### Example:
```bash
python official_validator.py "C:/path/to/level5_1_small.in" "C:/path/to/level5_1_small.out"
```

## How Movement Works (from visualizer.html)

The visualizer uses a **tick-based system**:

1. Each pace value is **expanded**: pace value is repeated |pace| times (minimum 1)
   - Example: `[0, 5, -3, 0]` → `[0, 5, 5, 5, 5, 5, -3, -3, -3, 0]`

2. For each expanded pace, the Entity.move() function:
   - Increments tick counter
   - When ticks reach |pace|, moves position by ±1
   - Resets tick counter

3. Position is recorded at **every step** (after each tick increment)

## Verification

This validator has been tested against the visualizer and produces identical results:
- ✅ Detects collision at step 21 for case 15
- ✅ Validates all other 19 cases successfully
- ✅ Uses exact same pace validation rules
- ✅ Uses exact same movement simulation
- ✅ Uses exact same collision detection (Chebyshev distance ≤ 2)

## Next Steps

To fix case 15, the `pad_sequences_to_avoid_asteroid()` function in `level5.py` needs to:
1. Generate alternative paths that avoid position (4,4) at any step
2. Use the official validator to verify the new path
3. Ensure the path stays MORE than 2 tiles away from asteroid (6,2) at all times
