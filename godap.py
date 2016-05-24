#!/usr/bin/python3

"""
script d'envoie de user dans LDAP
"""
VERSION = 0.2
import logging
logging.basicConfig(filename='client_application.log', level=logging.DEBUG)


from ldap3 import Server, Connection, SUBTREE
from ldap3.utils.log import set_library_log_detail_level, OFF, BASIC, NETWORK, EXTENDED, PROTOCOL
import argparse

import mods.ldap



set_library_log_detail_level(BASIC)

server='ldap-130a'
dn_connect='cn=admin,dc=edelia,dc=net'
dn_pass='M0j@ve3'
con=''
users={}



#pp.get_users()

#exit()


LDAP_USER_BRANCH='ou=people,dc=edelia,dc=net'
LDAP_GROUP_BRANCH='ou=groups,dc=edelia,dc=net'
LDAP_PTF_GROUP_BRANCH='ou=ptf,ou=groups,dc=edelia,dc=net'



GROUPS = { "dev" : "4000" ,
		 "dep" : "900" ,
		 "recette" : "2000",
		 "int" : "2500"
		 }

def read_config_file() :
	config_file = 'godap.ini'


def usage() :
	print ("godap -u user -G primary_group -g grp1,grp2 -m home_directory")

def connexion():
	global con
	print ("methode de connexion")
	con=Connection(server, user=dn_connect , password=dn_pass)
	if not con.bind():
		print("error de connexion a {}".format(server) )

def get_user():
	global con
	groups_ids = []
	print ("methode de get des users")
	con.search(search_base='dc=edelia,dc=net',
	    search_filter = '(objectClass=person)',
		search_scope = SUBTREE ,
		attributes= ['*'] )
	#for entry in con.response:
	#	print(entry['dn'], entry['attributes'])
	#for entry in con.response:
		#print(entry['dn'], entry['attributes'])
	users = con.response

	#print ( att )
	#print (users)
	return users


	for i in users :
		#print ( i )
		print ("sn est : {}".format( i ) )
		#for j in i.keys() :
		#print ("j: {}".format(j) )
		dn = i["dn"]
		print ( dn )

def get_group_dn(group) :
	global con
	filter = ""
	filter = '(cn=' + group +')'
	print(filter)
	con.search(search_base='ou=groups,dc=edelia,dc=net',
		search_filter = filter,
		search_scope = SUBTREE )
		#attributes= ['*'] )

	list_of_groups_dn = con.response
	print (con.response[0]["dn"])



#def send_ldap_user_group():



#def send_ldap_request() :


if __name__ == "__main__" :

	"""
	parsage des arguments
	"""
	user_name=""
	primary_group=""
	groups=[]

	parser = argparse.ArgumentParser(description='commend line for adding a user in LDAP')

	parser.add_argument('-u', action='store',  default="none" , dest='user',help='name of the user to add')
	parser.add_argument('-n', action='store',  default="none" , dest='name',help='name of the user to add')
	parser.add_argument('-G', action='store',  default="none", dest='primary_group',help='name of the primary group of the user')
	parser.add_argument('-g', action='append',  default=[], dest='groups',help='group to add to the user')
	#parser.add_argument('count', action='store')
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	results = parser.parse_args()
	print ("options : user : {} {}, group primary : {} , groups : {}".format(results.user , results.name , results.primary_group , results.groups ))

 	#connexion()

	ls = mods.ldap.ldap(server, dn_connect, dn_pass)

	#

	get_group_dn("ptf24")

	exit()
	send_ldap_user_creation( results.user , results.primary_group , results.groups , results.name )
	exit()
	users = get_user()
	get_last_user_uid_from_group(users,"dev")
