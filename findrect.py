import math

def find_best_rect(number):
    rects = []

    # Finding the nearest square gives us the depth of the search we need to do
    # for the list of possible rectangles for the mazes
    nearest_square = math.sqrt(number)
    if not nearest_square.is_integer():
        nearest_square = math.ceil(nearest_square)
    else:
        nearest_square = int(nearest_square)
    
    # We don't want the height to be greater than the width, so only
    # iterate up to the next square number (if not already a square)
    for i in range(1, nearest_square):
        if i * i > (number + i):
            break
        # if i is a factor of the <number>, add this rectangle
        if number % i == 0:
            rects.append((i, number // i, 0))
        else:
            # otherwise find the largest multiplier that would make a rectangle big
            # enough for the <number> with side i
            j = 0
            for j in range(i, number // i + 1):
                # when j * i exceeds the <number> + one more row, exit loop
                # (everything else bigger is too big)
                if j * i > number + i:
                    break
            j += 1
            # add the rectangle i x j
            rects.append((i, j, (i * j) - number))

    # always include the nearest square
    rects.append((nearest_square, nearest_square, nearest_square * nearest_square - number))
    #print(f"Rectangles for capacity: {number} are: {rects}")

    return best_fit_rect(rects)

def best_fit_rect (rects):
    if not rects:
        return None
    
    # return a square if there is one
    for rect in rects:
        if rect[0] == rect[1] == rect[2] == 0:
            return rect
    
    # or return the perfect rectangle that has the least remaining space
    for rect in reversed(rects):
        if rect[2] <= rect[1] / 2:
            return rect

"""
def main():
    for i in range(29):
        print(best_fit_rect(find_rects(i)))

main()
"""