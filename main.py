import pickle
import time
import datetime
import cyclops
from math import pi
from map_generator import *

torch_id = 0
isButton7down = False
isWalking = False
wandOldPos = None
bgmDeltaT = 0
inChannel = False
tile = []

start_x = 0
start_z = 0
end_x = 0
end_z = 0

level = 0

nearest_torch_0 = 0
nearest_torch_1 = 1
nearest_torch_2 = 2
nearest_torch_3 = 3
nearest_torch_4 = 4

class Texture:
	def __init__(self):
		self.floor = Material.create()
		self.floor.setDiffuseTexture('textures/floor_U2_01.jpg')
		self.wall = Material.create()
		self.wall.setDiffuseTexture('textures/rock.png')
		self.ceil = Material.create()
		self.ceil.setDiffuseTexture('textures/rock.png')

		self.channel = Material.create()
		self.channel.setDiffuseTexture('textures/mud1.jpg')
		#self.channel.setColor(Color('red'),Color('red'))
		self.side = Material.create()
		self.side.setDiffuseTexture('textures/mud1.jpg')
		#self.side.setColor(Color('green'),Color('green'))
		self.top = Material.create()
		self.top.setDiffuseTexture('textures/mud1.jpg')
		#self.top.setColor(Color('blue'),Color('blue'))
		self.torch = Material.create()
		self.torch.setDiffuseTexture('textures/wood1.jpg')

		self.door = Material.create()
		self.door.setDiffuseTexture('textures/door012.jpg')

texture = Texture()

TOTAL_WIDTH = 100
TOTAL_DEEP = 80
WALL_HEIGHT = 3
WALL_HALF_HEIGHT = WALL_HEIGHT*0.5
TILE_WIDTH = 1
TILE_HALF_WIDTH = TILE_WIDTH*0.5
BODY_HEIGHT = 1.76
BODY_HALF_HEIGHT = BODY_HEIGHT*0.5
BODY_WEIGHT = 50
EYE_HEIGHT = 1.55
STAIR_HEIGHT = 0.22
STAIR_HALF_HEIGHT = STAIR_HEIGHT*0.5
CHEST_WIDTH = 0.6
CHEST_HEIGHT = 0.3
CHEST_HALF_HEIGHT = CHEST_HEIGHT*0.5
CHEST_DEEP = 0.35
CHANNEL_HEIGHT = WALL_HEIGHT*0.68
CHANNEL_HALF_HEIGHT = CHANNEL_HEIGHT*0.5

HALF_PI = pi*0.5

GRAVITY = -9.8

scene = getSceneManager()
scene.setBackgroundColor(Color(0, 0, 0, 1))

scene.setGravity(Vector3(0, GRAVITY, 0))

sn_root = SceneNode.create('root')

## Create player character - a box
# TO DO: a cylinder

#sn_player = SceneNode.create('player')
me = BoxShape.create(0.4,BODY_HEIGHT,0.3)
#me.setEffect('colored -e red')
#me.setBoundingBoxVisible(True)
me.getRigidBody().initialize(RigidBodyType.Box, BODY_WEIGHT)
#me.getRigidBody().setUserControlled(True)
me.setVisible(False)

#me.setPosition(50,BODY_HALF_HEIGHT,40)

#sn_player.addChild(me)
cam = getDefaultCamera()
me.addChild(cam)
#cam.addChild(me)

cam.setPosition(0,-2-BODY_HALF_HEIGHT+EYE_HEIGHT,0)
cam.setControllerEnabled(False)

setNearFarZ(0.1,100)

# if (0):
# 	#cam.setPosition(TOTAL_WIDTH/2,20,TOTAL_DEEP/2)
# 	#cam.pitch(-HALF_PI)
# 	me.setPosition(TOTAL_WIDTH/2,20,TOTAL_DEEP/2)
# 	me.pitch(-HALF_PI)
# 	me.getRigidBody().sync()
# 	#sn_player.setPosition(50,50,40)
# 	#sn_player.pitch(-HALF_PI)
# else:
#  	#cam.setPosition(TOTAL_WIDTH/2,0,TOTAL_DEEP/2)
#  	me.setPosition(TOTAL_WIDTH/2,BODY_HALF_HEIGHT+0.05,TOTAL_DEEP/2)
#  	me.getRigidBody().sync()
#  	#sn_player.setPosition(50,0,40)

##############################################################################################################
# LIGHTING

