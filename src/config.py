'''
Shared scheduling constants.

Change DAILY_LOAD_CAP here to adjust how many reviews per day the system
considers "overloaded" — affects both per-mark load smoothing (mark.py)
and the rebalance command (rebalance.py).
'''

DAILY_LOAD_CAP = 4
