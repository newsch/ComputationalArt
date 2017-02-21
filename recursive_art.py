#!/usr/bin/env python3
"""
Computational Art Project
SoftDes Spring 2017
Evan Lloyd New-Schmidt
"""

import random
from PIL import Image
from math import cos, sin, pi


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # list of final values
    final_functions = [
        [lambda a, b: a, 'x'],
        [lambda a, b: b, 'y'],
    ]
    # list of functions with number of required arguments and names
    possible_functions = [
        [lambda a, b: a * b,         2,  'prod'],
        [lambda a, b: 0.5 * (a + b), 2,  'avg'],
        [lambda a: cos(pi * a),      1,  'cos'],
        [lambda a: sin(pi * a),      1,  'sin'],
    ]
    if max_depth <= 1 or (min_depth <= 1 and random.choice([True, False])):
        choice = random.choice(final_functions)
        print(choice[1], end=') ', flush=True)
        return lambda a, b: choice[0](a, b)
    else:
        choice = random.choice(possible_functions)
        print(choice[2], end='(', flush=True)
        next_function = choice[0]
        # generate arguments for next function
        f_args = []
        for i in range(choice[1]):  # TODO: change to single line
            f_args.append(build_random_function(min_depth - 1, max_depth - 1))
        return lambda a, b: next_function(*[f_arg(a, b) for f_arg in f_args])


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_ratio = (val - input_interval_start) \
        / (input_interval_end - input_interval_start)
    output_val = input_ratio * (output_interval_end - output_interval_start) \
        + output_interval_start
    return output_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    print('red function:')
    red_function = build_random_function(7, 9)
    print('\ngreen function:')
    green_function = build_random_function(7, 9)
    print('\nblue function:')
    blue_function = build_random_function(7, 9)
    print()

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function(x, y)),
                    color_map(green_function(x, y)),
                    color_map(blue_function(x, y))
                    )

    im.save(filename)


def get_an_uncontroversial_filename(base_string='myart',
                                    destination='output/',
                                    extension='.png'):
    """ Find a filename that won't overwrite existing art.

        Do this in a roudabout way of finding all the current art files that
        follow a convention of base_string + an_int + extension in the
        destination folder, finding the largest an_int, and +1-ing that to get
        the returned filename.

        The irony of this is that in the process of writing
        and testing this function many arts were created and overwritten.

        returns: filename as a string
    """
    import glob
    files = glob.glob(destination + 'myart*.png')  # get all files of pattern
    # parse number out of filename and get biggest one
    big_int = 1
    for filename in files:
        int_begin = filename.rfind(base_string) + len(base_string)
        int_end = filename.find(extension)
        new_int = filename[int_begin:int_end]
        # check to make sure this is really an int and if it's bigger or not
        if new_int.isdigit():
            new_int = int(new_int)
            if new_int > big_int:
                big_int = new_int

    bigger_int = big_int + 1  # make a bigger int for the new filename
    an_uncontroversial_filename = destination + base_string \
        + str(bigger_int) + extension
    return(an_uncontroversial_filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art(get_an_uncontroversial_filename())

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
