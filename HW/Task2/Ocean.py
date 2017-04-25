import random


class OceanGenerator(object):
    def __init__(self, shape):
        self.ocean_shape = shape

    def generate(self, predator_hungry, predator_birth, victim_birth):
        new_ocean = []
        for i in range(self.ocean_shape[0]):
            to_push = []
            positions = [random.randint(0, 3)
                         for _ in range(self.ocean_shape[1])]
            for pos in positions:
                if pos == 0:
                    to_push.append(0)
                elif pos == 1:
                    to_push.append(1)
                elif pos == 2:
                    to_push.append(Predator(predator_hungry, predator_birth))
                else:
                    to_push.append(Victim(victim_birth))

            new_ocean.append(to_push)

        return new_ocean


class Predator(object):
    def __init__(self, hungry_time, birth_time):
        self.hungry_time = hungry_time
        self.birth_time = birth_time
        self.cur_hunger = hungry_time
        self.cur_lifetime = 0

    def __str__(self):
        # return 'Predator' + str((self.cur_hunger, self.cur_lifetime))
        return 'P'

    def is_alive(self):
        return self.cur_hunger > 0

    def need_child(self):
        if self.cur_lifetime == self.birth_time:
            return True
        else:
            return False

    def span_child(self):
        return Predator(self.hungry_time, self.birth_time)


class Victim(object):
    def __init__(self, birth_time):
        self.birth_time = birth_time
        self.cur_lifetime = 0

    def __str__(self):
        # return 'Victim(' + str(self.cur_lifetime) + ')'
        return 'V'

    def need_child(self):
        if self.cur_lifetime == self.birth_time:
            return True
        else:
            return False

    def span_child(self):
        return Victim(self.birth_time)


class Ocean:
    def __init__(self, data):
        self.ocean = data
        self.ocean_shape = (len(data), len(data[0]))
        self.victims_number = 0
        self.predators_number = 0

        for i in range(self.ocean_shape[0]):
            for j in range(self.ocean_shape[1]):

                if isinstance(self.ocean[i][j], Victim):
                    self.victims_number += 1
                elif isinstance(self.ocean[i][j], Predator):
                    self.predators_number += 1

        self.predators_history = [self.predators_number]
        self.victims_history = [self.victims_number]

        self.snapshot = generate_ones(self.ocean_shape)

    def __getitem__(self, indices):
        return self.ocean[indices[0]][indices[1]]

    def __setitem__(self, indices, value):
        self.ocean[indices[0]][indices[1]] = value

    def print_ocean(self):
        res = ''
        for i in range(self.ocean_shape[0]):
            res += ' '.join(map(str, self.ocean[i])) + '\n'

        print(res + '\n\n')

    def get_neighbours(self, pos):
        free_cells = set()
        victim_cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j:
                    continue

                if (0 <= pos[0] + i < self.ocean_shape[0]) \
                        and (0 <= pos[1] + j < self.ocean_shape[1]):
                    neighbor = self.ocean[pos[0] + i][pos[1] + j]
                    if neighbor == 0:
                        free_cells.add((pos[0] + i,
                                        pos[1] + j))
                    elif isinstance(neighbor, Victim):
                        victim_cells.add((pos[0] + i,
                                          pos[1] + j))

        return free_cells, victim_cells

    def span_child(self, pos, free_cells, is_predator):
        child_pos = random.sample(free_cells, 1)[0]
        free_cells.remove(child_pos)
        if is_predator:
            self.predators_number += 1
            self[child_pos] = self[pos].span_child()
        else:
            self.victims_number += 1
            self[child_pos] = self[pos].span_child()

    def process_new_pos(self, pos, free_cells, victim_cells, is_predator):
        if is_predator:
            available_cells = free_cells | victim_cells
            if len(available_cells):
                new_pos = random.sample(available_cells, 1)[0]
            else:
                if not self[pos].is_alive():
                    self.predators_number -= 1

                    self[pos] = 0

                return
        else:
            if len(free_cells):
                new_pos = random.sample(free_cells, 1)[0]
            else:
                return

        return new_pos

    def update_properties_before_move(self, pos, new_pos):
        if isinstance(self[new_pos], Victim):
            self[pos].cur_hunger = self[pos].hungry_time
            self.victims_number -= 1
        else:
            if not self[pos].is_alive():
                self.predators_number -= 1
                self[pos] = 0

    def go(self, pos):
        if isinstance(self[pos], int):
            return

        is_predator = False
        if isinstance(self[pos], Predator):
            is_predator = True
            self[pos].cur_hunger -= 1

        self[pos].cur_lifetime += 1

        free_cells, victim_cells = self.get_neighbours(pos)

        if self[pos].need_child() and len(free_cells) is not 0:
            self[pos].cur_lifetime = 0
            self.span_child(pos, free_cells, is_predator)

        new_pos = self.process_new_pos(pos, free_cells, victim_cells, is_predator)

        if new_pos is None:
            return

        self.snapshot[new_pos[0]][new_pos[1]] = 0  # HERE ASSIGN SNAPSHOT VALUE

        if is_predator:
            self.update_properties_before_move(pos, new_pos)

        self[new_pos] = self[pos]
        self[pos] = 0

    def simulate(self, iter_number=100, need_vizualization=False):
        self.print_ocean()

        for iter_num in (range(iter_number)):
            self.snapshot = generate_ones(self.ocean_shape)
            for i in range(self.ocean_shape[0]):
                for j in range(self.ocean_shape[1]):
                    if self.snapshot[i][j] == 0:
                        continue

                    self.go((i, j))

            if need_vizualization:
                self.print_ocean()
            self.predators_history.append(self.predators_number)
            self.victims_history.append(self.victims_number)

            if self.victims_number == 0 or self.predators_number == 0:
                print('Somebody dead at {} iteration'.format(iter_num),
                      'Victims = ', self.victims_number,
                      ' Predators = ', self.predators_number)
                break


def generate_ones(shape):
    ''' Create array of ones with given shape

        Parameters
        ----------
        shape: tuple

        Returns
        -------
        list
             matrix with shape, containing only ones
    '''
    res = []
    for i in range(shape[0]):
        res.append([1] * shape[1])
    return res


def start_simulation(shape, hungry_time,
                     predator_birth, victim_birth, iter_num,
                     need_vizualization=False):
    ocean_generator = OceanGenerator(shape)
    cells = ocean_generator.generate(hungry_time, predator_birth, victim_birth)
    ocean = Ocean(cells)
    ocean.simulate(iter_num, need_vizualization)

    return ocean


def main():
    shape = (5, 5)
    citizens = [Predator(20, 10), Victim(10), 0, 1]
    ocean_generator = OceanGenerator(shape)
    cells = ocean_generator.generate(20, 10, 10)

    ocean = Ocean(cells)
    ocean.simulate()


if __name__ == '__main__':
    main()
