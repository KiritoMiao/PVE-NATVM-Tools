import os


def ping():
    print("Pong")
    return 0


def check_nat_rule(protocal, externalPort, internalIp, internalPort):
    result = os.popen("/usr/sbin/iptables -t nat -L -n")
    # 如果有该规则，返回1
    if protocal + " dpt:" + externalPort + " to:" + internalIp + ":" + internalPort in result.read():
        return 1
    else:
        return 0


def set_nat_rule(protocal, externalPort, internalIp, internalPort):
    if check_nat_rule(protocal, externalPort, internalIp, internalPort) == 0:
        result = os.system(
            "/usr/sbin/iptables -A PREROUTING -t nat -p " + protocal + " -m " + protocal + " --dport " + externalPort + " -j DNAT --to-destination " + internalIp + ":" + internalPort)
        if result == 0:
            return 0
        else:
            return 1
    else:
        return 2


def del_nat_rule(protocal, externalPort, internalIp, internalPort):
    if check_nat_rule(protocal, externalPort, internalIp, internalPort) == 1:
        result = os.system(
            "/usr/sbin/iptables -D PREROUTING -t nat -p " + protocal + " -m " + protocal + " --dport " + externalPort + " -j DNAT --to-destination " + internalIp + ":" + internalPort)
        if result == 0:
            return 0
        else:
            return 1
    else:
        return 2


def cleanNatRule():
    os.system("/usr/sbin/iptables -t nat -F PREROUTING")
    return 0


def saveIptables():
    os.system("/usr/sbin/iptables-save > /etc/iptables/rules.v4")
    return 0