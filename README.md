# MountyPy

A cross-platform Python tool for mounting remote SSH filesystems using SSHFS. Easily mount and unmount remote directories from `login.dev.actindo.com` to your local machine.

## Features

- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Automatic directory creation
- ✅ Platform-specific mount locations
- ✅ Robust error handling
- ✅ Easy mount/unmount operations
- ✅ Optimized SSHFS options for better performance

## Requirements

### Linux
```bash
# Ubuntu/Debian
sudo apt install sshfs

# Fedora/CentOS/RHEL
sudo dnf install fuse-sshfs
# or
sudo yum install fuse-sshfs

# Arch Linux
sudo pacman -S sshfs
```

### macOS
```bash
# Using Homebrew
brew install sshfs

# Using MacPorts
sudo port install sshfs
```

### Windows
Install one of the following:
- **sshfs-win**: Download from [GitHub releases](https://github.com/winfsp/sshfs-win/releases)
- **WinFsp + SSHFS-Win**: 
  1. Install [WinFsp](https://winfsp.dev/rel/)
  2. Install [SSHFS-Win](https://github.com/winfsp/sshfs-win/releases)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/MountyPy.git
cd MountyPy
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x mounty.py
```

## Usage

### Mount a remote directory
```bash
python3 mounty.py mount <SANDBOX_NAME>
```

### Unmount a directory
```bash
python3 mounty.py unmount <SANDBOX_NAME>
```

### Examples
```bash
# Mount a sandbox called "my-project"
python3 mounty.py mount my-project

# Unmount the same sandbox
python3 mounty.py unmount my-project
```

## Mount Locations

The tool creates mount points in different locations depending on your operating system:

| Platform | Mount Location |
|----------|----------------|
| **Linux** | `~/mounts/<SANDBOX_NAME>` |
| **macOS** | `~/Documents/mounts/<SANDBOX_NAME>` |
| **Windows** | `~/Documents/mounts/<SANDBOX_NAME>` |

## SSHFS Options

The tool uses optimized SSHFS options for better performance and reliability:

- `noatime` - Don't update access times
- `reconnect` - Automatically reconnect on connection drops
- `ServerAliveInterval=20` - Send keepalive packets every 20 seconds
- `ServerAliveCountMax=3` - Maximum failed keepalive attempts
- `cache_timeout=1200` - Cache timeout (20 minutes)
- `entry_timeout=1200` - Directory entry cache timeout
- `attr_timeout=1200` - File attribute cache timeout
- `negative_timeout=1200` - Negative lookup cache timeout

## Troubleshooting

### Connection Issues
- Ensure you have SSH access to `login.dev.actindo.com`
- Check if your SSH key is properly configured
- Verify the sandbox name exists on the remote server

### Permission Issues (Linux/macOS)
```bash
# Add user to fuse group (may require logout/login)
sudo usermod -a -G fuse $USER
```

### Mount Already Exists
If you get "mount point already in use" errors:
```bash
# Unmount first, then try mounting again
python3 mounty.py unmount <SANDBOX_NAME>
python3 mounty.py mount <SANDBOX_NAME>
```

### Windows-Specific Issues
- Ensure WinFsp service is running
- Run Command Prompt as Administrator if needed
- Check Windows Defender/Antivirus settings

## Platform Detection

The tool automatically detects your platform and adjusts behavior accordingly:

```bash
python3 mounty.py mount test-sandbox
# Output: Platform: Linux
# Output: Mounting directory: test-sandbox
# Output: Mount path: /home/username/mounts/test-sandbox
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms if possible
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notes

- This tool connects to `nintendo_admin@login.dev.actindo.com`
- Ensure your SSH keys are properly secured
- Use SSH agent for key management
- Consider using SSH config for connection settings

## Support

For issues and questions:
1. Check the [Issues](https://github.com/yourusername/MountyPy/issues) page
2. Create a new issue with platform and error details
3. Include relevant log output 
