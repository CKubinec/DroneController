import pygame


def init():
    pygame.init()
    pygame.display.set_mode((300, 300))


def get_key(key_name):
    ans = False
    for ans in pygame.event.get():
        pass
    ket_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if ket_input[my_key]:
        ans = True
        pygame.display.update()
        return ans


def main():
    if get_key("LEFT"):
        print("Left Key Pressed")
    if get_key("RIGHT"):
        print('Right Key Pressed')


if __name__ == '__main__':
    init()
    while True:
        main()
