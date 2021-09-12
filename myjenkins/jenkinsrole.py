import requests
import json

class JenkinsRole:
    def __init__(self, host, username, port=8080, password=None, token=None, ssl=False):
        """
        password和token使用其中一个即可
        :param host: Jenkins主机
        :param username: 管理员用户
        :param port: Jenkins端口
        :param password: 管理员密码
        :param token: 管理员的Token
        :param ssl: Jenkins地址是否是https协议
        """
        self.host = host
        self.username = username
        self.port = port
        self.password = password
        self.token = token
        self.ssl = ssl

    @property
    def pwd_or_token(self):
        if self.password and self.token:
            raise ConnectionError("password与token填写一个即可")
        return self.password if self.password else self.token

    @property
    def proto(self):
        return 'https' if self.ssl else 'http'

    def get_crumb(self) -> dict:
        res = requests.get(
            f'{self.proto}://{self.username}:{self.pwd_or_token}@{self.host}:{self.port}/crumbIssuer/api/xml?'
            f'xpath=concat(//crumbRequestField,":",//crumb)')

        return {res.text.split(':')[0]: res.text.split(':')[1]}

    def add_role(self, role_type, role_name, permissions: str, role_pattern=None, overwrite=True):
        """
        添加角色
        如果添加的权限不属于对应的角色类型，两种情况：
        1、添加的权限都不属于对应的角色类型，则会添加一个空权限的角色
        比如向projectRoles中添加视图权限hudson.model.View.Create命名为p1,
        则在projectRoles列表中依然会添加p1角色，但是该角色没有任何权限

        2、添加的权限部分不属于对应的角色类型，则会将属于该角色类型的权限添加上

        :param role_type: 只能是globalRoles或projectRoles或slaveRoles
        :param role_name: 角色名称
        :param permissions: 角色ID，多个角色ID使用 , 号隔开，比如：'hudson.model.Hudson.Read,hudson.model.Computer.Build'
        :param role_pattern: 角色模式，支持正则表达式，当添加的是项目角色时需要指定
        :param overwrite: 如果新增的权限已经存在是否覆盖，如果选择不覆盖，即使权限已经存在，也不会返回任何报错
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        if role_type in ('projectRoles', 'slaveRoles') and not role_pattern:
            raise AttributeError("如果增加项目权限或节点权限，必须指定role_pattern，否则将匹配 .* ")

        role_data = {
            "type": role_type,
            "roleName": role_name,
            "permissionIds": permissions,
            "overwrite": overwrite,
            "pattern": role_pattern
        }

        headers = self.get_crumb()

        res = requests.post(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/addRole', data=role_data,
                            headers=headers, auth=(self.username, self.pwd_or_token))
        return res.status_code

    def get_role(self, role_type, role_name):
        """
        获取指定角色的详细，返回结果示例：
        {'permissionIds': {'hudson.model.Computer.Build': True}, 'sids': ['admin']}
        :param role_type:
        :param role_name:
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        params = {
            "type": role_type,
            "roleName": role_name
        }

        res = requests.get(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/getRole',
                           params=params, auth=(self.username, self.pwd_or_token))
        return res.json()

    def remove_roles(self, role_type, role_names: str):
        """
        删除权限
        :param role_type:
        :param role_names: 多个角色用 , 号隔开
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        data = {
            'type': role_type,
            'roleNames': role_names
        }

        headers = self.get_crumb()

        res = requests.post(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/removeRoles', data=data,
                            headers=headers, auth=(self.username, self.pwd_or_token))
        return res.status_code

    def assign_role(self, role_type, role_name, sid):
        """
        将某个角色赋予某个用户
        注意：如果赋予用户某个不存在的权限也不会报错
        :param role_type:
        :param role_name: (单个角色)
        :param sid: 用户名称(单个用户)
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        data = {
            'type': role_type,
            'roleName': role_name,
            'sid': sid
        }

        headers = self.get_crumb()

        res = requests.post(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/assignRole', data=data,
                            headers=headers, auth=(self.username, self.pwd_or_token))
        return res.status_code

    def delete_roles_from_sid(self, role_type, sid):
        """
        删除指定用户所有的相关权限
        注意：如果指定了一个不存在的用户，也不会报错
        :param role_type:
        :param sid: 单个用户
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        data = {
            'type': role_type,
            'sid': sid
        }

        headers = self.get_crumb()

        res = requests.post(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/deleteSid', data=data,
                            headers=headers, auth=(self.username, self.pwd_or_token))
        return res.status_code

    def unassign_role(self, role_type, role_name, sid):
        """
        删除指定用户的某个权限
        注意：即使指定一个不存在的用户或不存在的role，也不会返回错误
        :param role_type:
        :param role_name:
        :param sid:
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        data = {
            'type': role_type,
            'roleName': role_name,
            'sid': sid
        }

        headers = self.get_crumb()

        res = requests.post(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/unassignRole', data=data,
                            headers=headers, auth=(self.username, self.pwd_or_token))
        return res.status_code

    def get_all_roles(self, role_type):
        """
        获取指定类型角色下的所有角色以及角色下的用户
        返回结果示例：{"p1":[],"p2":["zm"],"test":["zm"]}
        :param role_type:
        :return:
        """
        if role_type not in ('globalRoles', 'projectRoles', 'slaveRoles'):
            raise AttributeError("role_type必须是'globalRoles', 'projectRoles', 'slaveRoles' 其中一个")

        params = {
            "type": role_type
        }

        res = requests.get(f'{self.proto}://{self.host}:{self.port}/role-strategy/strategy/getAllRoles',
                           params=params, auth=(self.username, self.pwd_or_token))
        return res.json()
