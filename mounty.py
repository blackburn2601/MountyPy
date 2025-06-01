import os
import subprocess
import sys

def mount_sshfs(variable):
    sshfs_command = (
        f"sshfs -o noatime,reconnect,ServerAliveInterval=20,ServerAliveCountMax=3,"
        f"cache_timeout=1200,entry_timeout=1200,attr_timeout=1200,negative_timeout=1200 "
        f"nintendo_admin@login.dev.actindo.com:/home/nintendo_admin/sandboxes/{variable} "
        f"~/Documents/mounts/{variable}"
    )
    
    mount_dir = os.path.expanduser(f"~/Documents/mounts/{variable}")
    os.makedirs(mount_dir, exist_ok=True)

    try:
        print(f"Mounting directory: {variable}")
        subprocess.run(sshfs_command, shell=True, check=True, executable="/bin/bash")
        print(f"Directory successfully mounted at: ~/Documents/mounts/{variable}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing a command: {e}")
        sys.exit(1)

def unmount_sshfs(variable):
    mount_dir = os.path.expanduser(f"~/Documents/mounts/{variable}")
    # Determine the correct unmount command based on the platform
    if os.name == "posix":
        unmount_command = f"umount {mount_dir}"  # Works for macOS and most Unix systems
    else:
        print("Unmounting is not supported on this OS.")
        sys.exit(1)

    try:
        print(f"Unmounting directory: {variable}")
        subprocess.run(unmount_command, shell=True, check=True, executable="/bin/bash")
        print(f"Directory successfully unmounted: {mount_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error unmounting directory: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ["mount", "unmount"]:
        print("Usage:")
        print("  python3 mountinator.py mount <VARIABLE>")
        print("  python3 mountinator.py unmount <VARIABLE>")
        sys.exit(1)
    
    command = sys.argv[1]
    variable = sys.argv[2]
    
    if command == "mount":
        mount_sshfs(variable)
    elif command == "unmount":
        unmount_sshfs(variable)
