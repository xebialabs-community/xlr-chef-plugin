#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, traceback
import re
import java.lang.String as String
from java.io import PrintWriter
from java.io import StringWriter
from com.xebialabs.overthere import CmdLine
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from com.xebialabs.overthere.local import LocalConnection

class ChefClient( object ):
   def __init__(self, chefCI ):
      self.cmdLine = CmdLine()
      self.chefPath = chefCI['chefPath']
      self.chefKey  = self.formatKey( chefCI['chefKey'] )
      if chefCI['os'] :
         self.os = "UNIX"
      else:
         self.os = "WINDOWS"
      # End if
      self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
      self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()
   #
   @staticmethod
   def createDXClient( chefCI ):
      return ChefClient( chefCI )
   # End createDKClient
   #
   def knife( self, search, cmd, attribute ):
      print "kife"
      # knife ssh 'role:web' 'sudo chef-client' --ssh-user rbroker --ssh-password 'merlin1' --attribute publicip
   # End knife
   #
   def bootstrapUnix( self, address, nodeName, knifeFile, sudo, sudoPassword, sshUser, sshPassword, identity, runList ):
      if sudo :
         sudoParm = "--sudo"
      else:
         sudoParm = ""
      # End if
      if sudoPassword :
         sudoPassParm = "--use-sudo-password"
      else:
         sudoPassParm = ""
      # End if
      if (type(runList).__name__ <> 'NoneType' and len(runList) > 0):
         runOpt = "--run-list '%s'" % runList
      else:
         runOpt = ""
      # End if
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
tar -czf /tmp/chef.tgz .
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife bootstrap %s --ssh-user %s --ssh-password '%s' %s %s --node-name %s %s
""" % ( scriptPath, knifeFile, self.chefKey, self.chefPath, self.chefPath, self.chefPath, address, sshUser, sshPassword, sudoParm, sudoPassParm, nodeName, runOpt)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         traceback.print_exc(file=sys.stdout)
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End bootstrapUnix
   #
   def bootstrapWindows( self, address, nodeName, runList):
      print "bootstrap Windows"
      # knife bootstrap windows winrm ADDRESS --winrm-user USER --winrm-password 'PASSWORD' --node-name node1-windows --run-list 'recipe[learn_chef_iis]'
   # End bootstrapWindows

   def deleteNode( self, knifeFile, nodeName ):
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife node delete --yes %s
""" % ( scriptPath, knifeFile, self.chefKey, self.chefPath, self.chefPath, self.chefPath, nodeName)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def

   def deleteClient( self, knifeFile, nodeName ):
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife client delete --yes %s
""" % ( scriptPath, knifeFile, self.chefKey, self.chefPath, self.chefPath, self.chefPath, nodeName)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def


   def getCookbookList( self, knifeFile, options ):
      connection = None
      try:
         if (type(options).__name__ <> 'NoneType' and len(options) > 0):
            options = " %s " % options
         else:
            options = ""
         # End if
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife cookbook list %s
""" % ( scriptPath, knifeFile, self.chefKey, self.chefPath, self.chefPath, self.chefPath, options)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def

   def formatKey(self, key):
      chefKey=re.sub("---- .*", "----\n", key)
      foot=re.sub(".* ----", "----", key)
      body=re.sub(".*--- ", "", key)
      body=re.sub(" ---.*", "", body)
      for l in body.split():
         chefKey = "%s%s\n" % (chefKey, l)
      # End for
      chefKey = "%s%s\n" % (chefKey, foot)
      return chefKey
   # End formatKey

   def printData(self, data):
      print data
   # End def

   def printException(self, e):
      print e
   # End def

   def getStdout(self):
      return self.stdout.getOutput()
   # End getStdout

   def getStdoutLines(self):
      return self.stdout.getOutputLines()
   # End getStdoutLines

   def printStdOut(self):
      print "#===== STD Out ====\n\n"
      tmpData = self.getStdoutLines()
      for val in tmpData:
         print "%s\n" % val
      self.data = tmpData[len(tmpData)-1]
      print "#===== STD Out ====\n\n"
   # End printStdOut

   def getStderr(self):
      return self.stderr.getOutput()
   # End getStderr

   def getStderrLines(self):
      return self.stderr.getOutputLines()
   # End getStderrLines

   def printStdErr(self):
      print "#===== STD Err ====\n\n"
      tmpData = self.getStderrLines()
      for val in tmpData:
         print "%s\n" % val
      print "#===== STD Err ====\n\n"
   # End printStdOut

   def getData(self):
      return self.data
   # End getData
# End ChefClient