# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:58:58 2017

@author: ADEKUNLE
"""

import one

print("top level in two.py")
one.func() #calling the method in module one

if __name__ == "__main__":
    print("two.py is being executed directly")
else:
    print("two.py is being imported")