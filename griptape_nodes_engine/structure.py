import json
import os
import subprocess
import time
import threading
from urllib.parse import urljoin
from attrs import define, field, Factory
from pathlib import Path
from griptape.drivers.file_manager.griptape_cloud_file_manager_driver import (
    GriptapeCloudFileManagerDriver,
)
from griptape_nodes import (
    main as nodes_main,
    _init_system_config,
    _get_current_version,
    _get_latest_version,
    INSTALL_SCRIPT,
    CONFIG_FILE,
    ENV_FILE,
    REPO_NAME,
)
from dotenv import set_key
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

API_KEY = os.getenv("GT_CLOUD_API_KEY")
BASE_URL = os.getenv("GT_CLOUD_BASE_URL", "https://cloud.griptape.ai")
NODES_HOME_DIR = Path().home() / "GriptapeNodes"
NODES_SYNC_DIR = os.environ.get("NODES_SYNC_DIR", "GriptapeNodes")


@define
class MyHandler(FileSystemEventHandler):

    bucket_id: str = field()
    workdir: str = field(default=NODES_SYNC_DIR)
    file_driver: GriptapeCloudFileManagerDriver = field(
        default=Factory(
            lambda self: GriptapeCloudFileManagerDriver(
                workdir=self.workdir, bucket_id=self.bucket_id
            ),
            takes_self=True,
        ),
    )
    exclude_patterns: list = field(default=Factory(lambda: [".env"]))

    def __hash__(self):
        # Return a hash based on the bucket_id or other immutable fields
        return hash(self.bucket_id)

    def __eq__(self, other):
        # Ensure equality is based on the bucket_id (or any other immutable fields)
        if isinstance(other, MyHandler):
            return self.bucket_id == other.bucket_id
        return False

    def on_modified(self, event):
        """Triggered when a file is modified."""
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            path = Path(str(event.src_path))
            # Check if the file is in the exclude patterns
            if any(pattern in str(path) for pattern in self.exclude_patterns):
                print(f"Skipping excluded file: {path}")
                return
            self._upload_file(path)

    def on_created(self, event):
        """Triggered when a file is created."""
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            path = Path(str(event.src_path))
            # Check if the file is in the exclude patterns
            if any(pattern in str(path) for pattern in self.exclude_patterns):
                print(f"Skipping excluded file: {path}")
                return
            self._upload_file(path)

    def on_deleted(self, event):
        """Triggered when a file is deleted."""
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            path = Path(str(event.src_path))
            self._delete_file(path)

    def sync_files(self):
        """Syncs files from Griptape Cloud to local directory."""
        try:
            files = self.file_driver.try_list_files(path="/")
            if len(files) == 0:
                print("No files found in Griptape Cloud.")
                return
            for file in files:
                file_path = Path(
                    str(file.removeprefix(f"{self.file_driver.workdir.lstrip("/")}/"))
                )
                local_file_path = NODES_HOME_DIR / file_path
                if not local_file_path.exists():
                    print(f"Downloading {file_path} to {local_file_path}")
                    data = self.file_driver.try_load_file(
                        path=str(file_path),
                    )
                    if data:
                        local_file_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(local_file_path, "wb") as f:
                            f.write(data)
                        print(f"Downloaded {file_path} to {local_file_path}")
                else:
                    print(f"File {local_file_path} already exists.")
        except Exception as e:
            print(f"Error syncing files: {e}")

    def _upload_file(self, file_path: Path):
        """Uploads the file to Griptape Cloud."""

        if not file_path.exists():
            print(f"File {file_path} does not exist.")
            return

        with open(file_path, "r") as f:
            upload_path = self._strip_local_working_dir_from_path(file_path)
            self.file_driver.try_save_file(
                path=upload_path,
                value=f.read().encode(),
            )
        print(f"Uploaded {file_path} to Griptape Cloud.")

    def _delete_file(self, file_path: Path):
        try:
            asset_path = self._strip_local_working_dir_from_path(file_path)
            self.file_driver._call_api(
                method="delete",
                path=f"/buckets/{self.file_driver.bucket_id}/assets/{self.file_driver._to_full_key(asset_path)}",
                raise_for_status=True,
            )
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    def _strip_local_working_dir_from_path(self, path):
        """Strips the local working directory from the path."""
        return str(path).replace(str(NODES_HOME_DIR), "")


def get_bucket_id() -> str:
    """Retrieves the bucket ID from the environment variable."""
    bucket_id = os.environ.get("GT_CLOUD_BUCKET_ID")
    if bucket_id:
        return bucket_id
    url = urljoin(BASE_URL, f"/api/buckets")
    res = requests.request("GET", url, headers={"Authorization": f"Bearer {API_KEY}"})
    res.raise_for_status()
    data = res.json()
    if not data["buckets"]:
        raise ValueError("No buckets found.")

    buckets_list = filter(lambda x: x["name"] != "schemas", data["buckets"])
    return list(buckets_list)[0]["bucket_id"]


def create_deployment() -> None:
    try:
        structure_id = os.environ.get("GT_CLOUD_STRUCTURE_ID")
        url = urljoin(BASE_URL, f"/api/structures/{structure_id}/deployments")
        res = requests.request(
            "POST",
            url,
            json={"force": True},
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        res.raise_for_status()
    except Exception as e:
        print(f"Error creating deployment: {e}")
        return


# Function to start the watchdog observer in a separate thread
def start_watchdog(event_handler: MyHandler) -> None:
    observer = Observer()
    observer.schedule(event_handler, str(NODES_HOME_DIR), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def auto_update() -> None:
    """Automatically updates the script to the latest version using a shell command."""
    current_version = _get_current_version()
    latest_version = _get_latest_version(REPO_NAME)

    if current_version < latest_version:
        create_deployment()
        subprocess.run(  # noqa: S603
            ["curl", "-LsSf", INSTALL_SCRIPT],  # noqa: S607
            capture_output=True,
            check=False,
            text=True,
        )


if __name__ == "__main__":

    if not API_KEY:
        raise ValueError("API_KEY environment variable is not set.")

    if not NODES_HOME_DIR.exists():
        NODES_HOME_DIR.mkdir(parents=True, exist_ok=True)

    auto_update()

    node_process = subprocess.run(
        [
            "griptape-nodes",
            "init",
            "--api-key",
            API_KEY,
            "--workspace-directory",
            str(NODES_HOME_DIR),
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    print(node_process.stdout)

    bucket_id = get_bucket_id()
    event_handler = MyHandler(
        bucket_id=bucket_id,
    )
    event_handler.sync_files()

    # Start the watchdog in a separate thread so it doesn't block the main process
    watchdog_thread = threading.Thread(
        target=start_watchdog, args=(event_handler,), daemon=True
    )
    watchdog_thread.start()

    nodes_main()
