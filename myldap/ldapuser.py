from ldap3 import Server,Connection,ALL,SUBTREE,ALL_ATTRIBUTES,MODIFY_REPLACE,MODIFY_ADD,MODIFY_DELETE, SAFE_SYNC, NTLM
import time
import re
from passlib.hash import  ldap_salted_sha1 as ssha
import yaml

class LdapInit():
    def __init__(self):
        with open('config.yml') as conf_file:
            lconf = yaml.load(conf_file, Loader=yaml.BaseLoader)
            self.ldap_server = lconf['ldap']['server']
            self.ldap_user = lconf['ldap']['user']
            self.ldap_pwd = lconf['ldap']['password']
            self.ldap_base = lconf['ldap']['ldap_base']

    def ldap_conn(self):
        server = Server(self.ldap_server)
        conn = Connection(server, self.ldap_user, self.ldap_pwd, client_strategy=SAFE_SYNC, auto_bind=True)
        return conn

class LdapOps(LdapInit):
    def __init__(self):
        super().__init__()

    # def ldap_get_uid(self, ldap_search_base):
    #     uidlist = []
    #     conn = self.ldap_conn()
    #     status, result, response, _ = conn.search(ldap_search_base, '(objectclass=*)', attributes=['*'])
    #     for i in response:
    #         searchObj = re.search('uid=\w+', i['dn'])
    #         if searchObj:
    #             uidlist.append(searchObj.group().strip('uid='))
    #     return uidlist


    def ldap_get_uid(self, ldap_search_base):
        uidlist = []
        conn = self.ldap_conn()
        status, result, response, _ = conn.search(ldap_search_base, '(objectclass=*)', attributes=['*'])
        for i in response:
            uidRegex = re.compile(r'(uid)=(\w+)')
            searchObj = uidRegex.search(i['dn'])
            if searchObj:
                uidlist.append(searchObj.group(2))
        return uidlist


    def ldap_add_user(self, uid, ou):
        conn = self.ldap_conn()
        # print(conn.add('cn=test03,ou=jenkins,dc=demo,dc=com', 'inetorgperson',
        #          {'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': 1111}))
        print(conn.add('uid=' + uid + ',' + ou, ['account', 'simpleSecurityObject', 'top'],
                                {'userPassword': ssha.encrypt('123456',salt_size=12)}))

    def ldap_del_user(self, uid, ou):
        conn = self.ldap_conn()
        print(conn.delete('uid=' + uid + ',' + ou))

    def ldap_add_group(self, ou):
        conn = self.ldap_conn()
        print(conn.add(ou, 'organizationalUnit'))

    def ldap_del_group(self, ou):
        conn = self.ldap_conn()
        print(conn.delete(ou))
