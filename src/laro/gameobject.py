
# NOTE:
# Adding *args and **kwds allows me to reduce the amount of copy-pasting I need to do in the future.
# It also allows classes that give more args and keyword args to use functions that take less.
# For example, if I had a Renderer that took "is_good_function," I won't have to copy is_good_function 
# to the GameObject and Collection.
# Though for future updates, we would have to use args[index] and kwds[key]

# Libraries
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Optional

import pygame
import laro

# Constants
DEFAULT_TEXTURE = pygame.Surface((64, 64))
DEFAULT_TEXTURE.set_colorkey((0, 0, 0, 0))
DEFAULT_TEXTURE.fill((255, 0, 255, 0))

DEFAULT_RENDERER = NotImplemented

# Code
# GameObjects
class GameObject(pygame.sprite.Sprite):
    __slots__ = (
        "_renderer",
        "_texture",
        "_position",
        "_scale",
        "_rotation",
        "_rect",
    )
    
    #   Magic Methods
    def __init__(self, 
        texture: pygame.Surface | None = None,
        renderer: Renderer | None = None,
        position: pygame.math.Vector2 | tuple[float, float] = (0, 0), 
        scale: pygame.math.Vector2 | tuple[float, float] = (64, 64), 
        rotation: float = 0.0,
        *groups: pygame.sprite.Group,
        **kwds: Any) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)

        # Variables
        self.renderer = renderer
        self.position = position # Position refers to the centre of the character, unlike pygame's top-left.
        self.scale = scale
        self.rotation = rotation
        self.texture = texture # Moved texture here because it needs scale and rotation to set the self.image.

    # Attributes
    @property
    def renderer(self) -> AbstractRenderer | Renderer:
        return self._renderer
    
    @renderer.setter
    def renderer(self, r: AbstractRenderer | Renderer | None) -> None:
        """Renderer to be used by the GameObject. If no renderers are supplied, DEFAULT_RENDERER is used."""
        self._renderer = Renderer() if r is None else r

    @property
    def texture(self) -> pygame.Surface | laro.assets.Texture:
        return self._texture
    
    @texture.setter
    def texture(self, t: pygame.Surface | laro.assets.Texture | None):
        """Stores the texture to be used by the GameObject but is not modified itself during rendering/drawing (for that, see GameObject.image)."""
        if t is None:
            self._texture = DEFAULT_TEXTURE    # Ensures that the GameObject always has something to render.
        else:
            self._texture = t

    @property
    def position(self) -> pygame.math.Vector2:
        return self._position

    @position.setter
    def position(self, p: pygame.math.Vector2 | tuple[float, float]) -> None:
        """The GameObject's Position."""
        self._position = pygame.math.Vector2(p)

    @property
    def scale(self) -> pygame.math.Vector2:
        return self._scale

    @scale.setter
    def scale(self, s: pygame.math.Vector2 | tuple[float, float])  -> None:
        """The GameObject's Scale. See GameObject.image for more information."""
        self._scale = pygame.math.Vector2(s)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, r: float) -> None:
        """The GameObject's Rotation. Limited to 0-360. See GameObject.image for more information."""
        self._rotation = r % 360

    @property
    def rect(self) -> pygame.Rect:
        """The GameObject's Rect/Hitbox. Primarily used by pygame.sprite.Group.draw(). This attribute cannot be set."""
        # The rect basically acts as the bounding box/hitbox for the GameObject.
        # Q: Why did I go through all the trouble to implement the rect attribute?
        # A: When I get lazy for other games, I could use the default draw() method of pygame.sprite.Group.
        # pygame.Surface.blit() uses the topleft corner of a Sprite's image to draw stuff.
        # This attribute effectively re-writes Sprite.rect, making it immutable.
        # We don't need the rects anyway since we only use it for sprite.Group's default draw().
        return self.image.get_rect(center=self.position) # type: ignore
    
    @rect.setter
    def rect(self, r) -> None: # type: ignore
        raise Exception('GameObject.rect not settable.')

    @property
    def image(self) -> pygame.Surface:
        """The actual image to be drawn onto a surface. Uses the GameObject.renderer to transform GameObject.texture."""
        # Similar to GameObject.rect, image is also immutable.
        return self.renderer.transform(self.texture, tuple(self.scale), self.rotation)
    
    @image.setter
    def image(self, i) -> None: # type: ignore
        raise Exception('GameObject.image not settable.')

    # Functions
    def update(self, *args: Any, **kwds: Any) -> None:
        pass

    def render(self, 
        dest: pygame.Surface,
        *args: Any, 
        draw_hitbox: bool = False,
        bounding_box: Optional[pygame.Rect] = None,
        **kwds: Any) -> None:
        """Draws a GameObject onto a destination surface. It makes use of the Renderer supplied during __init__().
        This function may be called by Collection.

        Args:
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): If true, draws GameObject.rect.
            bounding_box (Optional[pygame.Rect]): If set to a Rect, only draws the GameObject when it is inside it.
        """
        self.renderer(gameobject=self, dest=dest, *args, draw_hitbox=draw_hitbox, bounding_box=bounding_box, **kwds)

