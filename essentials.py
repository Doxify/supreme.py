from time import strftime
import os

os.environ['TZ'] = 'US/Pacific'
#Colors dictionary, from https://github.com/eggins/pybase
colors = {
			"error" 		: "\033[91m",
			"success" 		: "\033[92m",
			"info" 			: "\033[96m",
			"debug" 		: "\033[95m",
			"yellow" 		: "\033[93m",
			"lightpurple" 	: "\033[94m",
			"lightgray" 	: "\033[97m",
			"clear"			: "\033[00m"
		}


#Logger for displaying time and color in the message   
def logger(color, message):
	print colors['clear'] + strftime('[%I:%M:%S]'), colors[color] + message