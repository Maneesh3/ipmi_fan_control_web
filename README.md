# IPMI Fan control web service

- Fast API, Docker, ipmi_tool on shell

## Testing
- `sudo apt install ipmitool`
- `uvicorn app:app --reload --host 0.0.0.0 --port 18081`
- `gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:18081 app:app`

## TODO
- [ ] set timeout for all requests
- [ ] set security, running shell commands 
- [ ] initial request (enabling manual fan control)
- [ ] save config user based or login based