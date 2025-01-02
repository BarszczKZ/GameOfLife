import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

class LangstonsAnt:
    def __init__(self, width=100,height=100):
        self.width=width
        self.height=height
        self.grid=np.zeros(height,width)
        
