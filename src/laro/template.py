
# Libraries
import pygame
import laro
import moderngl

import sys

# Code
class Game:
    def __init__(self, 
        display_title: str="Pygame Window", 
        debug: bool=False, 
        icon: pygame.Surface | None = None) -> None:
        
        pygame.init()

        self.debug = debug
        self.icon = icon
        self.display_title = display_title
        self.display: pygame.Surface = pygame.display.set_mode(
            (500, 400), 
            pygame.RESIZABLE)
        self.clock: laro.Clock = laro.Clock(60)
        self.running: bool = False

    # Game Attributes
    @property
    def display_title(self) -> str:
        return self._display_title
    
    @display_title.setter
    def display_title(self, d: str) -> None:
        self._display_title = d
        pygame.display.set_caption(self.display_title)

    @property
    def icon(self) -> pygame.Surface | None:
        return self._icon
    
    @icon.setter
    def icon(self, i: pygame.Surface | None) -> None:
        if i is not None:
            self._icon = i
            pygame.display.set_icon(i)

    def __call__(self) -> None:
        # NOTE: All interactions are meant to be carried out through start(), update(), 
        # check_events(), render(), and quit(). Do not write code in this part unless you have to.

        self.start()
        while self.running:
            self.update()
            self.check_events()
            self.render()
        self.quit()

    # Functions
    def start(self) -> None:
        self.running = True

        if self.debug:
            # Enter additional debug code here.
            pass

        # Enter normal code here.

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Enter normal event checking here.
            
            if self.debug:
                # Enter additional debug code here. 
                pass

    def update(self) -> None:
        self.clock.tick()

        if self.debug:
            # Enter additional debug code here.
            pass

        # Enter normal code here.

    def render(self) -> None:
        if self.debug:
            # Fills the screen with an obnoxious purple colour during debug.
            # This code might be changed as I implement moderngl.
            self.display.fill((255, 0, 255, 0))

            # Enter additional debug code here. 
            
        else:
            self.display.fill((255, 255, 255, 0))

        # Enter normal code here.

        pygame.display.flip()

    def quit(self) -> None:
        if self.debug:
            # Enter additional debug code here. 
            pass

        # Enter normal code here.

        pygame.quit() 
        sys.exit()

# Run
if __name__ == "__main__":
    g = Game()
    g()