## Create environment light
#light_env = Light.create()
#light_env.setLightType(LightType.Point)
#light_env.setColor(Color(1.0, 1.0, 1.0, 1.0))
#light_env.setPosition(cam.getPosition())
#light_env.setEnabled(True)

## Create flashlight
light_flash = Light.create()
light_flash.setLightType(LightType.Spot)
light_flash.setColor(Color('#f8c377'))
light_flash.setLightDirection(Vector3(0,0,-1))
light_flash.setPosition(Vector3(0,0,0))
light_flash.setSpotExponent(32)
#light_flash.setSpotCutoff(10)
light_flash.setSpotCutoff(5/180*pi)
light_flash.setEnabled(False)
cam.addChild(light_flash)

## Create torchlight
light_torch = Light.create()
light_torch.setLightType(LightType.Point)
light_torch.setColor(Color('#f8c377')) # Duren torchlight http://encycolorpedia.com/f8c377
light_torch.setAttenuation(1, 0.22, 0.2)
light_torch.setPosition(Vector3(0.1,2,-0.8))
light_torch.setEnabled(True)
cam.addChild(light_torch)

##############################################################################################################
# MODELS

##STAIRS
sn_upstair = SceneNode.create('upstair')
#sn_root.addChild(sn_upstair)

upstair1 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH)
upstair1.setPosition(0,STAIR_HALF_HEIGHT,0)
sn_upstair.addChild(upstair1)

upstair2 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH-STAIR_HEIGHT)
upstair2.setPosition(0,STAIR_HEIGHT,-STAIR_HALF_HEIGHT)
upstair1.addChild(upstair2)

upstair3 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH-STAIR_HEIGHT*2)
upstair3.setPosition(0,STAIR_HEIGHT,-STAIR_HALF_HEIGHT)
upstair2.addChild(upstair3)

sn_downstair = SceneNode.create('downstair')
#sn_root.addChild(sn_downstair)

downstair1 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH)
downstair1.setPosition(0,-STAIR_HALF_HEIGHT*5,0)
#downstair1.setEffect('colored -e red')
sn_downstair.addChild(downstair1)

downstair2 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH-STAIR_HEIGHT)
downstair2.setPosition(0,STAIR_HEIGHT,-STAIR_HALF_HEIGHT)
#downstair2.setEffect('colored -e green')
downstair1.addChild(downstair2)

downstair3 = BoxShape.create(TILE_WIDTH, STAIR_HEIGHT, TILE_WIDTH-STAIR_HEIGHT*2)
downstair3.setPosition(0,STAIR_HEIGHT,-STAIR_HALF_HEIGHT)
#downstair3.setEffect('colored -e blue')
downstair2.addChild(downstair3)

## CHEST
sn_chest = SceneNode.create('chest')
#sn_root.addChild(sn_chest)

chest = BoxShape.create(CHEST_WIDTH,CHEST_HEIGHT,CHEST_DEEP)
chest.setPosition(0,CHEST_HALF_HEIGHT,0)
chest.setEffect('textured -d textures/wood1.jpg')
sn_chest.addChild(chest)

## TORCH class
class Torch:

	global texture
	global sn_root

	def __init__(self, id):
		self.parent = SceneNode.create('torch'+str(id))
		sn_root.addChild(self.parent)

		self.bot = CylinderShape.create(0.2,0.03,0.03,4,32)
		self.bot.setPosition(0,1.4,TILE_HALF_WIDTH)
		#self.bot.roll(HALF_PI*0.5)
		self.bot.clearMaterials()
		self.bot.addMaterial(texture.torch)
		self.bot.getMaterial().setProgram('floor')
		self.parent.addChild(self.bot)

		self.support_parent = SceneNode.create('support'+str(id))
		self.parent.addChild(self.support_parent)

		self.support = CylinderShape.create(0.5,0.03,0.03,4,32)
		self.support.setPosition(0,1.4-0.03,TILE_HALF_WIDTH+0.2)
		self.support.pitch(-HALF_PI)
		self.support.clearMaterials()
		self.support.addMaterial(texture.torch)
		self.support.getMaterial().setProgram('floor')
		self.support_parent.addChild(self.support)


		# self.text = BoxShape.create(0.1,0.1,0.1)
		# self.text.setEffect('colored -e red')
		# self.text.setPosition(0,0,0.5)
		# self.support.addChild(self.text)
		#self.fire_parent = SceneNode.create('fire'+str(id))
		self.fire = Light.create()
		self.fire.setLightType(LightType.Point)
		self.fire.setColor(Color('#f8c377'))
		#self.fire.setAttenuation(1, 0.09, 0.032)
		self.fire.setAttenuation(1, 0.22, 0.2)
		self.fire.setPosition(0,0,0.5)
		self.fire.setEnabled(False)
		self.support.addChild(self.fire)
		#self.fire_parent.addChild(self.fire)
		#self.support.addChild(self.fire_parent)

	def get(self):
		return self.parent


