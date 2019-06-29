import subprocess
from subprocess import PIPE
import os
import random
import glob
import time
import ffmpy
import sys
from optparse import OptionParser


def args():
	#parse commandline args
	parser = OptionParser()

	#file path
	parser.add_option("-f", "--file", dest="filename", help="file to generate gifs from", metavar="FILE")
	#gif(s) save path (set default to mkdir in file path?)
	parser.add_option("-s", "--save", dest="savepath", help="path to save", metavar="SAVE_PATH")
	#iterations
	parser.add_option("-i", "--iterations", dest="iterations", help="number of unqiue timeframes to try", metavar="ITER")

	#start_time
	parser.add_option("-t", "--start_time", dest="start_time", help="time to start gif at", metavar="START_TIME")
	#duration
	parser.add_option("-d", "--duration", dest="duration", help="gif duration", metavar="DURATION")


	(options, args) = parser.parse_args()

	print(options.filename)
	print(options.savepath)
	print(options.iterations)
	print(options.start_time)
	print(options.duration)
	return options.filename, options.savepath, int(options.iterations), options.start_time, options.duration

def get_duration(file_path):
	#call ffprobe as subprocess and retrieve result (seconds)
	p_ = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path], stdout=PIPE, stderr=PIPE) #"-sexagesimal"
	# p_.wait()
	duration = p_.stdout.decode("utf-8")
	return duration

def envoke_shell_script(file_path, save_path, iterations, start_time=None, duration_to_grab=None):

	#get file duration
	file_duration = get_duration(file_path)
	print(type(file_duration))
	print("here: {}".format(file_duration))
	file_duration = int(file_duration.split(".")[0])

	print("----------------------------")
	print(file_path)
	print(save_path)
	print(iterations)
	print(start_time)
	print(duration_to_grab)
	print("----------------------------")

	for i in range(0,iterations):
		print("------------- IN LOOP ----------")
		print(start_time)
		print(duration_to_grab)

		if duration_to_grab is None:
			duration_to_grab = str(random.choice([0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5]))

		if start_time is None:
			print("IN START TIME")
			#get random second value fromr ange
			random_start_seconds = random.randint(0,file_duration)
			#print(random_start_seconds)
			#turn into hh:mm:ss for start_time
			random_formatted = time.strftime('%H:%M:%S', time.gmtime(random_start_seconds))
			#print(random_formatted)
			start_time = random_formatted #"0" + str(random.choice(range(0,2))) + ":" + str(random.choice(range(0,60))) + ":" + str(random.choice(range(0,60)))
			
		print("------------- POST CONTROL FLOW ----------")
		print(start_time)
		print(duration_to_grab)

		patrol_flag = "yes"
		gif_name = start_time.replace(":","_")

		#then i would do my imagemagick work
		#checkout http://docs.wand-py.org/en/0.5.1/
		#hmm, it might actually not be worth the extra effort to replace my shell script, but perhaps I can calculate extra
		#parameters to pass into the shell script for things like estimating gif size or other parameters to make the gifs better?

		#make subcall
		shell_args = [file_path, save_path, gif_name, start_time, duration_to_grab, patrol_flag]
		print(shell_args)
		p = subprocess.Popen(['/home/martin/Code/make_gif.sh', file_path, save_path, gif_name, start_time, duration_to_grab, patrol_flag])
		#waits for process to end before continuing!
		p.wait()

		time.sleep(1)

		start_time = None
		
	#p.kill()
	print("Completed")
	#return save_path, gif_name

def pick_gif(save_path, gif_name):

	#see if patrol is eligible and randomly choose from list if so
	eligible_gifs = []

	#get gif files to check
	gifs = glob.glob(save_path + "*" + gif_name + "*.gif")
	print(gifs)

	for file in gifs:

		#check mb size
		print(os.path.getsize(file)/1000000.0)
		if os.path.getsize(file)/1000000.0 < 5.0:
			eligible_gifs.append(file)

	print(eligible_gifs)

	try:
		gif_to_post = random.choice(eligible_gifs)
	except:
		return "no dice"

	print(gif_to_post)
	return gif_to_post



#RUN
def run():
	file_path, save_path, iterations, start_time, duration = args()
	envoke_shell_script(file_path, save_path, iterations, start_time, duration)


if __name__ == '__main__':
	run()
