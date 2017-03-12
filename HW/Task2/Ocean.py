import numpy as np
import scipy
import pandas as pd
import random


class Predator:
    def __init__(self, hungry_time, birth_time):
        self.hungry_time = hungry_time
        self.birth_time = birth_time
        self.cur_hunger = hungry_time
        self.cur_lifetime = 0

    def __str__(self):
        return 'Predator' + str((self.cur_hunger, self.cur_lifetime))

    def is_alive(self):
        return self.cur_hunger > 0

    def need_child(self):
        return self.cur_lifetime >= self.birth_time


class Victim:
    def __init__(self, birth_time):
        self.birth_time = birth_time
        self.cur_lifetime = 0

    def __str__(self):
        return 'Victim(' + str(self.cur_lifetime) + ')'

    def need_child(self):
        return self.cur_lifetime == self.birth_time


class Ocean:
    def __init__(self, data):
        self.ocean = data
        self.ocean_shape = data.shape
        self.victims_number = len(list(filter(lambda elem:
                                              isinstance(elem, Victim),
                                              self.ocean.ravel())))
        self.predators_number = len(list(filter(lambda elem:
                                                isinstance(elem, Predator),
                                                self.ocean.ravel())))

    def __str__(self):
        return str(self.ocean.astype(str))

    def go(self, pos):
        print("POS", pos)
        if isinstance(self.ocean[pos[0]][pos[1]], int):
            return

        is_predator = False
        if isinstance(self.ocean[pos[0]][pos[1]], Predator):
            is_predator = True
            self.ocean[pos[0]][pos[1]].cur_hunger -= 1

        self.ocean[pos[0]][pos[1]].cur_lifetime += 1
        need_child = False
        if self.ocean[pos[0]][pos[1]].need_child():
            need_child = True
            self.ocean[pos[0]][pos[1]].cur_lifetime = 0

        free_cells = set()
        victim_cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j:
                    continue
                elif (0 <= pos[0] + i < self.ocean_shape[0]) \
                        and (0 <= pos[1] + j < self.ocean_shape[1]):
                    neighbor = self.ocean[pos[0] + i][pos[1] + j]
                    if neighbor == 0:
                        free_cells.add((pos[0] + i,
                                        pos[1] + j))
                    elif isinstance(neighbor, Victim):
                        # Victim
                        victim_cells.add((pos[0] + i,
                                          pos[1] + j))

        if need_child and len(free_cells):
            child_pos = random.sample(free_cells, 1)[0]
            free_cells.remove(child_pos)
            if is_predator:
                self.predators_number += 1
                self.ocean[child_pos[0]][child_pos[1]] = \
                    Predator(self.hungry_time, self.birth_time)
            else:
                self.victims_number += 1
                self.ocean[child_pos[0]][child_pos[1]] = \
                    Victim(self.birth_time)

        new_pos = None
        if is_predator:
            available_cells = free_cells | victim_cells
            if len(available_cells):
                new_pos = random.sample(available_cells, 1)[0]
                print('PREDATOR', new_pos)
            else:
                if self.ocean[pos[0]][pos[1]].is_alive() is False:
                    self.predators_number -= 1

                    self.ocean[pos[0]][pos[1]] = 0

                return
        else:
            if len(free_cells):
                new_pos = random.sample(free_cells, 1)[0]
                print('VICTIM', new_pos)
            else:
                return

        if is_predator:
            if isinstance(self.ocean[new_pos[0]][new_pos[1]],
                          Victim):
                self.ocean[pos[0]][pos[1]].cur_hunger = \
                    self.ocean[pos[0]][pos[1]].hungry_time
                self.victims_number -= 1
            else:
                if self.ocean[pos[0]][pos[1]].is_alive() is False:
                    self.predators_number -= 1

                    self.ocean[pos[0]][pos[1]] = 0
                    return

        self.ocean[new_pos[0]][new_pos[1]] = self.ocean[pos[0]][pos[1]]
        self.ocean[pos[0]][pos[1]] = 0

    def simulate(self, iter_number=100):

        for iter_num in range(iter_number):
            for i in range(self.ocean.shape[0]):
                for j in range(self.ocean.shape[1]):
                    self.go((i, j))
                    print(self)

            if self.victims_number == 0 or self.predators_number == 0:
                print('Somebody dead',
                      'Victims = ', self.victims_number,
                      ' Predators = ', self.predators_number)
                break
