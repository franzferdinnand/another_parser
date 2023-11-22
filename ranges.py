def ranges_for_parser(num_of_pages):
    start = 0
    stop = 0
    ranges = [(0, 30)]
    for i in range(0, num_of_pages, 30):
        start += 30
        stop = start + 30

        ranges.append((start, stop))
    return ranges


if __name__ == '__main__':
    print(ranges_for_parser(780))
