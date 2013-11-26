# Welcome!

Welcome to the homepage of my third project of Fall 2013 Semester, *I Can See Clearly Now*, Project 3 of Professor [Andy Johnson](http://www.evl.uic.edu/aej/)'s [Computer Graphics II](http://www.evl.uic.edu/aej/526/) course.
See also my [Project 1](http://joysword.github.io/cs526.project1/) and [Project 2](http://joysword.github.io/cs526.project2/)

### Demo

### Introduction

This project was proposed as a [rogue-like](http://en.wikipedia.org/wiki/Roguelike) 'game' developed as a practice on multiple techniques for [omegalib](http://github.com/uic-evl/omegalib) and [CAVE2](http://www.evl.uic.edu/core.php?mod=4&type=1&indi=424). The original proposal can be found [here](https://sites.google.com/site/syin8uic/CS526/project3).

What I actually implemented include:

1. Randomly generated dungeon levels
2. GPU Shaders for textures
3. Navigation using Wand
4. Background music and environmental sound effects
5. Environmental lighting and two kinds of artificial lighting
6. Extended [Bullet](http://bulletphysics.org/wordpress/) physics engine functionality in Omegalib applied in this project

### Download and Installation

1. Have omegalib installed, with python support enabled and cyclops and omegaOsg modules added
2. If you are using Mountain Lion or higher, you also need to have [XQuartz](http://xquartz.macosforge.org/landing/) installed and running. If you are using Mavericks, you need to download Xcode 5 and command line tools.
3. Download source code of this project from [Github](https://github.com/joysword/cs526.project3) or on top of this page
4. To run the project, using following commands:
$ cd [omegalib_build]/bin/
$ ./orun -s [where_you_put_this_project]/main.py

Note that to have the best experience, you need to run it on CAVE2. If you want one, you can buy one [here](http://www.mechdyne.com/cave2.aspx)

# Detail Description
##### all fatures and usages discussed here are for running this app on [CAVE2](http://www.evl.uic.edu/core.php?mod=4&type=1&indi=424) if not noticed otherwise

### Features and Usage
#### Dungeons Randomized
Each level of dungeon has random number of rooms of random sizes. Rooms are connected by tunnels at random positions and with random length. In each room there are 3-4 torches, which provide lighting, at random position of each side.

#### Physics Attached
Floors and walls come with attached physics attributes so that the 'character' won't go through the wall. (Note that if you keep trying, you will be able go through walls due to the accuracy issue of physics calculation)

#### Navigation Implemented
Currently what the 'character' can do is walking in the maze. I also implmented 'jumping' using physics but it is not really useful until creeps or monsters are put into this dungeon in the future. The 'character' starts from the room with staircases that coming from upper world and tries to find the other staircase that leads to a lower level of dungeon.

There is also a chest in a random room but currently nothing is in it!

To move the 'character' around, use analog stick of the Wand. To turn left or right, hold Button7 and move the Wand to the same direction that you want to turn to. To jump, press ButtonDown. If the 'character' falls, pressButtonUp to reset his orientation.

#### Navigation Implement

# Gains

### GPU Programming
I took this project as an opportunity to pick up half of what I learned in GPU Programming course, writing shaders. And learned basic of writing shaders in omegalib.
Writing shaders in omegalib is somewhat different from doing in native OpenGL programs, but the underlying principle and process are the same. Generally speaking, the uniqueness reflects in following aspects:

* omegalib provides multiple default structures and uniforms that users can assign value to in cyclops appllication
* omegalib provides multiple default shaders. Users in most times will only need to write a part of the whole process

In this project, I wrote shaders for attaching texture to an entity in different ways.

### Random Dungeon Generation

### Lighting
I also tried out simulating fire light and flashlight.

### Bullet Physics
I continued working on Bullet Physics engine and added `RigidBody` for `PlaneShape`. `PlaneShape`'s are extensively used in building the dungeon.
I also added `addCentralForce()` and `setLinearVelocity()` to current functionality set in cyclops because I thought they would be useful if the 'character' needs to kill creatures in the dungeon. Unfortunately, I haven't got a chance to add more fun stuff into my dungeon.

### *Using xbox 360 controller as input device
This has not been acquired 100%. I tried to implement handling events from xbox 360 controller because xbox 360 controller is probably more intuitive than the Wand in this setting. Although some experiments were done, I couldn't make everything work properly before deadline.

# Source and Reference
Sources and reference I used in this project:

* [CS 525 Course Notes](http://www.evl.uic.edu/aej/525/index.html) (I used it to pick up GPU programming)
* [Encycolorpedia](http://encycolorpedia.com/f8c377) (I used it to choose color for lighting)
* [freesound.org](http://www.freesound.org) (I used it to find sound effects)
* [Introduction to OGRE3D](https://jira.ai2.upv.es/confluence/download/attachments/13303823/Introduction+to+Ogre3D.pdf?version=1&modificationDate=1317394839000) (I used it to choose parameters for lighting)
* [lighthouse3d.com](http://www.lighthouse3d.com/tutorials/) (I used it to pick up GPU programming)
* [NetCave: Project Description](http://graphics.cs.wisc.edu/WP/virtualreality11/category/netcave-project-description/) (I used it as the idea of this project)
* [Random Dungeon Generations](http://breinygames.blogspot.com/2011/07/random-map-generation.html) (I used it as the foundation of generator)
* [soundjay.com](http://soundjay.com/) (I used it to find sound effects)

# Future Work

There are plenty of interesting things I thought of adding to the dungeon. I hope in the future I can make this dungeon more and more fun (by making it creepy and dangerous)
