
# Libraries
from typing import Iterable

import pygame
import laro

# Code
class Texture(tuple):
    # Magic Methods
    def __new__(cls, *iterable: Iterable[pygame.Surface | Texture]) -> Texture:
        # NOTE: Include instantiation through loading of filename for both 2d and 3d (spritestacked) textures.
        return super().__new__(cls, iterable[0] if len(iterable) == 1 else iterable)
    
    def __init__(self, *args) -> None:
        super().__init__()

        try:
            self.texture = self[0]
        except IndexError:
            self.texture = None

    def __repr__(self) -> str:
        return f"laro.assets.Texture: {super().__repr__()}"

    # Functions
    @classmethod
    def load(cls,
        path: str, 
        *args, 
        width: int=16,
        height: int=16, 
        horizontal: bool=True, 
        **kwds) -> Texture:
        raise NotImplementedError("Texture loading not yet implemented. Come back later.")

    @classmethod
    def load_stacked(cls, 
        path: str, 
        *args, 
        width: int=16,
        height: int=16, 
        **kwds) -> Texture:
        # Integrated texture loading and storing.
        # May be used by:
        # - Simple Spritestack
        # - Animated Spritestack
        raise NotImplementedError("Texture loading not yet implemented. Come back later.")

def _test() -> None:
    t = Texture()
    print(t)

# Test
if __name__ == "__main__":
    _test()