import socket
import ipaddress


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8000: "HTTP",
    8080: "HTTP",
}


DEFAULT_TIMEOUT = 0.5
MAX_TIMEOUT = 3.0


def validate_target(target: str) -> bool:
    """
    Validate that the target is a valid IP address or hostname.
    """

    target = target.strip()

    if not target:
        return False

    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass

    if len(target) > 253:
        return False

    if target.startswith(".") or target.endswith("."):
        return False

    try:
        socket.getaddrinfo(
            target,
            None,
            type=socket.SOCK_STREAM,
        )
        return True
    except socket.gaierror:
        return False


def scan_port(
    target: str,
    port: int,
    timeout: float = DEFAULT_TIMEOUT,
):
    """
    Safely scan one TCP port.
    """

    service = COMMON_PORTS.get(port, "Unknown")

    if not validate_target(target):
        return {
            "port": port,
            "protocol": "TCP",
            "service": service,
            "state": "ERROR",
        }

    if not isinstance(port, int) or not (1 <= port <= 65535):
        return {
            "port": port,
            "protocol": "TCP",
            "service": service,
            "state": "ERROR",
        }

    timeout = min(max(float(timeout), 0.1), MAX_TIMEOUT)

    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        ) as sock:

            sock.settimeout(timeout)

            result = sock.connect_ex(
                (target, port)
            )

            if result == 0:
                state = "OPEN"
            else:
                state = "CLOSED"

            return {
                "port": port,
                "protocol": "TCP",
                "service": service,
                "state": state,
            }

    except (socket.timeout, socket.error, OSError):
        return {
            "port": port,
            "protocol": "TCP",
            "service": service,
            "state": "ERROR",
        }