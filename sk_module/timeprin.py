#!/usr/bin/python
import datetime
import json
import sys
import shlex
import os
#from ansible.module_utils.basic import *

#tim = str(datetime.datetime.now())
#print json.dumps({
#	"time":tim
#	})

#mod = AnsibleModule()

def main():
	arg_file = sys.argv[1]
	arg_data = file(arg_file).read()
	arg = shlex.split(arg_data)
	print arg
	for ar in arg:
		#print ar
		if '=' in ar:
			(key, val) = ar.split('=')
			print ar
			print key, val
			if key == 'time ':
				print "value :",val.split(',')
				cmd = "date -s %s"%val.split(',')[0]
				print "Command :",cmd
				rc = os.system(cmd)
				if rc !=0:
					print json.dumps({
						"failed":True, 
						"msg":"failed to set time cmd failed"
						})
					sys.exit(1)
	
				tim = str(datetime.datetime.now())
				#print json.dumps({ "time" : tim, "changed" : True})
				#mod.exit_json("time"= tim, "changed"=True)
				print json.dumps({ 
					"time" : tim
					})
				sys.exit(0)


	tim = str(datetime.datetime.now())
	print json.dumps({ "time" : tim})
	sys.exit(0)
	#print tim

if __name__=='__main__':
	main()
