import myldap
from myldap import ldapuser
import sys


ldap_server = '10.10.111.159'
ldap_user = 'cn=admin,dc=demo,dc=com'
ldap_pwd = '123456'
ldap_search_base = 'ou=jenkins,dc=demo,dc=com'

l = ldapuser.LdapOps(ldap_server, ldap_user, ldap_pwd)
userlist = l.ldap_get_uid(ldap_search_base)
print(userlist)