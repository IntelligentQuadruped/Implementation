def convertToCommand(float_in):
    """Takes in command in float form and encodes command as two digit string."""
    int_in = int(float_in * 10)
    first_digit = 0 if int_in < 0 else 1 #encodes negative
    second_digit = abs(int_in) #only consider magnitude
    return (first_digit, second_digit)

def command(**kwargs):
    """Converts command input to 8 byte integer.
    Takes arguments as follows:
        behavior    [int]       0 to 9,
        forward     [float]  -0.9 to 0.9,
        turn        [float]  -0.9 to 0.9,
        height      [float]  -0.9 to 0.9
    """
    new_command = list("90000000")

    for key in kwargs:
        if key == 'forward':
            new_command[2:4] = convertToCommand(kwargs[key])
        elif key == 'turn':
            new_command[4:6] = convertToCommand(kwargs[key])
        elif key == 'height':
            new_command[6:8] = convertToCommand(kwargs[key])
        elif key == 'behavior':
            new_command[1] = int(kwargs[key])

    new_command = map(str,new_command) # converting int to char
    new_command = ''.join(new_command) # joining char to str




if __name__ == '__main__':
    command(behavior  = 1, forward = 0.3)
    command(forward = -.3, turn = 0.3)
    command(height = 0.5)