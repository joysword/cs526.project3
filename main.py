import pickle
import time
import cyclops
from math import pi
from map_generator import *

class Texture:
	def __init__(self):
		#self.floor = Material.create()
		#self.floor.setDiffuseTexture('textures/mud1.jpg')
		self.floor = 'textures/mud1.jpg'
		self.wall = 'textures/rock2.jpg'

texture = Texture()

WALL_HEIGHT = 2
WALL_HALF_HEIGHT = WALL_HEIGHT*0.5
TILE_WIDTH = 1
TILE_HALF_WIDTH = TILE_WIDTH*0.5
BODY_HEIGHT = 1.76
BODY_HALF_HEIGHT = BODY_HEIGHT*0.5
BODY_WEIGHT = 50
EYE_HEIGHT = 1.55

HALF_PI = pi*0.5

GRAVITY = -9.8

dungeon = Dungeon((100, 80), "Neverland", 50, (4, 4), (12, 12), (8, 8))
dungeon.generate_dungeon()

tile = dungeon.grid

print 'tile:'
#print tile

scene = getSceneManager()
scene.setBackgroundColor(Color(0, 0, 0, 1))

scene.setGravity(Vector3(0, GRAVITY, 0))

sn_root = SceneNode.create('root')

## Create player character - a box
# TO DO: a cylinder

#sn_player = SceneNode.create('player')
me = BoxShape.create(0.8,BODY_HEIGHT,1.9)
me.setEffect('colored -e red')
#me.setBoundingBoxVisible(True)
me.getRigidBody().initialize(RigidBodyType.Box, BODY_WEIGHT)
#me.getRigidBody().setUserControlled(True)

#me.setPosition(50,BODY_HALF_HEIGHT,40)

#sn_player.addChild(me)
cam = getDefaultCamera()
me.addChild(cam)
#cam.addChild(me)

cam.setPosition(0,-2-BODY_HALF_HEIGHT+EYE_HEIGHT,0)

setNearFarZ(0.1,100)

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
	#cam.setPosition(50,50,40)
	#cam.pitch(-HALF_PI)
	me.setPosition(50,50,40)
	me.pitch(-HALF_PI)
	me.getRigidBody().sync()
	#sn_player.setPosition(50,50,40)
	#sn_player.pitch(-HALF_PI)
else:
 	#cam.setPosition(50,0,40)
 	me.setPosition(50,1,40)
 	me.getRigidBody().sync()
 	#sn_player.setPosition(50,0,40)


shader_floor = ProgramAsset()
shader_floor.name = "floor"
shader_floor.vertexShaderName = 'shaders/floor.vert'
shader_floor.fragmentShaderName = 'shaders/floor.frag'
#shader_floor.geometryShaderName = 'shaders/floor.geom'

scene.addProgram(shader_floor)

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
			floor.pitch(-HALF_PI)
			#floor.setEffect('colored -e green')
			floor.setEffect('textured -v emissive -d '+texture.floor)
			#m = floor.getMaterial()
			#m = texture.floor
			#floor.getRigidBody().initialize(RigidBodyType.Plane,0)
			#floor.getRigidBody().sync()
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
			wall.getRigidBody().initialize(RigidBodyType.Plane,0)
			wall.getRigidBody().sync()
			sn_root.addChild(wall)
		elif ti==4: # EAST wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
			wall.yaw(-HALF_PI)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			wall.getRigidBody().initialize(RigidBodyType.Plane,0)
			wall.getRigidBody().sync()
			sn_root.addChild(wall)
		elif ti==5: # SOUTH wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
			wall.pitch(pi)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			wall.getRigidBody().initialize(RigidBodyType.Plane,0)
			wall.getRigidBody().sync()
			sn_root.addChild(wall)
		elif ti==6: # WEST wall
			wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
			wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
			wall.yaw(HALF_PI)
			#wall.setEffect('colored -e blue')
			wall.setEffect('textured -v emissive -d '+texture.wall)
			wall.getRigidBody().initialize(RigidBodyType.Plane,0)
			wall.getRigidBody().sync()
			sn_root.addChild(wall)
		elif ti==7: # door - NO DOORS
			print "door"
			door = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			door.setPosition(x,WALL_HALF_HEIGHT,z)
			door.setEffect('colored -e #00611c')
			sn_root.addChild(door)
		elif ti==8: # upstairs TO DO
			upstairs = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			upstairs.setPosition(x,WALL_HALF_HEIGHT,z)
			upstairs.setEffect('colored -e white')
			sn_root.addChild(upstairs)
		elif ti==9: # downstairs TO DO
			downstairs = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
			downstairs.setPosition(x,WALL_HALF_HEIGHT,z)
			downstairs.setEffect('colored -e black')
			sn_root.addChild(downstairs)
		elif ti==10: # chest
			floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
			floor.setPosition(x,0,z)
			floor.pitch(-HALF_PI)
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
			floor.pitch(-HALF_PI)
			floor.setEffect('colored -e #01b2f1')
			sn_root.addChild(floor)


ground = PlaneShape.create(120,100)
ground.setPosition(50,0,40)
ground.pitch(-HALF_PI)
ground.getRigidBody().initialize(RigidBodyType.Plane,0)
ground.getRigidBody().sync()
#ground.setEffect('colored -e red')
ground.setVisible(False)

print me.getPosition()

##############################################################################################################
# EVENT FUNCTION

def onEvent():
	global me

	e = getEvent()
	#print e.getSourceId()

	if e.isKeyDown(ord('a')):
		me.translate(-0.1,0,0,Space.Local)
		print 'a'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('s')):
		me.translate(0,0,0.1,Space.Local)
		print 's'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('d')):
		me.translate(0.1,0,0,Space.Local)
		print 'd'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('w')):
		me.translate(0,0,-0.1,Space.Local)
		print 'w'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(32):
		#me.translate(0,0.5,0,Space.Local)
		me.getRigidBody().applyCentralImpulse(Vector3(0,120,0))
		print 'space_bar'
		e.setProcessed()
	elif e.isKeyDown(ord('f')):
		me.translate(0,-0.1,0,Space.Local)
		print 'f'
		me.getRigidBody().sync()
		e.setProcessed()

setEventFunction(onEvent)

##############################################################################################################
# UPDATE FUNCTION

def onUpdate(frame, t, dt):
	#me.getRigidBody().sync()
	#print me.getPosition()
	if t>5 and not scene.isPhysicsEnabled():
		scene.setPhysicsEnabled(True)
	pass

setUpdateFunction(onUpdate)