# Collections
class Collection(pygame.sprite.Group):
    __slots__ = (
        "spritedict",
        "lostsprites"
    )
    def __init__(self, *gameobjects: Any | GameObject | Collection, **kwds: Any) -> None:
        super().__init__(*gameobjects)

    def update(self) -> None:
        """Updates the GameObjects in this Collection by calling their update() functions.
        """
        for sprite in self:
            sprite.update()

    def render(self, 
        dest: pygame.Surface, 
        *args: Any, 
        draw_hitbox: bool=False,
        bounding_box: Optional[pygame.Rect]=None,
        **kwds: Any) -> None:
        """Renders all of the GameObjects in this Collection. More customisable than the standard Group.draw()

        Args:
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): If true, draws the hitboxes of the GameObject.
            bounding_box (Optional[pygame.Rect]): If None, gets the Rect of the destination surface and only draws when the GameObject is inside it. If set to a Rect, only draws the GameObject when it is inside it.
        """
        for sprite in self:
            sprite.render(dest=dest, *args, draw_hitbox=draw_hitbox, bounding_box=dest.get_rect() if bounding_box is None else bounding_box, **kwds)

# Renderers
class AbstractRenderer(ABC):
    __slots__ = {
        "hitbox_colour": "Colour of the hitboxes to be displayed.",
        "_hitbox_width": None,
    }
    # Magic Methods
    @abstractmethod
    def __init__(self, 
        hitbox_colour: pygame.typing.ColorLike = (255, 0, 0, 0), 
        hitbox_width: int = 1, 
        *args: Any, 
        **kwds: Any) -> None:
        self.hitbox_colour: pygame.typing.ColorLike = hitbox_colour
        self.hitbox_width = hitbox_width

    @abstractmethod
    def __call__(self, 
        gameobject: GameObject, 
        dest: pygame.Surface, 
        *args: Any,
        draw_hitbox: bool=False,
        bounding_box: Optional[pygame.Rect]=None,  
        **kwds: Any) -> None:
        pass

    # Attributes
    @property
    def hitbox_width(self) -> int:
        return self._hitbox_width
    
    @hitbox_width.setter
    def hitbox_width(self, h: int) -> None:
        """Border thickness of the hitbox. May be set to any positive integer. Defaults to 1 if set otherwise."""
        if h > 0:
            self._hitbox_width = h
        else:
            self._hitbox_width = 1

    # Functions
    @lru_cache(maxsize=1024)
    @abstractmethod
    def transform(self, 
        source: pygame.Surface | laro.assets.Texture, 
        scale: tuple[float, float], 
        rotation: float, 
        *args: Any, 
        **kwds: Any) -> pygame.Surface:
        pass

class Renderer(AbstractRenderer):
    __slots__ = {
        "hitbox_colour": "Colour of the hitboxes to be displayed.",
        "_hitbox_width": None,
    }
    def __init__(self, 
        hitbox_colour: pygame.typing.ColorLike = (255, 0, 0, 0), 
        hitbox_width: int = 1, 
        *args: Any, 
        **kwds: Any) -> None:
        super().__init__(hitbox_colour, hitbox_width, *args, **kwds)

    def __call__(self, 
        gameobject: GameObject, 
        dest: pygame.Surface, 
        *args: Any,
        draw_hitbox: bool=False,
        bounding_box: Optional[pygame.Rect]=None,  
        **kwds: Any) -> None:
        """Blits GameObjects onto a destination surface. This is the standard rendering.

        Args:
            gameobject (GameObject): GameObject to be blitted.
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): If true, draws GameObject.rect.
            bounding_box (Optional[pygame.Rect]): If set to a Rect, only draws the GameObject when it is inside it.
        """
        if bounding_box is not None and bounding_box.colliderect(gameobject.rect):
            dest.blit(gameobject.image, gameobject.rect)
            if draw_hitbox:
                pygame.draw.rect(dest, self.hitbox_colour, gameobject.rect, self.hitbox_width)

    # Functions
    @lru_cache(maxsize=1024)
    def transform(self, 
        source: pygame.Surface | laro.assets.Texture, 
        scale: tuple[float, float], 
        rotation: float, 
        *args: Any, 
        **kwds: Any) -> pygame.Surface:
        """Standard transformation for Surfaces. Scale is done before rotation to maintain its proportions. 
        Only supports regular 2d textures.

        Args:
            source (pygame.Surface | laro.assets.Texture): The Surface to be transformed.
            scale (pygame.math.Vector2 | tuple[float, float]): Scale of Surface.
            rotation (float): Rotation of Surface.

        Returns:
            pygame.Surface: Transformed Surface.
        """
        # This function is cached because I'm guessing a thousand transformations per frame can't be good for your health.

        # Scale happens before rotation so that the gameobject retains its proportions.
        # A renderer subclass is used if we want to transformation in weird ways (e.g. for a fake 3D effect).
        if isinstance(source, pygame.Surface):
            return pygame.transform.rotate(pygame.transform.scale(source, scale), rotation)
        # We assume that its a Single 2d Texture instead.
        return pygame.transform.rotate(pygame.transform.scale(source[0], scale), rotation)

# Don't delete: this is the peak code. このコード最高すぎだよ！
# class FlatRenderer(Renderer):
#     def transform(self, source, scale, rotation) -> pygame.Surface:
#         surf = super().transform(source, scale, rotation)
#         return pygame.transform.scale(surf, (surf.get_width(), surf.get_height()//2))

# Testing
def _test() -> None:
    pass

# Test
if __name__ == "__main__":
    _test()