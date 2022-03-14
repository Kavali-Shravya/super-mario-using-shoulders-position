import pynput

# intiallizing the keyboard controller for acessing the keyboard interface
keyboard = pynput.keyboard.Controller()

key = None
space_pressed = False

def do_nothing():
    print('DO Nothing')

def move_left():
    print('LEFT')
    key = 'a'
    for i in range(150):
        keyboard.press(key)
    keyboard.release(key)

def move_right():
    print('Right')
    key = 'd'
    for i in range(150):
        keyboard.press(key)
    keyboard.release(key)

def jump():
    print("Space pressed")
    keyboard.press(pynput.keyboard.Key.space)
    keyboard.release(pynput.keyboard.Key.space)

def jump_right():
    print('JUMP RIGHT')

    with keyboard.pressed(pynput.keyboard.Key.space):
        key = 'd'
        for i in range(50):
            keyboard.press(key)
        keyboard.release(key)
    keyboard.release(pynput.keyboard.Key.space)

def jump_left():
    print('JUMP Left')

    with keyboard.pressed(pynput.keyboard.Key.space):
        key = 'a'
        for i in range(50):
            keyboard.press(key)
        keyboard.release(key)
    keyboard.release(pynput.keyboard.Key.space)
