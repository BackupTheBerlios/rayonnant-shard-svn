"""
/*
 * Rayonnant Scripts
 * Copyright 2004 by holders identified in shard/docs/authors.xml
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Palace - Suite 330, Boston, MA 02111-1307, USA.
 *
 * In addition to that license, if you are running this program or modified
 * versions of it on a public system you HAVE TO make the complete source of
 * the version used by you available or provide people with a location to
 * download it.
 *
 * Rayonnant Shard Home: http://developer.berlios.de/projects/rayonnant-shard/
 * Official Shard: http://shard.rayonnant.net/
 */
"""

import wolfpack
import random

def leaves_progress( leaves, args ):
	if leaves == None:
		return False
	if leaves.hastag( 'stage' ):
		stage = int( leaves.gettag( "stage" ) )
		if leaves.hastag( "picked" ):
			# Picked Apple Trees
			# Clean Picked to Decayed
			if stage == 1 and leaves.id in [ 0xd95, 0xd99 ]:
				leaves.id += 2
				leaves.settag( 'stage', 2 ) # Proceed to Stage 3
				leaves.deltag( 'picked', 0 )
				leaves.settag( 'fruit_count', 0 )
				leaves.addtimer( int( 60000 * random.randint( 2, 15 ) ), leaves_progress, [] )
				leaves.update()
				return True
		else:
			# Clean Leaves to Fruit Leaves
			if stage == 0 and leaves.id in [ 0xd95, 0xd99 ]:
				leaves.id += 1
				leaves.settag( 'stage', 1 )
				leaves.settag( 'fruit_count', int( random.randint( 5, 25 ) ) )
				leaves.addtimer( int( 60000 * random.randint( 2, 15 ) ), leaves_progress, [] )
				leaves.update()
				return True
			# Fruit Leaves to Decayed Leaves
			elif stage == 1 and leaves.id in [ 0xd96, 0xd9a ]:
				leaves.id += 1
				leaves.settag( 'stage', 2 )
				leaves.settag( 'fruit_count', 0 )
				leaves.addtimer( int( 60000 * random.randint( 2, 15 ) ), leaves_progress, [] )
				leaves.update()
				return True
			# From Dead Leaves/ Picked Leaves to Hidden Leaves
			elif stage == 2 and leaves.id in [ 0xd97, 0xd9b ]:
				leaves.settag( 'stage', 3 )
				leaves.removefromview()
				leaves.id -= 2
				leaves.visible = 0
				leaves.settag( 'fruit_count', 0 )
				leaves.addtimer( int( 60000 * 20 ), leaves_progress, [] )
				leaves.update()
				return True
			# Hidden Leaves to Visible Leaves
			elif stage == 3 and leaves.id in [ 0xd95, 0xd99 ]:
				leaves.visible = 1
				leaves.settag( 'stage', 0 )
				leaves.update()
				leaves.addtimer( int( 60000 * random.randint( 2, 15 ) ), leaves_progress, [] )
				return True
	return False

def create_leaves( serial, fruittype='apple' ):
	object = wolfpack.finditem( serial )
	# Lets figure out what kind of leaves we need
	if object.id == 0xd94:
		leaves = wolfpack.additem( 'd95' )
	elif object.id == 0xd98:
		leaves = wolfpack.additem( 'd99' )

	if leaves:
		object.settag( 'leaf_serial', leaves.serial )
		leaves = None
		leaves = wolfpack.finditem( object.gettag('leaf_serial') )
		leaves.pos = "%i,%i,%i,%i" % ( object.pos.x, object.pos.y, object.pos.z, object.pos.map )
		if leaves.pos != object.pos:
			leaves.moveto( object.pos )
		#leaves.visible = 0
		object.update()
		# 2 - 15 minutes
		leaves.addtimer( int( 60000 * random.randint( 2, 15 ) ), leaves_progress, [] )
		leaves.update()
		leaves.settag( 'fruit_count', 0 )
		leaves.settag( 'fruit_type', str( fruittype ) )
		leaves.settag( 'stage', 0 )
		return True
	else:
		object.update()
		return False

def onDelete( object ):
	if object.hastag('leaf_serial'):
		leaves = wolfpack.finditem( object.gettag('leaf_serial') )
		if leaves:
			leaves.delete()
	return True

def onCreate(object, id):
	# Let's make the tree grow up
	object.movable = 3
	if id == "apple_tree_gem":
		object.id = random.choice( [ 0xd94, 0xd98 ] )
		fruittype = 'apple'

	if create_leaves( object.serial, fruittype ):
		return True
	return False

def onUse( player, object ):
	socket = player.socket
	leaves = None
	leaves = wolfpack.finditem( object.gettag('leaf_serial') )
	leaves.pos = "%i,%i,%i,%i" % ( object.pos.x, object.pos.y, object.pos.z, object.pos.map )

	if leaves.pos != object.pos:
		leaves.moveto( object.pos )
	#leaves.visible = 0
	leaves.update()

	if leaves.hastag( 'fruit_count' ) and leaves.hastag( 'fruit_type' ):
		if int( leaves.gettag( 'fruit_count' ) ) > 0:
			socket.sysmessage( 'You pick some fruit from the tree.' )
			leaves.settag( 'fruit_count', int( int( leaves.gettag( 'fruit_count' ) ) - 1 ) )
			fruit = leaves.gettag( 'fruit_type' )
			# Create the fruit
			if fruit == 'apple':
				item = wolfpack.additem( '9d0' )
			else:
				item = None
			if item:
				if not wolfpack.utilities.tocontainer( item, player.getbackpack() ):
					item.update()
			if int( leaves.gettag( 'fruit_count' ) ) == 0:
				leaves.settag( "picked", 1 )
				leaves.id -= 1
				leaves.update()
		else:
			socket.sysmessage( 'This tree has no fruit to gather.' )
	return True
