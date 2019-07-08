# Pysteroids

This is basically a Asteroids clone done with Python 3.7 and Pygame, as a learning experiment.

It's not a clone in the sense that I didn't worry too much with mimicking the actual game, just the idea of it.

Zero care was taken with performance, so it might struggle on weaker CPUs (there's a naive particle system implementation, and most everything is done with anti-aliased lines).

The game evolved during development in terms of architecture, as I learned more about Python. 

There'a an engine component (under the Engine folder), which takes care of the game loop, screen handling (there's two - title screen and game screen), mesh drawing and loading (using JSON for the file format), particle system, trail effect, font handling (both through Pygame and a custom system that uses lines).

Full documentation will be added in the near future for Doxygen (so I also get used to that in this type of learning projects).

## Art

* Graphics and models are done directly in JSON and imported into the engine
* Audio is done using [Bfxr]

## Licenses

All code in this repo is made available through the [GPLv3] license.
The text and all the other files are made available through the 
[CC BY-NC-SA 4.0] license.

## Metadata

* Autor: [Diogo Andrade][]

[Diogo Andrade]:https://github.com/DiogoDeAndrade
[GPLv3]:https://www.gnu.org/licenses/gpl-3.0.en.html
[CC BY-NC-SA 4.0]:https://creativecommons.org/licenses/by-nc-sa/4.0/
[Bfxr]:https://www.bfxr.net/