##############################################################################################################
# PROGRAM ASSETS
shader_floor = ProgramAsset()
shader_floor.name = 'floor'
shader_floor.vertexShaderName = 'shaders/floor.vert'
shader_floor.fragmentShaderName = 'shaders/floor.frag'
#shader_floor.geometryShaderName = 'shaders/floor.geom'

shader_door_left = ProgramAsset()
shader_door_left.name = 'door_left'
shader_door_left.vertexShaderName = 'shaders/door_left.vert'
shader_door_left.fragmentShaderName = 'shaders/door_left.frag'

scene.addProgram(shader_floor)
scene.addProgram(shader_door_left)

##############################################################################################################
# PLAY SOUND
sdEnv = getSoundEnvironment()
sdEnv.setAssetDirectory('syin_p3_cs526')

sd_bgm = SoundInstance(sdEnv.loadSoundFromFile('bgm','sound/bgm.wav'))
sd_water = SoundInstance(sdEnv.loadSoundFromFile('water','sound/water.wav'))
sd_footstep = SoundInstance(sdEnv.loadSoundFromFile('footstep','sound/footsteps-4.wav'))
sd_stair = SoundInstance(sdEnv.loadSoundFromFile('stair','sound/wooden-stairs.wav'))
sd_door = SoundInstance(sdEnv.loadSoundFromFile('stair','sound/door.wav'))

def playSound(sd, pos, vol):
	sd.setPosition(pos)
	sd.setVolume(vol)
	sd.setWidth(20)
	sd.play()

playSound(sd_bgm,cam.getPosition(),0.1)

##############################################################################################################
# DRAW MAZE
def removeAllChildren(sn):
	if sn.numChildren()>0:
		for i in xrange(sn.numChildren()):
			sn.removeChildByIndex(0)

