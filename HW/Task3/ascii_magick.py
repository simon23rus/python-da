import argparse

image_alphabet = dict(list(zip(list("@%#*+=-:. "), list(range(10)))))
bri_to_alphabet = {v: k for k, v in image_alphabet.items()}


def crop(parsed, data):
    left = parsed.left
    right = parsed.right
    top = parsed.top
    bottom = parsed.bottom
    n, m = len(data), len(data[0])
    data = data[top: n - bottom]
    for i in range(len(data)):
        data[i] = data[i][left: m - right]

    return data


def expose(parsed, data):
    brightness = parsed.brightness
    for i in range(len(data)):
        for j in range(len(data[i])):
            sym = data[i][j]
            new_brightness = image_alphabet[sym] + brightness
            if new_brightness < 0:
                new_brightness = 0
            elif new_brightness > 9:
                new_brightness = 9
            data[i][j] = bri_to_alphabet[new_brightness]
    return data


def rotate(parsed, data):
    angle = parsed.angle
    iter_number = (angle // 90) % 4
    n, m = len(data), len(data[0])
    new_data = data
    for _ in range(iter_number):
        n, m = m, n
        new_data = []
        for i in range(n):
            new_data.append([0] * m)

        for i in range(m):
            for j in range(n):
                new_data[n - j - 1][i] = data[i][j]
        data = new_data
    return new_data


def main():

    with open('./input.txt', 'r') as f:
        data = f.read().splitlines()

    args = data[0].split()
    data = list(map(list, data[1:]))
    mode, args = args[0], args[1:]
    parser = argparse.ArgumentParser()
    if mode == 'crop':
        parser.add_argument('--left', '-l', type=int, default=0)
        parser.add_argument('--right', '-r', type=int, default=0)
        parser.add_argument('--top', '-t', type=int, default=0)
        parser.add_argument('--bottom', '-b', type=int, default=0)
        parsed = parser.parse_args(args)
        data = crop(parsed, data)

    elif mode == 'expose':
        parser.add_argument('brightness', type=int)
        parsed = parser.parse_args(args)
        data = expose(parsed, data)

    elif mode == 'rotate':
        parser.add_argument('angle', type=int)
        parsed = parser.parse_args(args)
        data = rotate(parsed, data)

    print('\n'.join(list(map(lambda elem: ''.join(elem), data))))


if __name__ == '__main__':
    main()
