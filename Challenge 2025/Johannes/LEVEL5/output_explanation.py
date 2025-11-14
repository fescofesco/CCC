"""
EXPLANATION OF LEVEL 5 OUTPUT FORMAT
=====================================

Input for case 1:
- Target station: (6, 0)
- Time limit: 118
- Asteroid at: (3, 0)

Output (two lines):
Line 1 (X sequence): 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 4 3 3 4 5 0
Line 2 (Y sequence): 0 5 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -5 -4 -5 0

WHAT EACH NUMBER MEANS:
-----------------------

Each number is a "PACE" value that controls movement:

PACE RULES:
- Pace = 0: Stay in place for 1 time unit
- Pace > 0: Move +1 position, costs |pace| time units
- Pace < 0: Move -1 position, costs |pace| time units

For example:
- Pace 5: Move +1 position, takes 5 time units
- Pace -3: Move -1 position, takes 3 time units
- Pace 0: Stay in place, takes 1 time unit

TRANSITION RULES (from Level 3):
- Must start and end with pace 0
- From pace 0, can only go to ±5
- To pace 0, can only come from ±5
- Between non-zero paces, can only change by ±1

HOW THE SEQUENCES WORK TOGETHER:
---------------------------------

The X and Y sequences execute IN PARALLEL. At each step:
- Read the next pace from X sequence → affects X position
- Read the next pace from Y sequence → affects Y position
- Both happen simultaneously in 2D space

Let me trace through case 1:

Step  | X pace | Y pace | Action                    | Position | Time
------|--------|--------|---------------------------|----------|------
  0   |   0    |   0    | Both start at rest        | (0, 0)   |  0
  1   |   0    |   5    | X waits, Y moves up (+1)  | (0, 1)   |  1+5=6
  2   |   0    |   4    | X waits, Y moves up (+1)  | (0, 2)   |  6+4=10
  3   |   0    |   5    | X waits, Y moves up (+1)  | (0, 3)   |  10+5=15
  4   |   0    |   0    | Both wait                 | (0, 3)   |  15+1=16
  5-14|   0    |   0    | Both keep waiting         | (0, 3)   |  16→25
 15   |   5    |   0    | X moves right (+1), Y waits| (1, 3)  |  25+5=30 (but max=30)
 16   |   4    |   0    | X moves right (+1), Y waits| (2, 3)  |  30+4=34 (but max=34)
 17   |   3    |   0    | X moves right (+1), Y waits| (3, 3)  |  34+3=37 (but max=37)
 18   |   3    |   0    | X moves right (+1), Y waits| (4, 3)  |  37+3=40 (but max=40)
 19   |   4    |   0    | X moves right (+1), Y waits| (5, 3)  |  40+4=44 (but max=44)
 20   |   5    |   0    | X moves right (+1), Y waits| (6, 3)  |  44+5=49 (but max=49)
 21   |   0    |   0    | Both wait                 | (6, 3)   |  49+1=50
22-27 |   0    |   0    | Both keep waiting         | (6, 3)   |  50→56
 28   |   0    |  -5    | X waits, Y moves down (-1)| (6, 2)   |  56+5=61
 29   |   0    |  -4    | X waits, Y moves down (-1)| (6, 1)   |  61+4=65
 30   |   0    |  -5    | X waits, Y moves down (-1)| (6, 0)   |  65+5=70
 31   |   0    |   0    | Both at rest (END)        | (6, 0)   |  70+1=71

FINAL RESULT:
- Starting position: (0, 0)
- Ending position: (6, 0) ✓ (matches target)
- Total time: 71 (well under limit of 118) ✓
- Asteroid at (3, 0) avoided by going around via (0,3) → (6,3) → (6,0) ✓

KEY INSIGHTS:
-------------

1. The sequences don't need to be the same length - they run in parallel
2. Time advances by max(x_pace_cost, y_pace_cost) at each step
3. The zeros create "waiting" - one axis pauses while the other moves
4. The path in 2D space is: (0,0) → up to (0,3) → right to (6,3) → down to (6,0)
5. This avoids the asteroid at (3,0) which would collide with any point where 
   max(|x-3|, |y-0|) ≤ 2 (Chebyshev distance)

WHY OUR OUTPUT DIFFERS:
-----------------------

Our generated output has the SAME path but LESS waiting:
- We move X immediately after Y reaches (0,3)
- We move Y down immediately after X reaches (6,3)
- No extra wait periods

Both solutions are VALID - they both:
✓ Reach the target
✓ Avoid the asteroid
✓ Follow all pace transition rules
✓ Stay within time limit

The difference is just timing optimization/preference!
"""

print(__doc__)
