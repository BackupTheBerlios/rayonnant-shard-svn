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

def onCollide( char, item ):
	if char.npc:
		if char.hasscript( 'shardscripts.npcs.rabbit' ):
			return True
		if char.baseid == 'rabbit':
			char.addscript( 'shardscripts.npcs.rabbit' )
			return True
	return False


def onWalk( char, dir, sequence ):
	food = None
	for item in wolfpack.items( char.pos.x, char.pos.y, char.pos.map, 0 ):
		if item.hasscript( 'shardscripts.npcs.rabbit' ):
			food = item
			break
	if food:
		food.delete()
		char.sound( random.choice( [ 0x03a, 0x03b, 0x03c ] ) )
		char.emote( "munch" )
		if char.hitpoints < char.maxhitpoints:
			char.hitpoints += 1
			char.updatehealth()
	if char.hasscript( 'shardscripts.npcs.rabbit' ):
		char.removescript( 'shardscripts.npcs.rabbit' )
	return True
