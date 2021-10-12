#!/usr/bin/env python
# Little script to make HISTORY.rst more easy to format properly, lots TODO
# pull message down and embed, use arg parse, handle multiple, etc...
import os
import sys
import textwrap
import urllib.parse

try:
    import requests
except ImportError:
    requests = None

PROJECT_DIRECTORY = os.path.join(os.path.dirname(__file__), "..")
new_path = [PROJECT_DIRECTORY]
new_path.extend(sys.path[1:])  # remove scripts/ from the path
sys.path = new_path

import galaxy_utils as project  # noqa: E402

PROJECT_OWNER = project.PROJECT_OWNER
PROJECT_NAME = project.PROJECT_NAME
PROJECT_URL = project.PROJECT_URL
PROJECT_API = PROJECT_URL.replace("https://github.com/", "https://api.github.com/repos/") + "/"


def main(argv):
    history_path = os.path.join(PROJECT_DIRECTORY, "HISTORY.rst")
    history = open(history_path).read()

    def extend(from_str, line):
        from_str += "\n"
        return history.replace(from_str, from_str + line + "\n")

    ident = argv[1]

    message = ""
    if len(argv) > 2:
        message = argv[2]
    elif not (ident.startswith("pr") or ident.startswith("issue")):
        api_url = urllib.parse.urljoin(PROJECT_API, f"commits/{ident}")
        req = requests.get(api_url).json()
        commit = req["commit"]
        message = commit["message"]
        message = get_first_sentence(message)
    elif requests is not None and ident.startswith("pr"):
        pull_request = ident[len("pr"):]
        api_url = urllib.parse.urljoin(PROJECT_API, f"pulls/{pull_request}")
        req = requests.get(api_url).json()
        message = req["title"]
    elif requests is not None and ident.startswith("issue"):
        issue = ident[len("issue"):]
        api_url = urllib.parse.urljoin(PROJECT_API, f"issues/{issue}")
        req = requests.get(api_url).json()
        message = req["title"]
    else:
        message = ""

    to_doc = message + " "

    if ident.startswith("pr"):
        pull_request = ident[len("pr"):]
        text = f".. _Pull Request {pull_request}: {PROJECT_URL}/pull/{pull_request}"
        history = extend(".. github_links", text)
        to_doc += f"`Pull Request {pull_request}`_"
    elif ident.startswith("issue"):
        issue = ident[len("issue"):]
        text = f".. _Issue {issue}: {PROJECT_URL}/issues/{issue}"
        history = extend(".. github_links", text)
        to_doc += f"`Issue {issue}`_"
    else:
        short_rev = ident[:7]
        text = ".. _{short_rev}: {PROJECT_URL}/commit/{short_rev}"
        history = extend(".. github_links", text)
        to_doc += f"{short_rev}_"

    to_doc = wrap(to_doc)
    history = extend(".. to_doc", to_doc)
    with open(history_path, "w") as fh:
        fh.write(history)


def get_first_sentence(message):
    first_line = message.split("\n")[0]
    return first_line


def wrap(message):
    wrapper = textwrap.TextWrapper(initial_indent="* ")
    wrapper.subsequent_indent = '  '
    wrapper.width = 78
    return "\n".join(wrapper.wrap(message))


if __name__ == "__main__":
    main(sys.argv)
