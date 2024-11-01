Scripts Folder:

This folder contains automation scripts to streamline project setup and management.

Contents:

auto_runner.sh: Automates the startup sequence for specific applications and services.
auto_sleeper.sh: Handles scheduled shutdown or sleep operations for your environment.
Usage

Setup: Make sure to grant execute permissions with chmod +x script_name.sh.
Run Scripts: Execute scripts from the command line:
bash
Copy code
./auto_runner.sh
./auto_sleeper.sh
Requirements:
Ensure dependencies (if any) are installed and paths are configured correctly.
To run on startup with Mac, cronetab the script to run at whatever time you want the weather/events for
You will also need to pmset a wakeup right before the script time run, and execute a sleeping script after
I included my scripts in the repo
