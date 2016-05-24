""" module de gestion LDAP """

from ldap3 import Server, Connection, SUBTREE

def testldap(line) :
    print (line)


class ldap:

    def __init__(self, server, user, password ):
        self.server = server
        self.user = user
        self.password = password
        self.con =''

        print ("init de ldap")

        self.con = Connection(self.server, user=self.user, password=self.password)
        if not self.con.bind() :
            print ("erreur de connexion a {}".format(self.server))
        else :
            print("connexion reussi")


    def get_users(self) :
        print ("methode de get des users")
        self.con.search(search_base='dc=edelia,dc=net',
                   search_filter='(objectClass=person)',
                   search_scope=SUBTREE,
                   attributes=['*'])
        #for entry in self.con.response:
        #	print(entry['dn'], entry['attributes'])
        # for entry in con.response:
        # print(entry['dn'], entry['attributes'])
        users = self.con.response

        # print ( att )
        # print (users)
        return users

    def get_group_dn(group) :

        filter = ""
        filter = '(cn=' + group +')'
        print(filter)
        self.con.search(search_base='ou=groups,dc=edelia,dc=net',
		    search_filter = filter,
		    search_scope = SUBTREE )
        #attributes= ['*'] )

	    #list_of_groups_dn = self.con.response
        print (self.con.response[0]["dn"])
        return self.con.response[0]["dn"]

    def get_groups():
        print ("methode de get des groups")

    def get_last_user_uid_from_group(users, group):
        global groups2
        print (groups2, group)
        # print("user {} et groups {}".format( users , group) )
        print("group {} {}".format(group, groups2[group]))
        uids_list = []
        for i in users:
            dn = i["dn"]
            att = i["attributes"]
            print("gid {} {}".format(att["gidNumber"][0], groups2[group]))
            for j in att:
                print ("{} : att : {} est {} ".format(dn, j, att[j]))
            if att["gidNumber"][0] == groups2[group]:
                print("bon uid du bon groupe")
                uids_list.extend(att["uidNumber"])
        print("liste des uids {}".format(uids_list))
        uids_list.sort()
        print ("ultimo uids est {}".format(uids_list[-1]))
        return uids_list[-1]

    def send_ldap_user_creation(uid, primary_group, groups, name):
        global con
        ldapuser = {}
        id_futur = 0

        ldapuser["uid"] = uid
        ldapuser["dn"] = "uid=" + uid + "," + LDAP_USER_BRANCH
        if primary_group == "recette":
            ldapuser["home"] = '/home/recette/' + uid
        else:
            ldapuser["home"] = '/home/' + uid
        ldapuser["firstname"], ldapuser["surname"] = name.split()

        users = get_user()
        id_futur = int(get_last_user_uid_from_group(users, primary_group)) + 1

        # print("add de dn : {}, uid : {},uidnumber : {} , primary_group: {} , home :{} , name : {} , surname : {} ".format(ldapuser["dn"], ldapuser["uid"],id_futur, groups2[primary_group], ldapuser["home"], ldapuser["firstname"] , ldapuser["surname"]))


        if not con.add(ldapuser["dn"], ["top", "posixAccount", "person", "organizationalPerson", "inetOrgPerson"],
                       {'uid': ldapuser["uid"], 'cn': ldapuser["uid"], 'sn': ldapuser["surname"],
                        'gidNumber': groups2[primary_group], 'homeDirectory': ldapuser["home"], 'uidNumber': id_futur,
                        'loginShell': '/bin/bash'}):
            print ("erreur de add")
