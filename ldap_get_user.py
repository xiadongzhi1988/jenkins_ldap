import myldap
from myldap import ldapuser
import sys


ldap_search_base = 'ou=jenkins,dc=demo,dc=com'

l = ldapuser.LdapOps()
userlist = l.ldap_get_uid(ldap_search_base)
print(userlist)