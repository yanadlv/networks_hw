import sys
import subprocess
import validators


def mtu_check(mtu, host):
    try:
        checker_command = ['ping', host, '-s', str(mtu), '-c', '1', '-M', 'do']
        result = subprocess.run(checker_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        raise Exception("ERROR: operation failed")
    return result.returncode


def bin_search(L, R, host):
    while R - L > 1:
        mid_mtu = (L + R) // 2
        if not mtu_check(mid_mtu, host):
            L = mid_mtu
        else:
            R = mid_mtu
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
if result.wait() != 0:
    print("ICMP blocked")
    exit(1)

# ищем ответ бинпоиском
L = 64 - 28
R = 1519 - 28
mtu_res = bin_search(L, R, host)

print(f"SUCCESS: MTU equals {mtu_res}")
