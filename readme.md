# Welcome!

Welcome to the homepage of my third project of Fall 2013 Semester, I Can See Clearly Now, project 2 of Professor [Andy Johnson](http://www.evl.uic.edu/aej/)'s [Computer Graphics II](http://www.evl.uic.edu/aej/526/) course.
See also my [Project 1](http://joysword.github.io/cs526.project1/) and [Project 2](http://joysword.github.io/cs526.project2/)

### Introduction

This project is a [rogue-like](http://en.wikipedia.org/wiki/Roguelike) 'game' developed as a practice on multiple techniques for [omegalib](http://github.com/uic-evl/omegalib) and [CAVE2](http://www.evl.uic.edu/core.php?mod=4&type=1&indi=424).

Generally speaking, it has following features:

1. Random dungeon levels generated fast using GPU
2. Three redirection techniques implemented
3. Music and lighting varies as environment changes
4. [Bullet](http://bulletphysics.org/wordpress/) physics engines used for collision detection
5. omegalib 2D container used for HUD

### Demo

### Download and Installation

1. have omegalib installed, with python support enabled and cyclops and omegaOsg modules added
2. if you are using Mac OS X Mountain Lion or higher, you also need to have [XQuartz](http://xquartz.macosforge.org/landing/) installed and running
3. download source code of this project from [Github](https://github.com/joysword/cs526.project3) or on top of this page
4. to run the project, do as following:
$ cd [omegalib_build]/bin/
$ ./orun -s [where_you_put_this_project]/main.py

Note that to have the best performance from this app, you need to run it on CAVE2. You can buy one [here](http://www.mechdyne.com/cave2.aspx)

# Features and Usage
##### all fatures and usages are for running this app on [CAVE2](http://www.evl.uic.edu/core.php?mod=4&type=1&indi=424) if not noticed otherwise

Data used in this project is coming from different sources, including but not limiting to

* [Exoplanet Data Explorer](http://exoplanets.org/table?datasets=explorer)
* [NASA Exoplanet Archive](http://exoplanetarchive.ipac.caltech.edu)
* [Open Exoplanet Catalogue](http://www.openexoplanetcatalogue.com/index.php)
* [Extrasolar Planets Encyclopedia](http://exoplanet.eu)
* [Wikipedia](http://en.wikipedia.org)

[More info](data.html) about the Data

### Interesting Findings
Using this app, we are able to look into the data and discover things. See [more info](findings.html) about what I found



Mazes will be generated using random dungeon generating algorithm
Geometries and textures will be rendered using GPU shaders
Textures will include at least floors, rocks and walls
Models will include at least doors, chests and stairs
Coming up with good ways to navigate (in cave2) through the maze

At least 3 redirection techniques [1] will be implemented or compared
Making appropriate use of audio

Different background music will be played for different environment
Sound effects will include at least footsteps, door opening and door locked
Making appropriate use of lighting

Lighting will include at least environment lighting and flashlight
Applying appropriate physics in the scene

Bullet physics engine will be used for collision detection
Ideally the door movement (opening and closing) would be using Hinge Constraint in Bullet
Ideally there will be as much as physics
Adding simple gaming elements into the scene

HUD, if implemented, will be using 2D container in omegalib
picking up keys in chests to open doors
Ideally there will be killing monsters involved
See [detailed desciption](features.html) for all the features.
