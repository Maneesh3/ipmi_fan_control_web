import subprocess

async def run_command_test():
    command = "ipmitool -V"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode == 0:  # Check if the command was successful
        print("Output:", result.stdout)
        return "Success", result.stdout
    else:
        print("Error:", result.stderr)
        return "Error", result.stdout


async def fan_control_command(request:dict)->dict:
    command = f"ipmitool -I lanplus -H {request['ipaddress']} -U {request['username']} -P {request['password']} raw 0x30 0x30 0x02 0xff {hex(request['fanspeed'])}"
    # print(command)
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    # need to add more error types
    if result.returncode == 0:  # Check if the command was successful
        return {"code": "success", "message" : f"Fan speed set to {request['fanspeed']}% for IP {request['ipaddress']}"}
    else:
        return {"code": "error", "message" : f"Command error : {result.stdout}"}