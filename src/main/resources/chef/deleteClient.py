#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
from java.lang import Exception
from chef.ChefClient import ChefClient

if chefClient is None:
   print "No server provided."
   sys.exit(1)

chefDXClient = ChefClient.createDXClient(chefClient)

try:
   data = chefDXClient.deleteClient(knifeFile, chefKey, nodeName )
except Exception, e:
   exc_info = sys.exc_info()
   traceback.printException( *exc_info )
   print e
   print chefDXClient.print_error( e )
   print "Failed to delete node %s" % (nodeName)
   sys.exit(1)