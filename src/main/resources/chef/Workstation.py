#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import os, re, sys, traceback

import java.lang.String as String

from com.xebialabs.overthere import CmdLine
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from com.xebialabs.overthere.local import LocalConnection

class Workstation(object):
    def __init__(self, workstation_config):
        self.cmd_line = CmdLine()
        self.chef_sdk_path = workstation_config['chef_sdk_path']
        self.client_key  = Workstation.format_key(workstation_config['client_key'])
        if workstation_config['os'] :
            self.os = "UNIX"
        else:
            self.os = "WINDOWS"
        self.chef_server_url = workstation_config['chef_server_url']
        self.node_name = workstation_config['node_name']
        self.log_level = workstation_config['log_level']
        self.log_location = workstation_config['log_location']
        self.cookbook_path = workstation_config['cookbook_path']
        self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
        self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

    @staticmethod
    def get_workstation(workstation_config):
        return Workstation(workstation_config)

    @staticmethod
    def format_key(key):
        chef_key = re.sub("---- .*", "----\n", key)
        footer = re.sub(".* ----", "----", key)
        body = re.sub(".*--- ", "", key)
        body = re.sub(" ---.*", "", body)
        for l in body.split():
            chef_key = "%s%s\n" % (chef_key, l)
        chef_key = "%s%s\n" % (chef_key, footer)
        return chef_key

    def bootstrap_unix(self, address, node_name, sudo, sudo_password, ssh_user, ssh_password, identity_file, run_list, options=None):
        if sudo :
            sudo_param = "--sudo"
        else:
            sudo_param = ""
        if sudo_password :
            sudo_password_param = "--use-sudo-password"
        else:
            sudo_password_param = ""
        if (type(run_list).__name__ <> 'NoneType' and len(run_list) > 0):
            run_list_param = "--run-list '%s'" % run_list
        else:
            run_list_param = ""
        try:
            #TODO: Need to figure out how to do identity file if specified, either ssh password --OR-- identity file
            return self.execute_knife_command("bootstrap --yes %s --ssh-user %s --ssh-password '%s' %s %s --node-name %s %s" \
                % (address, ssh_user, ssh_password, sudo_param, sudo_password_param, node_name, run_list_param), 'bootstrap_unix.script', options, True)
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def cookbook_list(self, options):
        return self.execute_knife_command("cookbook list", 'cookbook_list.script', options, True)

    def node_list(self, options):
        return self.execute_knife_command("node list", 'node_list.script', options, True)

    def client_list(self, options):
        return self.execute_knife_command("client list", 'client_list.script', options, True)

    def delete_node(self, node_name, options=None):
        return self.execute_knife_command("node delete --yes %s" % node_name, 'delete_node.script', options, True)

    def delete_client(self, node_name, options=None):
        return self.execute_knife_command("client delete --yes %s" % node_name, 'delete_client.script', options, True)

    def apply_cookbook_unix(self, node_name, ssh_user, ssh_password, options=None):
        return self.execute_knife_command("ssh 'name:%s' 'sudo chef-client' --yes --ssh-user %s --ssh-password '%s'" % (node_name, ssh_user, ssh_password), 'apply_cookbook_unix.script', options, True)

    def apply_cookbook_windows(self, node_name, username, password, options=None):
        return self.execute_knife_command("winrm --yes 'name:%s' 'chef-client' --winrm-user %s --winrm-password '%s'" % (node_name, username, password), 'apply_cookbook_windows.script', options, True)

    def set_runlist(self, node_name, cookbook_name, options=None):
        return self.execute_knife_command("node run_list set %s 'recipe[%s]'" % (node_name, cookbook_name), 'set_run_list.script', options, True)

    def show_node(self, node_name, options=None):
        return self.execute_knife_command("node show %s" % node_name, 'show_node.script', options, True)

    def bootstrap_windows(self, address, node_name, username, password, run_list, options=None):
        if (type(run_list).__name__ <> 'NoneType' and len(run_list) > 0):
            run_list_param = "--run-list '%s'" % run_list
        else:
            run_list_param = ""
        return self.execute_knife_command("bootstrap --yes windows winrm %s --winrm-user %s --winrm-password '%s' --node-name %s %s" % (address, username, password, node_name, run_list_param), 'bootstrap_windows.script', options, True)

    def execute_knife_command(self, command, script_name, options=None, zip_workspace=False):
        connection = None
        try:
            if type(options).__name__ <> 'NoneType' and len(options) > 0:
                options = " %s " % options
            else:
                options = ""
            connection = LocalConnection.getLocalConnection()
            workspace_path = self.create_chef_tmp_workspace(connection)
            knife_command = "#!/bin/bash\ncd %s\n%s/bin/knife %s %s" % (workspace_path, self.chef_sdk_path, command, options)
            script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), script_name))
            OverthereUtils.write(String(knife_command).getBytes(), script_file)
            script_file.setExecutable(True)
            command = CmdLine()
            command.addArgument(script_file.getPath())
            output_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
            error_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
            exit_code = connection.execute(output_handler, error_handler, command)
            if zip_workspace:
                self.zip_workspace(workspace_path, connection)
            return [exit_code, output_handler]
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)
        finally:
            if connection is not None:
                connection.close()

    def create_chef_tmp_workspace(self, connection):
        try:
            tmp_workspace_file = connection.getTempFile('tmp_workspace')
            workspace_path = re.sub('tmp_workspace', '', tmp_workspace_file.getPath())
            workspace_directory = connection.getFile(workspace_path)
            connection.setWorkingDirectory(workspace_directory)
            new_path = "%s.chef" % workspace_path
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            self.generate_knife_rb(new_path, connection)
            chef_key_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(new_path), 'chefkey.pem'))
            OverthereUtils.write(String(self.client_key).getBytes(), chef_key_file)
            script="""#!/bin/bash\ncd %s\n%s/bin/knife ssl fetch\n%s/bin/knife ssl check""" % (workspace_path, self.chef_sdk_path, self.chef_sdk_path)
            script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), 'ssl.script'))
            OverthereUtils.write(String(script).getBytes(), script_file)
            script_file.setExecutable(True)
            self.cmd_line.addArgument(script_file.getPath())
            connection.execute(self.stdout, self.stderr, self.cmd_line)
            return workspace_path
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def zip_workspace(self, workspace_path, connection):
        zip_script = "#!/bin/bash\ncd %s\ntar -czf /tmp/chef.tgz ." % workspace_path
        zip_script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), 'zip.script'))
        OverthereUtils.write(String(zip_script).getBytes(), zip_script_file)
        zip_script_file.setExecutable(True)
        command = CmdLine()
        command.addArgument(zip_script_file.getPath())
        return connection.execute(command)

    def generate_knife_rb(self, path, connection):
        knife_contents ='''current_dir = File.dirname(__FILE__)
  log_level %s
  log_location %s
  node_name "%s"
  client_key "#{current_dir}/chefkey.pem"
  chef_server_url "%s"
  Cookbook_path %s''' % (self.log_level, self.log_location, self.node_name, self.chef_server_url, self.cookbook_path)
        knife_rb_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(path), 'knife.rb'))
        OverthereUtils.write(knife_contents, knife_rb_file)

