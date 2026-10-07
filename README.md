
# live-vcs

![Tests](https://github.com/amelfia/live-vcs/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight, automated version control system tailored for **Ableton Live** projects.

![demo](assets/demo.gif)

## Motivation

Standard VCS tools like Git struggle with audio production: Ableton `.als` files are gzipped XML binaries, and saving manually interrupts the creative workflow. live-vcs automatically detects project saves in the background, generates content digests of the uncompressed XML, and manages an annotated snapshot history with branching, restoring, and DAG graph visualization.

---

## Key Features

- **Automated Save Detection:** Listens to filesystem events using `watchdog` to capture project states the instant you save in Ableton (`Cmd+S` / `Ctrl+S`).
- **Gzip XML Hashing:** Inflates `.als` archives in-memory and digests only the raw XML structure via MD5, ignoring filesystem metadata noise.
- **Branching & Directed Graph:** Full support for branching workflows (`branch`, `switch`) and an ASCII-rendered DAG history graph.
- **In-Place Workspace Restoration:** Restoring a commit (`load`) overwrites the active project file directly, preserving Ableton's relative sample paths while retaining immutable archives.
- **Thread-Safe CLI Loop:** Coordinates background file watchers and user terminal commands concurrently using non-blocking I/O (`select.select`) and thread synchronization primitives.

---

## Architecture

```text
Ableton Live (Editor)
       │  (Cmd + S)
       ▼
 [File System] ──(Watchdog Event)──► [hash_watcher.py]
                                            │
                                            ▼
                                   [hash_generator.py]
                                (Decompress .als & MD5)
                                            │
                                            ▼
                                 [write_commit_to_json.py]
                                            │
                             ┌──────────────┴──────────────┐
                             ▼                             ▼
                    [snapshot_hashes.json]            [snapshots/]
                      (DAG / Branch Pointer)      (Immutable ALS copies)
```

## History Graph Demo
``` text
* d4a2f81 Main synth melody sketch
|
* 1a9b2c3 synth double
|\
| * 7f2b1a4 Add vocal chop processing (vocal-chop)
| |
| * 3c8e190 Sidechain sub bass to kick
|/
|
* 3434343 init
``` 

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) or standard Python `venv`

## Quick Start

**1. Clone the repository**

```bash
git clone https://github.com/amelfia/live-vcs.git
cd live-vcs
```

**2. Create a virtual environment and install dependencies**

Using uv (recommended):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or using standard pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run the tool:

```bash
./main.sh
```

Or directly via Python:

```bash
python src/main.py
```

Enter the path to your Ableton project directory when prompted.


## Usage

| Command | Description |
|---------|-------------|
| `graph` | Render ASCII directed acyclic history graph of all branches and commits |
| `branch <name>` | Create a new branch pointing to the current commit |
| `switch <name>` | Switch working pointer to another branch |
| `load` | Restore project workspace to a specific commit hash |
| `quit` | Exit the CLI watcher cleanly |

## Contributing

### Run the test suite

The test suite covers branch pointers, hash generation, snapshot resolution, and handler error boundaries.

```bash
./test.sh
```

### Submit a pull request

Fork the repository and open a pull request.

## Platform Support

| Platform | Support | Opener |
|----------|---------|--------|
| macOS | Native | `open` |
| Windows | Native | `start` |
| Linux | Native | `xdg-open` |

