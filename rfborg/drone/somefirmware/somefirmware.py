from sympy import *
import numpy as np

def sayHi():
    print("Hi! 🙋")

def sayBye():
    print("Bye! 💁")

def count():
    for i in range(10):
        print(bin(i))

def eig():
    X=Matrix((10*np.random.rand(3,3)).astype("int"))
    pprint(X)
    i=1
    for lmda in X.eigenvals().keys():
        print(f"λ_{i}={N(lmda)}")
        i+=1
