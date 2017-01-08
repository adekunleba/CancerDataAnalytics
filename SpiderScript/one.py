# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:54:18 2017

@author: ADEKUNLE
"""

"""
Testing the __name__ = "__main__" function in python

"""
def func():
    print("func() in one.py")
print("top_level in one.py")
if __name__ == "__main__":
    print("one.py is being executed directly")
else:
    print("one.py is being imported")