def generate_level():
	global me
	global torch_id
	global level
	global tile

	playSound(sd_stair,cam.getPosition(),0.1)

	removeAllChildren(sn_root)

	random.seed(torch_id*level+19890101)

	dungeon = Dungeon((TOTAL_WIDTH, TOTAL_DEEP), "Neverland", 30, (7, 7), (14, 14), (8, 8))
	dungeon.generate_dungeon()
	#dungeon.print_info(True)

	tile = dungeon.grid

	torch_id = 0

	for z in xrange(TOTAL_DEEP):
		for x in xrange(TOTAL_WIDTH):
			#print z,x
			ti = tile[z][x]

			if ti==0:
				pass
			elif ti==1: # floor tile
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.floor)
				floor.getMaterial().setProgram('floor')
				floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				floor.getRigidBody().sync()
				sn_root.addChild(floor)

				ceil = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				ceil.setPosition(x,WALL_HEIGHT,z)
				ceil.pitch(HALF_PI)
				ceil.clearMaterials()
				ceil.addMaterial(texture.ceil)
				ceil.getMaterial().setProgram('floor')
				sn_root.addChild(ceil)
			elif ti==2: # corner TO DO
				#box = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				#box.setPosition(x,0.5,z)
				#box.yaw(0)
				#box.setEffect('colored -e white')
				#sn_root.addChild(box)
				pass

			elif ti==3: # NORTH wall

				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				wall.yaw(pi)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

			elif ti==23: # torch on NORTH

				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				wall.yaw(pi)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				torch = Torch(torch_id)
				torch_id += 1
				torch.get().setPosition(x,0,z)
				sn_root.addChild(torch.get())

			elif ti==4: # EAST wall

				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(-HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)
			elif ti==24: # torch on EAST

				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(-HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				torch = Torch(torch_id)
				torch_id += 1
				torch.get().setPosition(x,0,z)
				torch.get().yaw(-HALF_PI)
				sn_root.addChild(torch.get())

			elif ti==5: # SOUTH wall
				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				wall.yaw(pi)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)
			elif ti==25: # torch on SOUTH

				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				wall.yaw(pi)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				torch = Torch(torch_id)
				torch_id += 1
				torch.get().setPosition(x,0,z)
				torch.get().yaw(pi)
				sn_root.addChild(torch.get())

			elif ti==6: # WEST wall
				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(-HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)
			elif ti==26: # torch on WEST
				# wall = BoxShape.create(TILE_WIDTH,WALL_HEIGHT,TILE_WIDTH)
				# wall.setPosition(x,WALL_HALF_HEIGHT,z)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Box,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				# reverse
				wall = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				wall.yaw(-HALF_PI)
				wall.clearMaterials()
				wall.addMaterial(texture.wall)
				wall.getMaterial().setProgram('floor')
				wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				wall.getRigidBody().sync()
				sn_root.addChild(wall)

				torch = Torch(torch_id)
				torch_id += 1
				torch.get().setPosition(x,0,z)
				torch.get().yaw(HALF_PI)
				sn_root.addChild(torch.get())

	###### DOOR #######
			elif ti==73: # NORTH door left

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x-TILE_HALF_WIDTH*0.5,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('door_left')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==773: # NORTH door right

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x+TILE_HALF_WIDTH*0.5,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('floor')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==74: # EAST door left

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH*0.5)
				# wall.yaw(-HALF_PI)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				door.yaw(-HALF_PI)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('door_left')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==774: # EAST door right

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH*0.5)
				# wall.yaw(-HALF_PI)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x-TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				door.yaw(-HALF_PI)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('floor')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==75: # SOUTH door left

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x+TILE_HALF_WIDTH*0.5,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				# wall.yaw(pi)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				door.yaw(pi)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('door_left')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==775: # SOUTH door right

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x-TILE_HALF_WIDTH*0.5,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				# wall.yaw(pi)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
				door.yaw(pi)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('floor')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==76: # WEST door left

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z-TILE_HALF_WIDTH*0.5)
				# wall.yaw(HALF_PI)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				door.yaw(HALF_PI)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('door_left')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)
			elif ti==776: # WEST door right

				# wall = PlaneShape.create(TILE_WIDTH*0.5,WALL_HEIGHT)
				# wall.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z+TILE_HALF_WIDTH*0.5)
				# wall.yaw(HALF_PI)
				# wall.clearMaterials()
				# wall.addMaterial(texture.wall)
				# wall.getMaterial().setProgram('floor')
				# wall.getRigidBody().initialize(RigidBodyType.Plane,0)
				# wall.getRigidBody().sync()
				# sn_root.addChild(wall)

				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				door = PlaneShape.create(TILE_WIDTH,WALL_HEIGHT)
				door.setPosition(x+TILE_HALF_WIDTH,WALL_HALF_HEIGHT,z)
				door.yaw(HALF_PI)
				door.clearMaterials()
				door.addMaterial(texture.door)
				door.getMaterial().setProgram('floor')
				#door.setEffect('colored -e #00611c')
				sn_root.addChild(door)

			elif ti==8: # upstairs
				sn_upstair.setPosition(x,0,z)
				me.setPosition(x,BODY_HALF_HEIGHT+0.05,z)
				me.getRigidBody().sync()
			elif ti==9: # downstairs
				sn_downstair.setPosition(x,0,z)
				end_x = x
				end_z = z
			elif ti==10: # chest
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.floor)
				floor.getMaterial().setProgram('floor')
				sn_root.addChild(floor)
				sn_chest.setPosition(x,0,z)

	###### PATH #######
			elif ti==11: # path
				# original path
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.setEffect('colored -e #01b2f1')
				sn_root.addChild(floor)

				# floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				# floor.setPosition(x,0,z)
				# floor.pitch(-HALF_PI)
				# floor.clearMaterials()
				# floor.addMaterial(texture.floor)
				# floor.getMaterial().setProgram('floor')
				# #floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				# #floor.getRigidBody().sync()
				# sn_root.addChild(floor)

				# ceil = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				# ceil.setPosition(x,WALL_HEIGHT,z)
				# ceil.pitch(HALF_PI)
				# ceil.clearMaterials()
				# ceil.addMaterial(texture.ceil)
				# ceil.getMaterial().setProgram('floor')
				# sn_root.addChild(ceil)

	###### CHANNEL #######
			elif ti==13: # channel to north
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				floor.getRigidBody().sync()
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				if x<TOTAL_WIDTH-1 and tile[z][x+1]==13:
					west = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					west.setPosition(x,0,z)
					west.setPosition(x-TILE_HALF_WIDTH,CHANNEL_HALF_HEIGHT,z)
					west.yaw(HALF_PI)
					west.clearMaterials()
					west.addMaterial(texture.side)
					west.getMaterial().setProgram('floor')
					west.getRigidBody().initialize(RigidBodyType.Plane,0)
					west.getRigidBody().sync()
					#west.setEffect('colored -d red')
					sn_root.addChild(west)

				if x>0 and tile[z][x-1]==13:
					east = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					east.setPosition(x,0,z)
					east.setPosition(x+TILE_HALF_WIDTH,CHANNEL_HALF_HEIGHT,z)
					east.yaw(-HALF_PI)
					east.clearMaterials()
					east.addMaterial(texture.side)
					east.getMaterial().setProgram('floor')
					east.getRigidBody().initialize(RigidBodyType.Plane,0)
					east.getRigidBody().sync()
					#east.setEffect('colored -e red')
					sn_root.addChild(east)

			elif ti==14: # channel to east
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				floor.getRigidBody().sync()
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				if z<TOTAL_DEEP-1 and tile[z+1][x]==14:
					north = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					north.setPosition(x,0,z)
					north.setPosition(x,CHANNEL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
					north.clearMaterials()
					north.addMaterial(texture.side)
					north.getMaterial().setProgram('floor')
					north.getRigidBody().initialize(RigidBodyType.Plane,0)
					north.getRigidBody().sync()
					#north.setEffect('colored -e red')
					sn_root.addChild(north)

				if z>0 and tile[z-1][x]==14:
					south = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					south.setPosition(x,0,z)
					south.setPosition(x,CHANNEL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
					south.pitch(pi)
					south.clearMaterials()
					south.addMaterial(texture.side)
					south.getMaterial().setProgram('floor')
					south.getRigidBody().initialize(RigidBodyType.Plane,0)
					south.getRigidBody().sync()
					#south.setEffect('colored -e red')
					sn_root.addChild(south)

			elif ti==15: # channel to south
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				floor.getRigidBody().sync()
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				if x<TOTAL_WIDTH-1 and tile[z][x+1]==15:
					west = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					west.setPosition(x,0,z)
					west.setPosition(x-TILE_HALF_WIDTH,CHANNEL_HALF_HEIGHT,z)
					west.yaw(HALF_PI)
					west.clearMaterials()
					west.addMaterial(texture.side)
					west.getMaterial().setProgram('floor')
					west.getRigidBody().initialize(RigidBodyType.Plane,0)
					west.getRigidBody().sync()
					#west.setEffect('colored -e red')
					sn_root.addChild(west)

				if x>0 and tile[z][x-1]==15:
					east = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					east.setPosition(x,0,z)
					east.setPosition(x+TILE_HALF_WIDTH,CHANNEL_HALF_HEIGHT,z)
					east.yaw(-HALF_PI)
					east.clearMaterials()
					east.addMaterial(texture.side)
					east.getMaterial().setProgram('floor')
					east.getRigidBody().initialize(RigidBodyType.Plane,0)
					east.getRigidBody().sync()
					#east.setEffect('colored -e red')
					sn_root.addChild(east)

			elif ti==16: # channel to west
				floor = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				floor.setPosition(x,0,z)
				floor.pitch(-HALF_PI)
				floor.clearMaterials()
				floor.addMaterial(texture.channel)
				floor.getMaterial().setProgram('floor')
				floor.getRigidBody().initialize(RigidBodyType.Plane,0)
				floor.getRigidBody().sync()
				sn_root.addChild(floor)

				top = PlaneShape.create(TILE_WIDTH,TILE_WIDTH)
				top.setPosition(x,CHANNEL_HEIGHT,z)
				top.pitch(HALF_PI)
				top.clearMaterials()
				top.addMaterial(texture.top)
				top.getMaterial().setProgram('floor')
				sn_root.addChild(top)

				if z<TOTAL_DEEP-1 and tile[z+1][x]==16:
					north = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					north.setPosition(x,0,z)
					north.setPosition(x,CHANNEL_HALF_HEIGHT,z-TILE_HALF_WIDTH)
					north.clearMaterials()
					north.addMaterial(texture.side)
					north.getMaterial().setProgram('floor')
					#north.setEffect('colored -e red')
					north.getRigidBody().initialize(RigidBodyType.Plane,0)
					north.getRigidBody().sync()
					sn_root.addChild(north)

				if z>0 and tile[z-1][x]==16:
					south = PlaneShape.create(TILE_WIDTH,CHANNEL_HEIGHT)
					south.setPosition(x,0,z)
					south.setPosition(x,CHANNEL_HALF_HEIGHT,z+TILE_HALF_WIDTH)
					south.pitch(pi)
					south.clearMaterials()
					south.addMaterial(texture.side)
					south.getMaterial().setProgram('floor')
					south.getRigidBody().initialize(RigidBodyType.Plane,0)
					south.getRigidBody().sync()
					#south.setEffect('colored -e red')
					sn_root.addChild(south)

	ground = PlaneShape.create(120,100)
	ground.setPosition(50,0,40)
	ground.pitch(-HALF_PI)
	ground.getRigidBody().initialize(RigidBodyType.Plane,0)
	ground.getRigidBody().sync()
	#ground.setEffect('colored -e red')
	ground.setVisible(False)

	#print me.getPosition()

generate_level()

##############################################################################################################
# EVENT FUNCTION

def onEvent():
	global me
	global isButton7down
	global wandOldPos
	global isWalking
	global end_x
	global end_z

	e = getEvent()

	if e.getServiceType()==ServiceType.Wand:
		print 'Wand'
		axis_lr = e.getAxis(0)
		axis_ud = e.getAxis(1)
		if axis_lr>0.5 or axis_lr<-0.5:
			#print 'RIGHT LEFT'
			if isWalking == False:
				isWalking = True
				playSound(sd_footstep,cam.getPosition(), 0.1)
			me.translate(axis_lr*0.07,0,0,Space.Local)
			me.getRigidBody().sync()
			e.setProcessed()
		if axis_ud>0.5 or axis_ud<-0.5:
			#print 'UP DOWN'
			if isWalking == False:
				isWalking = True
				playSound(sd_footstep,cam.getPosition(), 0.1)
			me.translate(0,0,axis_ud*0.07,Space.Local)
			me.getRigidBody().sync()
			e.setProcessed()
		if axis_lr<0.5 and axis_lr>-0.5 and axis_ud<0.5 and axis_ud>0.5:
			isWalking = False

		if e.isButtonDown(EventFlags.Button7):
			if isButton7down==False:
				isButton7down = True
				wandOldPos = e.getPosition()
				#print 'here'

		elif e.isButtonUp(EventFlags.Button7):
			isButton7down = False
			#print 'upup'
			e.setProcessed()

		elif e.isButtonDown(EventFlags.ButtonDown):
			me.getRigidBody().applyCentralImpulse(Vector3(0,240,0))
	 		e.setProcessed()

	 	elif isButton7down:
			trans = wandOldPos-e.getPosition()
			me.yaw(trans.x*HALF_PI*0.05)
			me.getRigidBody().sync()
			#print 'here!!!'
			e.setProcessed()

		elif e.isButtonDown(EventFlags.Button5):
			light_torch.setEnabled(not light_torch.isEnabled())
			light_flash.setEnabled(not light_flash.isEnabled())
			e.setProcessed()

		elif e.isButtonDown(EventFlags.ButtonUp):
			me.resetOrientation()

		elif e.isButtonDown(EventFlags.ButtonLeft):
			me.setPosition(end_x,end_z-2)
			me.resetOrientation()
			me.getRigidBody().sync()

	# if e.getSourceId()==1:

	# 	axis_left_lr = e.getAxis(0)
	# 	axis_left_ud = e.getAxis(1)
	# 	axis_right_lr = e.getAxis(2)
	# 	axis_right_ud = e.getAxis(3)

	# 	ori = None
	# 	oriVec = None

	# 	# turn
	# 	#if e.getServiceType()==ServiceType.Mocap:
	# 		#print 'mocap', e.getSourceId()
	# 	ori = e.getOrientation()
	# 	oriVec = quaternionToEuler(ori)
	# 	oriVec.y = 0
	# 	oriVec.normalize()
	# 	print 'oriVec',oriVec

	# 	# move
	# 	if axis_left_lr:# and oriVec!=None: # LEFT ANALOG LEFT-RIGHT
	# 		print 'LR',axis_left_lr
	# 		print 'LEFT-RIGHT'
	# 		me.translate(axis_left_lr*0.1*oriVec.x,0,axis_left_lr*0.1*oriVec.z,Space.Local)
	# 		e.setProcessed()
	# 	if axis_left_ud:# and oriVec!=None: # LEFT ANALOG UP-DOWN
	# 		print 'UD',axis_left_ud
	# 		print 'UP-DOWN'
	# 		me.translate(axis_left_ud*0.1*oriVec.z,0,axis_left_ud*0.1*oriVec.x,Space.Local)
	# 		e.setProcessed()

	# 	# turn
	# 	if axis_right_lr: # RIGHT ANALOG LEFT-RIGHT
	# 		me.yaw(axis_right_lr*10)
	# 		e.setProcessed()

	# 	# jump
	# 	if e.isButtonDown(EventFlags.Button3): # BUTTON A
	# 		me.getRigidBody().applyCentralImpulse(Vector3(0,120,0))
	# 		e.setProcessed()

	# 	# change light
	# 	if e.isKeyDown(ord('f')) or e.isButtonDown(EventFlags.Button5): # LB
	# 		print e.getSourceId(), e.getServiceType()
	# 		light_torch.setEnabled(not light_torch.isEnabled())
	# 		light_flash.setEnabled(not light_flash.isEnabled())
	# 		e.setProcessed()

	if e.isKeyDown(ord('a')):
		me.translate(-0.1,0,0,Space.Local)
		#print 'a'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('s')):
		me.translate(0,0,0.1,Space.Local)
		#print 's'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('d')):
		me.translate(0.1,0,0,Space.Local)
		#print 'd'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(ord('w')):
		me.translate(0,0,-0.1,Space.Local)
		#print 'w'
		me.getRigidBody().sync()
		e.setProcessed()
	elif e.isKeyDown(32):
		#me.translate(0,0.5,0,Space.Local)
		me.getRigidBody().applyCentralImpulse(Vector3(0,120,0))
		#print 'space_bar'
		e.setProcessed()

	# 	e.setProcessed()

setEventFunction(onEvent)

# pos = me.convertLocalToWorldPosition(Vector3(0,0,0))
# print pos.x, pos.z

#print 'torch_id:',torch_id
##############################################################################################################
# UPDATE FUNCTION

def dis_square(x1,y1,x2,y2):
	return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

def onUpdate(frame, t, dt):
	global torch_id
	global me
	global end_x
	global end_z
	global level
	global bgmDeltaT
	global tile
	global inChannel

	#me.getRigidBody().sync()
	#print me.getPosition()
	if t>30 and scene.isPhysicsEnabled()==False:
		print 'enabling physics'
	 	scene.setPhysicsEnabled(True)

	pos = me.getPosition()
	#print 'pos:',pos

	num = 0
	for i in xrange(0,torch_id):
		tor = sn_root.getChildByName('torch'+str(i)) # SceneNode
		fire = tor.getChildByName('support'+str(i)).getChildByIndex(0).getChildByIndex(0) # Light
		pos1 = fire.convertLocalToWorldPosition(Vector3(0,0,0))
		if dis_square(pos1.x,pos1.z,pos.x,pos.z)<100:
			fire.setEnabled(True)
			num+=1
			#print 'true'
		else:
			fire.setEnabled(False)
			#print 'false'

	print 'num:',num

	if dis_square(pos.x,pos.z,end_x, end_z)<2:
		print 'contratulations!'
		print 'entering new level!'
		level+=1
		generate_level()

	# replay bgm
	if t-bgmDeltaT>=50:
		print "replaying bgm"
		bgmDeltaT = t
		playSound(sd_bgm,cam.getPosition(),0.1)

	# play water dripping sound when entering channels
	if inChannel==False:
		if tile[int(pos.z)][int(pos.x)]==16 or tile[int(pos.z)][int(pos.x)]==13 or tile[int(pos.z)][int(pos.x)]==14 or tile[int(pos.z)][int(pos.x)]==15:
			inChannel = True
			playSound(sd_water,cam.getPosition(),0.1)
	else:
		if tile[int(pos.z)][int(pos.x)]!=16 and tile[int(pos.z)][int(pos.x)]!=13 and tile[int(pos.z)][int(pos.x)]!=14 and tile[int(pos.z)][int(pos.x)]!=15:
			inChannel = False

setUpdateFunction(onUpdate)


