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
from wolfpack.consts import *
from wolfpack import console, accounts, sockets
import random
from threading import Thread, Event, Lock
import time

from shardscripts.server.consts import SHARDSTATUS

interval = float( 30 )
processthread = None

address = SHARDSTATUS[0]
output_file = SHARDSTATUS[1]
#time = SHARDSTATUS[2]

class ProcessThread(Thread):
	# Initialize this thread
	def __init__(self):
		Thread.__init__(self)
		self.stopped = Event() # Cancel Event
		self.mutex = Lock()
		self.processed = True # Start as True

	# This code runs in a separate thread
	def run(self):
		global interval

		while not self.stopped.isSet():
			# Get the processing state
			self.mutex.acquire()
			processed = self.processed
			self.mutex.release()
			# Create the page.
			if processed and wolfpack.isrunning():
				self.processed = False
				wolfpack.queuecode( autostatuswrapper, ( None, None ) )
			# Wait for the next timer to pass.
			self.stopped.wait(interval)

def autostatuswrapper( object, args ):
	WritePage( 'Online' )

def WritePage( status='Online' ):
	global processthread
	console.log(LOG_MESSAGE, "Generating Shard Status Page.\n")
	# Default/Static Information
	if status != 'Online' and status != 'Offline':
		status = "Unknown"

	#Prepare Information
	uptime = wolfpack.time.currenttime() / 1000

	# Build an uptime:
	upseconds = 0
	upminutes = 0
	uphours = 0
	updays = 0
	upseconds = uptime
	upminutes = uptime / 60
	upseconds -= upminutes * 60
	if upseconds <= 9:
		upseconds = '0%s' % upseconds
	uphours = upminutes / 60
	upminutes -= uphours * 60
	if upminutes <= 9:
		upminutes = '0%s' % upminutes
	if uphours <= 9:
		uphours = '0%s' % uphours

	#Make a time string
	timestring = '%s:%s:%s' % ( uphours, upminutes, upseconds )

	# Account Counting
	accountcount = 0
	admincount = 0
	gmcount = 0
	seercount = 0
	counselorcount = 0
	playercount = 0
	players = ""
	# ACC List
	for i in accounts.list():
		record = accounts.find( i )
		if record.acl == 'admin':
			admincount += 1
		elif record.acl == 'gm':
			gmcount += 1
		elif record.acl == 'seer':
			seercount += 1
		elif record.acl == 'counselor':
			counselorcount += 1
		elif record.acl == 'player':
			playercount += 1

	#Write the page
	file = open( output_file, 'w' )
	outputtext = "<div class='box' style='min-width:480px;width:90%;'>\n"
	outputtext += "<table class='contentinfo' style='width:100%;' cellpadding='0' cellspacing='0'>\n"
	outputtext += "<caption>Rayonnant Server Status [ <?=$phase?> ]</caption>\n"
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span style='font-weight:bold;'>Server&#160;Address:</span>&#160;</td>"
	outputtext += "<td>&#160;<span class='server_good'>%s</span></td></tr>\n" % ( address )
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span style='font-weight:bold;'>Server&#160;Status:</span>&#160;</td>"
	if status == 'Online':
		outputtext += "<td>&#160;<span class='server_good'>%s</span></td></tr>\n" % ( status )
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span style='font-weight:bold;'>Server&#160;Uptime:</span>&#160;</td>"
		outputtext += "<td>&#160;<span class='server_good'>%s</span></td></tr>\n" % ( timestring )
	elif status == 'Offline':
		outputtext += "<td>&#160;<span class='server_bad'>%s</span></td></tr>\n" % ( status )
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span style='font-weight:bold;'>Previous&#160;Uptime:</span>&#160;</td>"
		outputtext += "<td>&#160;<span class='server_bad'>%s</span></td></tr>\n" % ( timestring )
	else:
		outputtext += "<td>&#160;<span class='server_neutral'>%s</span></td></tr>\n" % ( status )
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span style='font-weight:bold;'>Server&#160;Uptime:</span>&#160;</td>"
		outputtext += "<td>&#160;<span class='server_neutral'>%s</span></td></tr>\n" % ( timestring )
	outputtext += "<tr><td style='width:90px;'>"
	outputtext += "<span style='font-weight:bold;'>Server&#160;Version:</span>&#160;</td>"
	outputtext += "<td>&#160;<span class='server_good'>%s</span></td></tr>\n" % ( wolfpack.serverversion() )
	if status == 'Online':
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span style='font-weight:bold;'>Accounts:</span>&#160;</td><td></td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;/&#160;<span class='server_good'>%s</span></td>" % ( wolfpack.sockets.count(), wolfpack.accounts.count() )
		outputtext += "<td style='text-indent:1em;'>&#160;Online&#160;/&#160;Total Accounts</td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( admincount )
		outputtext += "<td style='text-indent:1em;'>&#160;Admin&#160;Accounts</td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( gmcount )
		outputtext += "<td style='text-indent:1em;'>&#160;GM&#160;Accounts</td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( seercount )
		outputtext += "<td style='text-indent:1em;'>&#160;Seer&#160;Accounts</td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( counselorcount )
		outputtext += "<td style='text-indent:1em;'>&#160;Counselor&#160;Accounts</td></tr>\n"
		outputtext += "<tr><td style='width:90px;text-align:right;'>"
		outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( playercount )
		outputtext += "<td style='text-indent:1em;'>&#160;Player&#160;Accounts</td></tr>\n"
	# Statistics Item/Char Totals
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span style='font-weight:bold;'>Statistics:</span>&#160;</td><td></td></tr>\n"
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( wolfpack.playercount() )
	outputtext += "<td style='text-indent:1em;'>&#160;Total&#160;Players</td></tr>\n"
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( wolfpack.itemcount() )
	outputtext += "<td style='text-indent:1em;'>&#160;Total&#160;Items</td></tr>\n"
	outputtext += "<tr><td style='width:90px;text-align:right;'>"
	outputtext += "<span class='server_neutral'>%s</span>&#160;</td>" % ( wolfpack.npccount() )
	outputtext += "<td style='text-indent:1em;'>&#160;Total&#160;NPCs</td></tr>\n"
	outputtext += "</table>\n"
	outputtext += "</div>\n"
	file.write( outputtext )
	file.close()
	wolfpack.addtimer( 1000, autostatuswrapper )
	processthread.mutex.acquire()
	processthread.processed = True
	processthread.mutex.release()
	return True

def onLoad():
	# Send a message to the log
	console.log(LOG_MESSAGE, "Starting shard status page thread.\n")
	# Create the worker thread
	global processthread
	processthread = ProcessThread()
	processthread.start()
	return

def onUnload():
	console.log(LOG_MESSAGE, "Stopping shard status page thread.\n")
	global processthread
	if processthread:
		processthread.stopped.set()
		time.sleep( 0.01 ) # Sleep a little to give the thread time to exit
		if processthread:
			processthread.join()
		processthread = None
	return
