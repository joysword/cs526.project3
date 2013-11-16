import pickle
import time
import cyclops
from map_generator import *

dungeon = Dungeon((100, 80), "Neverland", 50, (4, 4), (12, 12), (8, 8))
dungeon.generate_dungeon()

tile = dungeon.grid

print 'tile:'
#print tile

scene = getSceneManager()
cam = getDefaultCamera()
scene.setBackgroundColor(Color(0, 0, 0, 1))

sn_root = SceneNode.create('root')

## Create a point ligh
light1 = Light.create()
light1.setLightType(LightType.Point)
light1.setColor(Color(1.0, 1.0, 1.0, 1.0))
light1.setPosition(cam.getPosition())
light1.setEnabled(True)

cam.addChild(light1)

cam.setPosition(50,125,40)
cam.pitch(-3.14*0.5)

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
			box = BoxShape.create(1,0.2,1)
			box.setPosition(x,0.1,z)
			box.setEffect('colored -d green')
			sn_root.addChild(box)
		elif ti==2: # corner
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d white')
			sn_root.addChild(box)
		elif ti==3: # NORTH wall
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d blue')
			sn_root.addChild(box)
		elif ti==4: # EAST wall
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d blue')
			sn_root.addChild(box)
		elif ti==5: # SOUTH wall
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d blue')
			sn_root.addChild(box)
		elif ti==6: # WEST wall
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d blue')
			sn_root.addChild(box)
		elif ti==7: # door
			box = BoxShape.create(1,0.2,1)
			box.setPosition(x,0.1,z)
			box.setEffect('colored -d #00611c')
			sn_root.addChild(box)
		elif ti==8: # upstairs
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d white')
			sn_root.addChild(box)
		elif ti==9: # downstairs
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d black')
			sn_root.addChild(box)
		elif ti==10: # chest
			box = BoxShape.create(1,1,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d yellow')
			sn_root.addChild(box)
		elif ti==11: # path
			box = BoxShape.create(1,0.2,1)
			box.setPosition(x,0.5,z)
			box.setEffect('colored -d green')
			sn_root.addChild(box)
