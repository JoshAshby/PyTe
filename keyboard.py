import pygame
import virtkeyboard
def key():
    mykeys = virtkeyboard.VirtualKeyboard()
    pygame.display.init()
    size=800,450
    screen=pygame.display.set_mode(size)
    userinput = mykeys.run(screen)
#debug    print userinput
    pygame.display.quit()
    return  userinput

