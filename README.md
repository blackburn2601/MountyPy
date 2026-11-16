<div align="center">

# MountyPy

**Mount and unmount remote project folders over SSH with one command.** A small cross-platform Python wrapper
around SSHFS: you give it a sandbox name, it works out the remote path and a sensible local mount point.

![Python](https://img.shields.io/badge/Python-3-3776ab)
![Platforms](https://img.shields.io/badge/Linux%20·%20macOS%20·%20Windows-supported-555)
![Dependencies](https://img.shields.io/badge/dependencies-stdlib%20only-brightgreen)
![SSHFS](https://img.shields.io/badge/SSHFS-FUSE-orange)

</div>

---

## About

Working on files that live on a remote development server is easier when they simply appear as a local folder.
SSHFS does that, but its command line is long, and the mount options that make it usable over a flaky connection
are easy to forget. MountyPy keeps them in one place:

```console
$ python3 mounty.py mount my-project      # remote: <user>@<host>:<sandbox_path>/my-project
$ python3 mounty.py unmount my-project
```

One host, one base path and the sandbox names under it, all configured once in a JSON file. It is a single script
with no third-party dependencies, only the standard library and the `sshfs` tool.

## How it works

```
mounty.py mount my-project
   │
   ├─ read config.json            host, user, sandbox_path
   ├─ local mount point           Linux: ~/mounts/my-project
   │                              macOS / Windows: ~/Documents/mounts/my-project
   ├─ create the directory if missing
   └─ sshfs -o <options> user@host:/path/to/sandboxes/my-project <mount point>
```

`unmount` removes the mount again: `fusermount -u` on Linux (falling back to `umount`), `umount` on macOS and
`sshfs -u` on Windows.

The mount options are chosen for a long-lived development connection:

| Option | Effect |
|---|---|
| `reconnect` | reconnect automatically after a dropped connection |
| `ServerAliveInterval=20`, `ServerAliveCountMax=3` | detect a dead connection after about a minute instead of hanging |
| `noatime` | do not write access times back to the server |
| `cache_timeout`, `entry_timeout`, `attr_timeout`, `negative_timeout` = `1200` | cache listings and attributes for 20 minutes, which makes browsing a large tree fast |

## Quick start

```bash
git clone git@github.com:blackburn2601/MountyPy.git && cd MountyPy

cp config.example.json config.json     # then edit it
```

```json
{
    "endpoint": {
        "host": "your.ssh.host",
        "user": "your_username",
        "sandbox_path": "/path/to/sandboxes"
    }
}
```

`config.json` is listed in `.gitignore`, so your host and user name stay out of the repository.

```bash
python3 mounty.py mount my-project
python3 mounty.py unmount my-project
```

SSH authentication is whatever your `ssh` setup already does (keys, agent, `~/.ssh/config`); MountyPy does not
handle credentials itself.

## Requirements

Python 3 and `sshfs`:

| Platform | Install |
|---|---|
| Debian / Ubuntu | `sudo apt install sshfs` |
| Fedora / RHEL | `sudo dnf install fuse-sshfs` |
| Arch | `sudo pacman -S sshfs` |
| macOS | `brew install sshfs` (needs macFUSE) |
| Windows | [WinFsp](https://winfsp.dev/rel/) and [SSHFS-Win](https://github.com/winfsp/sshfs-win/releases) |

## Usage and output

```console
$ python3 mounty.py --help
MountyPy - A tool for mounting remote SSHFS directories

Usage:
  python3 mounty.py [--help]
  python3 mounty.py mount <VARIABLE>
  python3 mounty.py unmount <VARIABLE>
  ...
```

These are real outputs of the error paths, run on Linux without `sshfs` installed:

```console
$ python3 mounty.py foo
Error: Invalid arguments
Use 'python3 mounty.py --help' for usage information

$ python3 mounty.py mount demo          # no config.json yet
Platform: Linux
Error: config.json not found. Please ensure it exists in the same directory as the script.

$ python3 mounty.py mount demo          # config present, sshfs missing
Platform: Linux
Mounting directory: demo
Mount path: /home/<user>/mounts/demo
Error: sshfs command not found.
On Unix systems, install sshfs package
```

## Troubleshooting

| Problem | What to check |
|---|---|
| Connection refused / permission denied | `ssh user@host` works without MountyPy; the sandbox exists under `sandbox_path` |
| `fusermount: failed to open /dev/fuse` | add yourself to the `fuse` group (`sudo usermod -aG fuse $USER`, then log in again) |
| "Mount point already in use" | `python3 mounty.py unmount <name>`, then mount again |
| Windows: nothing happens | the WinFsp service must be running; try an elevated prompt |

## Tech stack

| | |
|---|---|
| Language | Python 3, standard library only (`subprocess`, `platform`, `json`, `os`) |
| Mounting | SSHFS over FUSE (WinFsp on Windows) |
| Config | one JSON file next to the script |

## Project layout

```
mounty.py             the whole tool: config, mount point logic, mount / unmount
config.example.json   template for config.json (which is gitignored)
```

## Limitations

I read through the code and ran the error paths above. I could not run a real mount (the machine used for this
review has no `sshfs` or SSH server), so the mount and unmount commands themselves, in particular on macOS and Windows,
are untested here. Known weaknesses:

- **The sandbox name is not validated.** A name such as `../../x` leaves `~/mounts` locally and changes the remote
  path. Use it only with names you trust.
- **An empty mount directory is left behind** when `sshfs` is missing or fails, because the directory is created
  before the command runs.
- **One host only.** There is a single endpoint in the config.
- **The Windows unmount** calls `sshfs -u`; I could not confirm that SSHFS-Win supports this, so treat it as unverified.
- No tests.

## License

MIT, as stated by the author. The repository does not contain a `LICENSE` file yet.
