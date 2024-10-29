import subprocess
import sys
from typing import Optional, List
import os
import shutil
from google.colab import files 

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
        """Lists currently installed packages in the environment."""
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

    def kaggle_download(self, datasets: Optional[List[str]] = None, output_folder: str = 'data', paths_file: str = 'dataset_paths.txt'):
        """
        Downloads multiple datasets from Kaggle and organizes them.
        ...
        """
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Upload the Kaggle API key
        uploaded = files.upload()
        file_name = list(uploaded.keys())[0]

        # Set up Kaggle API key
        kaggle_dir = '/root/.kaggle'
        os.makedirs(kaggle_dir, exist_ok=True)
        with open(os.path.join(kaggle_dir, 'kaggle.json'), 'wb') as f:
            f.write(uploaded[file_name])
        os.chmod(os.path.join(kaggle_dir, 'kaggle.json'), 0o600)

        # Initialize dataset paths
        dataset_paths = []
        
        # Load existing dataset paths from the paths file
        if os.path.exists(paths_file):
            with open(paths_file, 'r') as f:
                dataset_paths = [line.strip() for line in f.readlines()]

        # If no datasets are provided, load from the dataset_paths.txt
        if datasets is None:
            datasets = []
            if os.path.exists(paths_file):
                with open(paths_file, 'r') as f:
                    datasets = [line.strip() for line in f.readlines()]

            for dataset in datasets:
                    try:
                        # Download dataset
                        print(f"Downloading dataset: {dataset}")
                        subprocess.check_call(['kaggle', 'datasets', 'download', '-d', dataset, '-p', output_folder, '--unzip'])
                        
                        # Find the downloaded files
                        downloaded_files = os.listdir(output_folder)
                        if downloaded_files:
                            first_file_name = downloaded_files[0]  # Get the first downloaded file
                            folder_name = first_file_name[-3:]  # Last 3 digits of the file name
                            designated_folder = os.path.join(output_folder, folder_name)

                            # Create a designated folder
                            os.makedirs(designated_folder, exist_ok=True)

                            # Move downloaded files to the designated folder
                            for file in downloaded_files:
                                shutil.move(os.path.join(output_folder, file), os.path.join(designated_folder, file))
                            
                            # Store the path of the designated folder
                            dataset_paths.append(designated_folder)
                            print(f"Dataset downloaded and moved to: {designated_folder}")

                    except subprocess.CalledProcessError as e:
                        print(f"Error occurred while downloading {dataset}: {e}")

            # Save dataset paths to a file
            with open(paths_file, 'w') as f:
                for path in dataset_paths:
                    f.write(path + '\n')
            print(f"Dataset paths saved to {paths_file}.")
