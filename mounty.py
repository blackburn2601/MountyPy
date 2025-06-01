import os
import subprocess
import sys
import platform

def get_mount_directory(variable):
    """Get platform-independent mount directory path."""
    if platform.system() == "Windows":
        # Use a more appropriate location for Windows
        base_dir = os.path.join(os.path.expanduser("~"), "Documents", "mounts")
    else:
        # Unix-like systems (macOS, Linux)
        base_dir = os.path.join(os.path.expanduser("~"), "Documents", "mounts")
    
    return os.path.join(base_dir, variable)

def mount_sshfs(variable):
    mount_dir = get_mount_directory(variable)
    os.makedirs(mount_dir, exist_ok=True)
    
    # Check platform and adjust command accordingly
    system = platform.system()
    
    if system == "Windows":
        # On Windows, we need sshfs-win or similar tool
        # This assumes sshfs-win is installed and available in PATH
        sshfs_command = [
            "sshfs",
            "-o", "noatime,reconnect,ServerAliveInterval=20,ServerAliveCountMax=3,cache_timeout=1200,entry_timeout=1200,attr_timeout=1200,negative_timeout=1200",
            f"nintendo_admin@login.dev.actindo.com:/home/nintendo_admin/sandboxes/{variable}",
            mount_dir
        ]
        shell = False
        executable = None
    else:
        # Unix-like systems (macOS, Linux)
        sshfs_command = [
            "sshfs",
            "-o", "noatime,reconnect,ServerAliveInterval=20,ServerAliveCountMax=3,cache_timeout=1200,entry_timeout=1200,attr_timeout=1200,negative_timeout=1200",
            f"nintendo_admin@login.dev.actindo.com:/home/nintendo_admin/sandboxes/{variable}",
            mount_dir
        ]
        shell = False
        executable = None

    try:
        print(f"Mounting directory: {variable}")
        print(f"Mount path: {mount_dir}")
        subprocess.run(sshfs_command, check=True, shell=shell, executable=executable)
        print(f"Directory successfully mounted at: {mount_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Make sure sshfs is installed on your system.")
        if system == "Windows":
            print("On Windows, install sshfs-win or WinFsp + SSHFS-Win")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: sshfs command not found.")
        if system == "Windows":
            print("On Windows, install sshfs-win or WinFsp + SSHFS-Win")
        else:
            print("On Unix systems, install sshfs package")
        sys.exit(1)

def unmount_sshfs(variable):
    mount_dir = get_mount_directory(variable)
    system = platform.system()
    
    # Determine the correct unmount command based on the platform
    if system == "Windows":
        # On Windows with sshfs-win
        unmount_command = ["sshfs", "-u", mount_dir]
    elif system == "Darwin":  # macOS
        unmount_command = ["umount", mount_dir]
    elif system == "Linux":
        # Try fusermount first (more reliable for FUSE mounts), fallback to umount
        try:
            subprocess.run(["fusermount", "-u", mount_dir], check=True)
            print(f"Directory successfully unmounted: {mount_dir}")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to regular umount
            unmount_command = ["umount", mount_dir]
    else:
        print(f"Unmounting is not supported on {system}.")
        sys.exit(1)

    try:
        print(f"Unmounting directory: {variable}")
        subprocess.run(unmount_command, check=True)
        print(f"Directory successfully unmounted: {mount_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error unmounting directory: {e}")
        if system == "Linux":
            print("Trying alternative unmount method...")
            try:
                subprocess.run(["fusermount", "-u", mount_dir], check=True)
                print(f"Directory successfully unmounted: {mount_dir}")
            except subprocess.CalledProcessError:
                print("Both umount and fusermount failed.")
                sys.exit(1)
        else:
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ["mount", "unmount"]:
        print("Usage:")
        print(f"  python3 {os.path.basename(__file__)} mount <VARIABLE>")
        print(f"  python3 {os.path.basename(__file__)} unmount <VARIABLE>")
        print("\nSupported platforms: Windows, macOS, Linux")
        print("Note: Requires sshfs to be installed:")
        print("  - Windows: Install sshfs-win or WinFsp + SSHFS-Win")
        print("  - macOS: Install via Homebrew: brew install sshfs")
        print("  - Linux: Install via package manager: apt install sshfs")
        sys.exit(1)
    
    command = sys.argv[1]
    variable = sys.argv[2]
    
    print(f"Platform: {platform.system()}")
    
    if command == "mount":
        mount_sshfs(variable)
    elif command == "unmount":
        unmount_sshfs(variable)
