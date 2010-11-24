#!/usr/bin/python
"""
Pre-Commit hook checking for pep8 complience and pyflakes errors.

Pro Tip: Ignore errors with ``git commit -n``.
"""

import sys
import re
import subprocess


_MODIFIED_RE = re.compile('^(?:M|A)..(?P<name>.*\.py)', re.M)


def main():
    p = subprocess.Popen(['git', 'status', '--porcelain'],
                         stdout=subprocess.PIPE)
    out, err = p.communicate()
    modifieds = _MODIFIED_RE.findall(out)

    rrcode = 0
    for file in modifieds:
        p = subprocess.Popen(['pep8', '--repeat', '--show-source', file],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out or err:
            sys.stdout.write(" * pep8:\n%s\n%s" % (out, err))
            rrcode = rrcode | 1
        retcode = subprocess.call(['pyflakes', file])
        rrcode = retcode | rrcode

    sys.exit(rrcode)


if __name__ == '__main__':
    main()
