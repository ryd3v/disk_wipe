#!/usr/bin/python
import os
import platform
import subprocess


def wipe_disk_windows(disk):
    # Wipe disk on Windows
    subprocess.run(['cipher', '/w:' + disk], check=True)


def wipe_disk_linux(disk, num_passes):
    # Wipe disk on Linux
    for i in range(num_passes):
        subprocess.run(['sudo', 'dc3dd', f'wipe={disk}', 'pat=0x00', f'hash=sha256', f'hlog=pass{i + 1}.log'],
                       check=True)


def main():
    disk = input("Please enter the disk: ")
    os_name = platform.system()

    if os_name == 'Windows':
        # Check that disk exists
        if not os.path.exists(disk):
            print(f"Error: Disk {disk} does not exist.")
            return
        wipe_disk_windows(disk)
    elif os_name == 'Linux':
        try:
            num_passes = int(input("Please enter the number of passes: "))
            if num_passes < 1:
                raise ValueError("Number of passes must be a positive integer.")
        except ValueError as e:
            print(f"Error: Invalid number of passes. {e}")
            return
        # Check that disk exists
        if not os.path.exists(disk):
            print(f"Error: Disk {disk} does not exist.")
            return
        try:
            wipe_disk_linux(disk, num_passes)
        except subprocess.CalledProcessError:
            print(f"Error: Failed to wipe disk {disk}.")
    else:
        print("Unsupported operating system.")


if __name__ == "__main__":
    main()
