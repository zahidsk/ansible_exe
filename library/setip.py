#!/usr/bin/python

from ansible.module_utils.basic import *
import commands
import os

def get_sys_ip():
	'''
	Desc: This function return system ip
	'''
	cmd_out = commands.getstatusoutput("ifconfig eth0 |grep -e 'inet addr'")[1].strip()
	ip = cmd_out.split(" ")[1].split(':')[1]
	return ip

def static_ip_set(data):
	'''
	Desc: This api set static ip to host system.
	Argument:
	  data: data is a dictionary contaning required detail to set static ip like IP, netmask
	'''
	has_changed = False

	# check if any required argument is absent
	if not (data.get('ip', False) and data.get('netmask', False) and data.get('gateway', False)):
		meta = {"Static" : "Required parameter absent to set static ip"}		
		return (has_changed, meta)

	shell_cmd = "ifconfig eth0 %s  netmask %s"%(data.get('ip'), data.get('netmask'))
	print "Shell_cmd : ",shell_cmd
	#ret = int(commands.getstatusoutput(shell_cmd)(0))
	ret = os.system(shell_cmd)
	if ret != 0:
		meta = {'static': 'command failed to set static ip'}
		return (has_changed, meta)

	# validate ip
	sys_ip = get_sys_ip()
	if sys_ip != data.get('ip'):
		meta = {'Static': 'IP not set, expected ip is %s but set ip is %s '%(data.get('ip'), sys_ip)}
		return (has_changed, meta)
	has_changed = True
	meta = {'Static': 'Ip(%s) succesfully set'%sys_ip}
	return (has_changed, meta)
	   
def dynamic_ip_set(data):
	'''
	Desc: This API is to set Dynamic ip to host system 
	'''
	has_changed = False

	shell_cmd = "service network-manager restart"
	ret = os.system(shell_cmd)
        if ret != 0:
		meta = {"Dynamic" : "dynamic ip changed command Failed"}
                return (has_changed, meta)
	
	sys_ip = get_sys_ip()
	has_changed = True
	meta = {'Dynamic': 'DHCP assign Ip(%s) succesfully'%sys_ip}
	return (has_changed, meta)


def main():
	fields={
		"settype": {"default":'static', "type": "str", "choices":['static', 'dynamic']},
		"ip": {"required":False, "type": "str"},
		"netmask":{"required":False, "type": "str"},
		"gateway":{"required":False, "type": "str"},
		}
	choice_map = {
		'static':static_ip_set,
		'dynamic':dynamic_ip_set
		}
	module = AnsibleModule(argument_spec=fields)
	#response = {"hello":"Calsoft"}
	has_changed, result = choice_map.get(module.params['settype'])(module.params)
	module.exit_json(changed=False, meta=result)

if __name__ == '__main__':
	main()
