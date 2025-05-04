#!/usr/bin/env python3
import os
import glob
import difflib
import shutil
import sys


def say(msg='', end="\n"):
    print(msg, file=sys.stderr, end=end)


def get_terminal_columns():
    return shutil.get_terminal_size((80, 20)).columns


def list_packages():
    return sorted(glob.glob("../packages/xchainpy_*"))


def display_packages(packages, columns=3, column_width=40):
    say("Available packages:")
    for i, pkg in enumerate(packages):
        label = f"{i + 1}) {os.path.basename(pkg)}"
        say(label.ljust(column_width), end="")
        if (i + 1) % columns == 0:
            say()
    if len(packages) % columns != 0:
        say()  # Ensure newline at end


def fuzzy_match(packages, query):
    base_names = [os.path.basename(p) for p in packages]
    matches = [p for p in packages if query.lower() in os.path.basename(p).lower()]
    if not matches:
        # Try fuzzy matching using difflib
        close = difflib.get_close_matches(query, base_names, n=3, cutoff=0.5)
        matches = [p for p in packages if os.path.basename(p) in close]
    return matches


def ask_for_package():
    packages = list_packages()
    if not packages:
        say("No packages found.")
        return

    while True:
        display_packages(packages)

        say("Which package do you want to select (enter number or search)?")
        choice = input().strip()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(packages):
                selected = packages[index]
                break
            else:
                say("❌ Invalid number. Try again.")
        else:
            matches = fuzzy_match(packages, choice)
            if len(matches) == 1:
                selected = matches[0]
                break
            elif len(matches) > 1:
                say("🔍 Multiple matches found:")
                for m in matches:
                    say(f"- {os.path.basename(m)}")
                say("❗ Be more specific.\n")
            else:
                say("❌ No matches found. Try again.\n")

    say(f"\n✅ Selected package: {selected}")
    print(selected)
    return selected


if __name__ == "__main__":
    ask_for_package()
