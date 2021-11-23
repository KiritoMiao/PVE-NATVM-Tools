import os
exec(compile(open("config.py", "rb").read(), "config.py", 'exec'))

def ping():
    print("Pong")
    print(VMBRNM, ADDRESS, NETMASK, CIDR, PUBLIC_IF)
    return 0


def check_nat_rule(protocol, external_port, internal_ip, internal_port):
    result = os.popen("/usr/sbin/iptables -t nat -L -n")
    if protocol + " dpt:" + external_port + " to:" + internal_ip + ":" + internal_port in result.read():
        # print("Rule exist")
        return 1
    else:
        # print("Rule not exist")
        return 0


def set_nat_rule(protocol, external_port, internal_ip, internal_port):
    if check_nat_rule(protocol, external_port, internal_ip, internal_port) == 0:
        result = os.system(
            "/usr/sbin/iptables -A PREROUTING -t nat -p " + protocol + " -m " + protocol + " -i " + PUBLIC_IF + " -o " + VMBRNM + " --dport " + external_port + " -j DNAT --to-destination " + internal_ip + ":" + internal_port)
        if result == 0:
            # print("success")
            return 0
        else:
            # print("set_nat_rule error")
            return 1
    else:
        # Rule already exist
        return 2


def del_nat_rule(protocol, external_port, internal_ip, internal_port):
    if check_nat_rule(protocol, external_port, internal_ip, internal_port) == 1:
        result = os.system(
            "/usr/sbin/iptables -D PREROUTING -t nat -p " + protocol + " -m " + protocol + " -i " + PUBLIC_IF + " -o " + VMBRNM + " --dport " + external_port + " -j DNAT --to-destination " + internal_ip + ":" + internal_port)
        if result == 0:
            # print("success")
            return 0
        else:
            # print("del_nat_rule error")
            return 1
    else:
        # Rule not exist
        return 2


def clean_nat_rule():
    # clean all nat rule
    os.system("/usr/sbin/iptables -t nat -F PREROUTING")
    return 0


def save_iptables():
    # save iptables
    os.system("/usr/sbin/iptables-save > /etc/iptables/rules.v4")
    return 0
