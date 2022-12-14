import sys
import subprocess
import platform
import validators


def mtu_check(mtu, host):
    checker_command = f"ping {host} -s {mtu} -c 1 -D"
    result = subprocess.Popen(checker_command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              shell=True)

    if platform.system().lower() == 'darwin':
        if result.returncode == 0:
            return 0, None
        elif result.returncode == 2:
            return 2, None
        else:
            return -1, result.stderr
    else:
        return result.returncode, result.stderr


def bin_search(L, R, host):
    while R - L > 1:
        mid_mtu = (L + R) // 2
        checker = mtu_check(mid_mtu, host)
        if not checker[0]:
            L = mid_mtu
        elif checker[0] == 2:
            R = mid_mtu
        else:
            print("ERROR: operation failed,", checker[1])
            exit(1)
    return L + 28


if len(sys.argv) != 2:
    print(f"ERROR: 1 argument expected, but {len(sys.argv) - 1} were given")
    exit(1)

host = sys.argv[1]
if not validators.domain(host):
    print("ERROR: host not valid")
    exit(1)

icmp_check = "cat /proc/sys/net/ipv4/icmp_echo_ignore_all"  # https://askubuntu.com/questions/637470/how-to-check-if-icmp-blocking-is-enabled-in-a-system
result = subprocess.run(icmp_check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.stdout:
    print("ICMP blocked")
    exit(1)

# ищем ответ бинпоиском
L = 64 - 28
R = 1519 - 28
mtu_res = bin_search(L, R, host)

print(f"SUCCESS: MTU equals {mtu_res}")
