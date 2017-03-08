#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from chef.Workstation import Workstation

result = Workstation.get_workstation(chef_workstation).set_runlist(node_name, run_list, options)

if result[0] <> 0:
    sys.exit(result[0])
else:
    output = result[1].getOutput()