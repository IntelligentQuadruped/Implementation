"""
Author: Jan Bernhard
Last updated: 04/22/18
Purpose: Testing head.py with defined control sequence. 
"""

import head

obj = head.Head()
obj.connect()


print(">>> TEST SEQUENCE STARTED <<<")
print(">>> Testing Turn Table: Standard use")
obj.test_look(turn = -45)
obj.test_look(turn = 0)
obj.test_look(turn = 45)
obj.test_look(turn = -90)
obj.test_look(turn = 0)
obj.test_look(turn = 90)
obj.test_look(turn = 0)
print(">>> Testing Turn Table: Invalid inputs")
obj.test_look(turn = -100)
obj.test_look(turn = 100)
print(">>> Testing Turn Table: Complete")
print(">>> Testing Tilt Axis: Standard use")
obj.test_look(tilt = -15)
obj.test_look(tilt = 0)
obj.test_look(tilt = 15)
obj.test_look(tilt = -30)
obj.test_look(tilt = 0)
obj.test_look(tilt = 30)
obj.test_look(tilt = 0)
print(">>> Testing Tilt Axis: Unvalid inputs")
obj.test_look(tilt = -70)
obj.test_look(tilt = 70)
print(">>> Testing Tilt Axis: Complete")
print(">>> TEST COMPLETE <<<")