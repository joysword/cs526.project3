import pickle
import time
import cyclops
from math import pi
from map_generator import *

class Texture:
	def __init__(self):
		self.floor = 'textures/mud1.jpg'
		self.wall = 'textures/rock2.jpg'

texture = Texture()

WALL_HEIGHT = 2
WALL_HALF_HEIGHT = WALL_HEIGHT*0.5
TILE_WIDTH = 1
TILE_HALF_WIDTH = TILE_WIDTH*0.5

dungeon = Dungeon((100, 80), "Neverland", 50, (4, 4), (12, 12), (8, 8))
dungeon.generate_dungeon()

tile = dungeon.grid

print 'tile:'
#print tile

scene = getSceneManager()
cam = getDefaultCamera()
scene.setBackgroundColor(Color(0, 0, 0, 1))

sn_root = SceneNode.create('root')

## Create a point light
light1 = Light.create()
light1.setLightType(LightType.Point)
light1.setColor(Color(1.0, 1.0, 1.0, 1.0))
light1.setPosition(cam.getPosition())
light1.setEnabled(True)

cam.addChild(light1)

light2 = Light.create()
light1.setLightType(LightType.Point)
light1.setColor(Color(1.0, 1.0, 1.0, 1.0))
light1.setPosition(Vector3(20,200,30))
light1.setEnabled(True)

if (0):
	cam.setPosition(50,50,40)
	cam.pitch(-pi*0.5)
else:
	cam.setPosition(50,0,40)

for z in xrange(80):
	for x in xrange(100):
		#print z,x
		ti = tile[z][x]


		'''
		0 = blank space (non-useable)
		1 = floor tile (walkable)
		2 = corner tile (non-useable)
		3 = wall tile facing NORTH.
		4 = wall tile facing EAST.
		5 = wall tile facing SOUTH.
		6 = wall tile facing WEST.
		7 = door tile.
		8 = stairs leading to a higher lever in the dungeon.
		9 = stairs leading to a lower level in the dungeon.
		10 = chest
		11 = path from up to down staircases (floor tile)
		'''

		if ti==0:
			pass
		elif ti==1: # floor tile
			floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
			floor.setPosition(x,0,z)
			floor.pitch(-pi*0.5)
			#floor.setEffect('colored -e green')
			floor.setEffect('textured -v emissive -d '+texture.floor)
			sn_root.addChild(floor)
		elif ti==2: # corner TO DO
			#box = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			#box.setPosition(x,0.5,z)
			#box.yaw(0)
			#box.setEffect('colored -e white')
			#sn_root.addChild(box)
			pass
		elif ti==3: # NORTH wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
			#wall.pitch(0)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			sn_root.addChild(wall)
		elif ti==4: # EAST wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
			wall.yaw(-pi*0.5)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			sn_root.addChild(wall)
		elif ti==5: # SOUTH wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
			wall.pitch(pi)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			sn_root.addChild(wall)
		elif ti==6: # WEST wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
			wall.yaw(pi*0.5)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			sn_root.addChild(wall)
		elif ti==7: # door - NO DOORS
			print "door"
			door = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			door.setPosition(x,WALL_HALF_HEIGHT,z)
			door.setEffect('colored -e #00611c')
			sn_root.addChild(door)
		elif ti==8: # upstairs TO DO
			print "upstairs"
			upstairs = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			upstairs.setPosition(x,WALL_HALF_HEIGHT,z)
			upstairs.setEffect('colored -e white')
			sn_root.addChild(upstairs)
		elif ti==9: # downstairs TO DO
			print "downstairs"
			downstairs = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			downstairs.setPosition(x,WALL_HALF_HEIGHT,z)
			downstairs.setEffect('colored -e black')
			sn_root.addChild(downstairs)
		elif ti==10: # chest
			floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
			floor.setPosition(x,0,z)
			floor.pitch(-pi*0.5)
			floor.setEffect('colored -e yellow')
			sn_root.addChild(floor)
			chest = BoxShape.create(TILE_WIDTH*0.6,0.2,TILE_WIDTH*0.35)
			chest.setPosition(x,0.1,z)
			#cam.setPosition(x+2,0,z+2)
			chest.setEffect('colored -e yellow')
			sn_root.addChild(chest)
		elif ti==11: # path
			floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
			floor.setPosition(x,0,z)
			floor.pitch(-pi*0.5)
			floor.setEffect('colored -e #01b2f1')
			sn_root.addChild(floor)

##############################################################################################################
# EVENT FUNCTION

def onEvent():
	pass

setEventFunction(onEvent)

##############################################################################################################
# UPDATE FUNCTION

def onUpdate(frame, t, dt):
	pass

setUpdateFunction(onUpdate)


