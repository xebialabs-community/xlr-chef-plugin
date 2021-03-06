#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from chef.Workstation import Workstation

def handle_result(result):
    if result[0] != 0:
        sys.exit(result[0])
    else:
        output_handler = result[1]
        error_handler = result[2]
        result_output = parse_output(output_handler.getOutputLines())
        result_output += parse_output(error_handler.getOutputLines())
    return result_output

def parse_output(lines):
    result_output = ""
    for line in lines:
        result_output = '\n'.join([result_output, line])
    return result_output

workstation = Workstation.get_workstation(chef_workstation)
method = str(task.getTaskType()).lower().replace('.', '_')
call = getattr(workstation, method)
output = handle_result(call(locals()))