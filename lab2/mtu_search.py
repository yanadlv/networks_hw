import sys
import subprocess
import platform
import validators


def binsearch_request(MTU):
    result = subprocess.run(f'ping {host} -c {count} -D -t 255 -s {MTU}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    # for testing on macos
    if platform.system().lower() == 'darwin':
        if result.returncode == 0:
            return 0, ""
        elif result.returncode == 2:
            return 1, result.stderr
        else:
            return 2, result.stderr
    else:
        return result.returncode, result.stderr

      

host, count = sys.argv[1], 1

if not validators.domain(host):
    print("Host is not valid")
    exit(1)

if count is None:
    count = 1
elif not count.isnumeric():
    print('Parameter c must be a number.')
    exit(1)
else:
    count = int(count)

result = subprocess.run(f'cat /proc/sys/net/ipv4/icmp_echo_ignore_all', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.wait() != 0:
    print("ICMP is blocked")
    exit(1)

left, right = 64 - 28, 1519 - 28  
while left + 1 < right:
    mid = (left + right) // 2
    # print(f'Last normal result: {left}; Current mid: {mid}')
    returncode, err = binsearch_request(mid)
    if returncode == 0:
        left = mid
    elif returncode == 1:
        right = mid
    else:
        print(f'Something goes wrong. An error is occured: {err}')
        exit(1)

print(f'MTU is {left + 28}')
