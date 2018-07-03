import ssl
import sys

import idna

__version__ = '1.0.1'


if sys.version_info[0] == 3 and sys.version_info[1] < 7:
    real_match_hostname = ssl.match_hostname

    def patched_match_hostname(cert, hostname):
        try:
            hostname = idna.encode(hostname, uts46=True).decode('ascii')
        except UnicodeError:
            hostname = hostname.encode('idna').decode('ascii')

        return real_match_hostname(cert, hostname)

    def patch_match_hostname():
        if hasattr(ssl.match_hostname, 'patched'):
            return

        ssl.match_hostname = patched_match_hostname
        ssl.match_hostname.patched = True

    def reset_match_hostname():
        if not hasattr(ssl.match_hostname, 'patched'):
            return

        ssl.match_hostname = real_match_hostname
else:
    def patched_match_hostname(cert, hostname):
        return ssl.match_hostname(cert, hostname)

    def patch_match_hostname():
        pass

    def reset_match_hostname():
        pass
