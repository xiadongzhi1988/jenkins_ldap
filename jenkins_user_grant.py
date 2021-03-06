import myjenkins
from myjenkins import jenkinsrole
import myldap
from myldap import ldapuser
import json
import re
import sys

#获取role信息
def get_role_info(role_type, role_name):
    jekins_role_json = j.get_role(role_type, role_name)
    js_fomat = json.dumps(jekins_role_json, sort_keys=True, indent=4)
    print(js_fomat)

#将某个角色赋予某个用户
def role_to_user(role_type, role_name, username):
    res = j.assign_role(role_type, role_name, username)
    print('%s to %s %d' %(role_name, username, res))

#删除指定用户的某个权限
def role_cancel_user(role_type, role_name, username):
    res = j.unassign_role(role_type, role_name, username)
    print('%s del %s %d' %(username, role_name, res))

#检查ldap用户是否存在
def ldap_user_exist(search_user):
    l = ldapuser.LdapOps()
    userlist = l.ldap_get_uid(l.ldap_base)
    flag = 0
    for user in userlist:
        if search_user == user:
            flag = 1
    return flag


# res = ldap_user_exist('xdz10')
# print(res)

#new_pre_jenkins
# j = jenkinsrole.JenkinsRole('192.168.41.29', '5010905')
# j.host = "192.168.41.29"
# j.port = 8080
# j.username = "5010905"
# j.token = '1130c5e4c3968bfe4c64edb9f0a8ecc5c5'


#my_jenkins
# j = jenkinsrole.JenkinsRole('10.10.111.201', 'admin')
# j.host = "10.10.111.201"
# j.port = 8080
# j.username = "admin"
# j.token = '116c82f41b96860fd566d04ec7244d1965'


j = jenkinsrole.JenkinsRole()

global_role_type = 'globalRoles'
global_role_name = 'base'

role_type = 'projectRoles'
# role_name = 'item_admin'
# role_pattern = '.*attachment.*'

# user = 'xdz11'

# role_to_user(global_role_type, global_role_name, user)
# role_to_user(role_type, role_name, user)
# get_role_info(role_type, role_name)

# role_list = ['item_cp', 'item_crm', 'item_design', 'item_dms', 'item_guimo']
# for role_name in role_list:
#     role_to_user(role_type, role_name, user)
    # role_cancel_user(role_type, role_name, user)

if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], 'role1', 'role2', '...', 'username')
else:
    user = sys.argv[-1]
    if ldap_user_exist(user):
        for i in range(1, len(sys.argv) - 1):
            role_to_user(role_type, sys.argv[i], user)
    else:
        print(user, '不存在')

# for role_pattern in role_pattern_list:
#     res_code = j.add_role(role_type, role_name, permissions, role_pattern)
#     print(res_code)

#new_pre ldap
# ldap_server = '192.168.41.13'
# ldap_user = 'cn=admin,cn=manager,dc=pre,dc=venusgroup,dc=com,dc=cn'
# ldap_pwd = 'root@123'
# ldap_search_base = 'ou=6334,ou=4474,ou=4260,ou=4259,ou=employee,dc=pre,dc=venusgroup,dc=com,dc=cn'


#myvm ldap
# ldap_server = '10.10.111.159'
# ldap_user = 'cn=admin,dc=demo,dc=com'
# ldap_pwd = '123456'
# ldap_search_base = 'ou=jenkins,dc=demo,dc=com'
# ldap_search_base = 'ou=group1,dc=demo,dc=com'

# l = ldapuser.LdapOps(ldap_server, ldap_user, ldap_pwd)
# l.ldap_server = ldap_server
# l.ldap_user = ldap_user
# l.ldap_pwd = ldap_pwd

# uid_list = l.ldap_get_uid(ldap_search_base)
# print(uid_list)

# uid = 'wuxingge2'
# ou = 'ou=group1,dc=demo,dc=com'
# l.ldap_add_user(uid, ou)
# l.ldap_del_user(uid, ou)
# l.ldap_add_group(ou)
# l.ldap_del_group(ou)

# user_list = ldapuser.ldap_get_uid(ldap_server, ldap_user, ldap_pwd, ldap_search_base)
# role_type = 'projectRoles'
# role_name = 'item_other'

# print(user_list)

#一个权限，多个用户
# for user in user_list:
    # role_to_user(role_type, role_name, user)
    # role_cancel_user(role_type, role_name, user)

#获取Jenkins所有role
# role_list = j.get_all_roles(role_type)


# for role in role_list.keys():
#     if not role == 'item_admin':
#         role_to_user(role_type, role, '5010958')
#         role_cancel_user(role_type, role, '5010958')

# for role in role_list.keys():
#     if re.search('xxl-job', role):
#         role_to_user(role_type, role, '5010958')
        # role_cancel_user(role_type, role, '5010958')


#一个用户，多个权限
# for role in role_list.keys():
#     if re.findall(r'alm|hrm|common', role):
#         role_to_user(role_type, role, '5010958')
#         # role_cancel_user(role_type, role, '5010958')

