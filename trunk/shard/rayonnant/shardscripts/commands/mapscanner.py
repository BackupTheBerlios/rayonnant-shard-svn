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

from wolfpack import *
from wolfpack.utilities import *
from wolfpack.consts import *

def doscan( socket, command, arguments ):
	# var = 4
	var = 8
	# var = 16
	# var = 32
	# var = 64
	subvar = (var - 1)
	map = 0
	x = 0
	y = 0
	x_max = 6143
	y_max = 4095
	i = 0
	doregion = 0
	output = open( './resgrid_map' + str(map) + '.xml', "wb" )
	output.write("# Ore Resource Grid Test\n# ID,x1,y1,x2,y2,map\n\n")
	while y <= y_max:
		while x <= x_max:
			ytemp = y
			xtemp = x
			while ytemp <= (y + subvar) and doregion == 0:
				while xtemp <= (x+subvar) and doregion == 0:
					mapdata = wolfpack.map( xtemp, ytemp, map )
					staticdata = wolfpack.statics( xtemp, ytemp, map )
					if ismountainorcave( mapdata['id'] ):
						doregion = 1
					if doregion == 0 and staticdata:
						for static in staticdata:
							if ismountainorcave( static['id'] ):
								doregion = 1
					xtemp += 1
				ytemp += 1
			if doregion == 1:
				output.write("%i,%i,%i,%i,%i,%i\n" % ( i, x, y, (x+subvar), (y+subvar), map ) )
				i += 1
			x += var
		x = 0
		y += var
	output.write( "\n" )
	output.close()
	return

def onLoad():
	wolfpack.registercommand( "resgridscan0", doscan )
	return
