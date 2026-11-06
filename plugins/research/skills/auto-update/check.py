r"""Tell whether the libraries of an environment are behind GitHub and list the latest pull requests of the projects.

Run it with the Python of the project environment (standard library only), e.g.
`python check.py --since 2026-11-04T08:00`. Python 3.6 or later; comparing the libraries needs 3.8 or later.
"""

import argparse
import json
import re
import urllib.error
import urllib.request

# fmt: off
#
# ----- Libraries compared with their branch on GitHub, projects whose pull requests are read
#
LIBRARIES = {
    "albus"  : ("VikVador/Albus",  "main"),
    "shaggy" : ("VikVador/Shaggy", "master"),
}
PROJECTS     = ["VikVador/Heimdall", "VikVador/Neptune"]
NUMBER_PULLS = 3
MAX_FILES    = 15
# fmt: on


def github(path: str) -> "dict | list":
    r"""Read one endpoint of the public GitHub API, without any token.

    Arguments:
        path : Path of the endpoint, e.g. "repos/VikVador/albus".

    Returns:
        content : Decoded JSON answer.
    """
    request = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "research-up-to-date"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def installed_commit(name: str) -> "tuple[str | None, str]":
    r"""Find the commit from which a library of the current environment was installed.

    Arguments:
        name : Name of the distribution, e.g. "shaggy".

    Returns:
        commit : Installed commit, or None when it cannot be compared with GitHub.
        status : Why there is no commit, empty otherwise.
    """
    try:
        import importlib.metadata  # Python 3.8 or later
    except ImportError:
        return None, "Python 3.8 or later is needed to read the installed version"
    try:
        distribution = importlib.metadata.distribution(name)
    except importlib.metadata.PackageNotFoundError:
        return None, "not installed in this environment"
    origin = json.loads(distribution.read_text("direct_url.json") or "{}")
    if origin.get("dir_info", {}).get("editable"):
        return None, f"editable install from {origin.get('url')}, update it with git pull"
    commit = origin.get("vcs_info", {}).get("commit_id")
    if commit is None:
        return None, f"version {distribution.version} not installed from git, not compared"
    return commit, ""


def report_library(name: str, repository: str, branch: str) -> "list[str]":
    r"""Describe how far an installed library is behind its branch on GitHub.

    Arguments:
        name       : Name of the distribution.
        repository : GitHub repository, e.g. "VikVador/shaggy".
        branch     : Branch the environment follows.

    Returns:
        lines : Lines of the report for this library.
    """
    commit, status = installed_commit(name)
    if commit is None:
        return [f"{name}: {status}"]
    compare = github(f"repos/{repository}/compare/{commit}...{branch}")
    if compare["ahead_by"] == 0:
        return [f"{name}: up to date (commit {commit[:7]} = {branch})"]
    lines = [
        f"{name}: BEHIND by {compare['ahead_by']} commits (installed {commit[:7]}, "
        f"{branch} is {compare['commits'][-1]['sha'][:7]}), update with:",
        f"    pip install --no-deps --force-reinstall git+https://github.com/{repository}@{branch}",
    ]
    for item in compare["commits"]:
        lines.append(
            f"    {item['commit']['author']['date'][:10]}  {item['commit']['message'].splitlines()[0]}"
        )
    files = [item["filename"] for item in compare.get("files", [])]
    shown = ", ".join(files[:MAX_FILES]) + (" ..." if len(files) > MAX_FILES else "")
    lines.append(f"    files changed ({len(files)}): {shown}")
    return lines


def versions() -> str:
    r"""Give the installed commit of each library on one line, to write next to a result.

    Returns:
        line : e.g. "albus 32ebf6b, shaggy 6095950".
    """
    parts = []
    for name in LIBRARIES:
        commit, status = installed_commit(name)
        parts.append(f"{name} {commit[:7]}" if commit else f"{name} ({status.split(',')[0]})")
    return ", ".join(parts)


def summary_of(body: "str | None") -> str:
    r"""Extract the "Summary" section of the body of a pull request.

    Arguments:
        body : Markdown body of the pull request.

    Returns:
        summary : Text of the section on one line, or the start of the body without such a section.
    """
    body = body or ""
    match = re.search(r"^##\s*Summary\s*\n(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    text = (match.group(1) if match else body[:400]).split("🤖")[0]
    return " ".join(text.split())


def report_project(repository: str, since: str) -> "list[str]":
    r"""List the latest pull requests of a project.

    Arguments:
        repository : GitHub repository, e.g. "VikVador/Heimdall".
        since      : Time of the last check (YYYY-MM-DDTHH:MM, UTC), pull requests updated after it are NEW.

    Returns:
        lines : Lines of the report for this project.
    """
    pulls = github(
        f"repos/{repository}/pulls?state=all&sort=created&direction=desc&per_page={NUMBER_PULLS}"
    )
    lines = [f"{repository}:"]
    for pull in pulls:
        state = "merged" if pull["merged_at"] else pull["state"]
        new = " NEW" if since and pull["updated_at"][:16] >= since else ""
        lines += [
            f"  #{pull['number']} [{state}{new}] {pull['created_at'][:10]} {pull['title']}",
            f"      {pull['html_url']}",
            f"      {summary_of(pull['body'])}",
        ]
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--since", default="", help="time of the last check, YYYY-MM-DDTHH:MM (UTC)"
    )
    parser.add_argument("--no-libraries", action="store_true", help="only the pull requests")
    parser.add_argument("--versions", action="store_true", help="only the installed commits")
    arguments = parser.parse_args()
    if arguments.versions:
        print(versions())
        return

    libraries = [(name, *source) for name, source in LIBRARIES.items()]
    sections = [] if arguments.no_libraries else [("LIBRARIES", report_library, libraries)]
    sections.append(("PULL REQUESTS", report_project, [(p, arguments.since) for p in PROJECTS]))
    for title, report, items in sections:
        print(f"===== {title}")
        for item in items:
            try:
                print("\n".join(report(*item)))
            except (urllib.error.URLError, KeyError, TimeoutError) as error:
                print(f"{item[0]}: ERROR - GitHub could not be read ({error}).")


if __name__ == "__main__":
    main()
