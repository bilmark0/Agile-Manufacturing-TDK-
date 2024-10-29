import subprocess
import sys
from typing import Optional
import zipfile
import os

class DependencyManager:
    def __init__(self, requirements_file: str = 'requirements.txt'):
        """
        Initializes the DependencyManager with the path to the requirements file.

        Parameters:
        - requirements_file (str): Path to the requirements file (default is 'requirements.txt').
        """
        self.requirements_file = requirements_file

    def install_dependencies(self, upgrade: bool = False) -> None:
        """
        Installs dependencies from the requirements file.

        Parameters:
        - upgrade (bool): If True, upgrades all packages to the latest versions.

        Returns:
        - None
        """
        try:
            command = [sys.executable, '-m', 'pip', 'install', '-r', self.requirements_file]
            if upgrade:
                command.append('--upgrade')
            subprocess.check_call(command)
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")

    def list_installed_packages(self) -> None:
        """
        Lists currently installed packages in the environment.

        Returns:
        - None
        """
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'list'])
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while listing packages: {e}")

    def freeze_environment(self, output_file: Optional[str] = 'requirements_freeze.txt') -> None:
        """
        Generates a freeze file with all installed packages and their versions.

        Parameters:
        - output_file (Optional[str]): The file to save the freeze output (default is 'requirements_freeze.txt').

        Returns:
        - None
        """
        try:
            with open(output_file, 'w') as f:
                subprocess.check_call([sys.executable, '-m', 'pip', 'freeze'], stdout=f)
            print(f"Environment frozen successfully to {output_file}.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while freezing environment: {e}")
    
    def kaggle_download(self):
        # Upload the file
        uploaded = files.upload()

        # Get the actual file name from the dictionary
        file_name = list(uploaded.keys())[0]
        !mkdir ~/.kaggle
        !cp kaggle.json ~/.kaggle/
        !chmod 600 ~/.kaggle/kaggle.json

        # Save the API key securely without displaying it
        with open('/root/.kaggle/kaggle.json', 'wb') as f:
            f.write(uploaded[file_name])

        # Set permissions
        !chmod 600 /root/.kaggle/kaggle.json
        
        #download data
        !kaggle competitions download -c isic-2024-challenge
        # Path to your zip file and extract location
        zip_file_path = 'isic-2024-challenge.zip'
        extract_to_path = 'data'

        # Extracting the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
            print("Extraction completed.")





