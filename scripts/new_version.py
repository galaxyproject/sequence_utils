#!/usr/bin/env python
# Modify version...
import os
import re
import subprocess
import sys
from distutils.version import StrictVersion


PROJECT_DIRECTORY = os.path.join(os.path.dirname(__file__), "..")


def main(argv):
    source_dir = argv[1]
    old_version = StrictVersion(argv[2])
    dot_at = 1
    if len(argv) > 3:
        dot_at = int(argv[3])
    old_version_tuple = old_version.version
    new_version_tuple = list(old_version_tuple)
    for i in range(len(new_version_tuple)):
        if i < dot_at:
            continue
        if dot_at == i:
            new_version_tuple[i] = old_version_tuple[i] + 1
        else:
            new_version_tuple[i] = 0
    new_version = ".".join(map(str, new_version_tuple))

    history_path = os.path.join(PROJECT_DIRECTORY, "HISTORY.rst")
    history = open(history_path).read()

    def extend(from_str, line):
        from_str += "\n"
        return history.replace(from_str, from_str + line + "\n")

    history = extend(".. to_doc", f"""
---------------------
{new_version}.dev0
---------------------

""")
    open(history_path, "w").write(history)

    source_mod_path = os.path.join(PROJECT_DIRECTORY, source_dir, "__init__.py")
    mod = open(source_mod_path).read()
    mod = re.sub(r"__version__ = '[\d\.]+'",
                 f"__version__ = '{new_version}.dev0'",
                 mod, 1)
    mod = open(source_mod_path, "w").write(mod)
    shell(["git", "commit", "-m", f"Starting work on {new_version}",
           "HISTORY.rst", f"{source_dir}/__init__.py"])


def shell(cmds, **kwds):
    p = subprocess.Popen(cmds, **kwds)
    return p.wait()


if __name__ == "__main__":
    main(sys.argv)
