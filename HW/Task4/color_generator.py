#!/usr/bin/env python3
import random


class ColorGenerator:
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F']

    def get_color(self):
        '''
        Returns hex-color, string
        '''
        color = '#'
        for i in range(6):
            index = 0
            for j in range(1000):
                index = random.randint(0, 15)
            color += (self.symbols[index])
        return color
