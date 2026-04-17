
# Libraries
from typing import Iterable
from collections import deque

import pygame
import laro

# Code
class Texture(deque):
    def __init__(self, iterable: Iterable[pygame.Surface | Texture], maxlen: int | None = None) -> None:
        # Integrated texture loading and storing.
        # May be used by:
        # - Simple 2d sprites
        # - Animated 2d sprites
        # - Simple Spritestack
        super().__init__(iterable, maxlen)

    # Attributes
    @property
    def texture(self) -> pygame.Surface:
        return self[0]
    
    @texture.setter
    def texture(self, t: pygame.Surface) -> None:
        self[0] =  t

def load(path: str, 
    *args, 
    width: int=16,
    height: int=16, 
    horizontal: bool=True, 
    **kwds) -> Texture:
    raise NotImplementedError("Texture loading not yet implemented. Come back later.")

def load_stacked(path: str, 
    *args, 
    width: int=16,
    height: int=16, 
    **kwds) -> Texture:
    # Integrated texture loading and storing.
    # May be used by:
    # - Simple Spritestack
    # - Animated Spritestack
    raise NotImplementedError("Texture loading not yet implemented. Come back later.")

def test() -> None:
    t = Textures([1,]) # type: ignore
    print(t)

# Test
if __name__ == "__main__":
    test()