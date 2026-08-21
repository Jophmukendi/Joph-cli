import os
import subprocess
import sys
import tempfile
from importlib.metadata import version

import requests
from packaging.version import Version


GITHUB_OWNER = "Jophmukendi"
GITHUB_REPOSITORY = "Joph-cli"
PACKAGE_NAME = "joph-cli"

API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPOSITORY}/releases/latest"
)


def get_current_version():
    return version(PACKAGE_NAME)


def get_latest_release():
    response = requests.get(
        API_URL,
        headers={
            "Accept": "application/vnd.github+json"
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def find_wheel(release):
    assets = release.get("assets", [])

    for asset in assets:
        if asset["name"].endswith(".whl"):
            return asset

    return None


def download_wheel(url, file_name):
    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    wheel_path = os.path.join(
        tempfile.gettempdir(),
        file_name,
    )

    with open(wheel_path, "wb") as file:
        file.write(response.content)

    return wheel_path


def install_wheel(wheel_path):
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            wheel_path,
        ]
    )


def update_app():
    print("Checking for updates...")

    try:
        current_version = get_current_version()
        release = get_latest_release()

        tag = release["tag_name"]
        latest_version = tag.removeprefix("v")

        print(f"Installed version: {current_version}")
        print(f"Latest version:    {latest_version}")

        if Version(latest_version) <= Version(current_version):
            print("Joph is already up to date.")
            return

        wheel = find_wheel(release)

        if wheel is None:
            print("No wheel found in the latest release.")
            return

        print(f"Downloading Joph {latest_version}...")

        wheel_path = download_wheel(
            wheel["browser_download_url"],
            wheel["name"],
        )

        print("Installing update...")

        install_wheel(wheel_path)

        print(
            f"Joph was successfully updated "
            f"to version {latest_version}."
        )

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except subprocess.CalledProcessError:
        print("Installation failed.")

    except Exception as error:
        print(f"Update error: {error}")