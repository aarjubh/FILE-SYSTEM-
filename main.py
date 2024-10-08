import os
import io
import shutil
from collections import OrderedDict
from datetime import datetime

class FileSystem:
    def __init__(self, name_or_root_path, is_directory=False):
        if is_directory:
            self.name = name_or_root_path
            self.is_directory = is_directory
            self.timestamp = datetime.now()
            self.size = 0
            self.permissions = "rw-r--r--"  # Default permissions
        else:
            self.current_directory = name_or_root_path
            self.root_directory = name_or_root_path
            self.metadata = {}
            self.permissions = {}  # Dictionary to store permissions
            if not os.path.exists(self.current_directory):
                os.makedirs(self.current_directory)

    def list_all(self):
        print(f"Detailed contents of directory '{self.current_directory}':")
        contents = os.listdir(self.current_directory)
        for item in contents:
            item_path = os.path.join(self.current_directory, item)
            item_type = "Directory" if os.path.isdir(item_path) else "File"
            metadata = self.get_metadata(item)
            if metadata:
                print(f"{item_type}: {item}\n{metadata}\n")
            else:
                print(f"{item_type}: {item}\n")

    def get_permissions(self, item):
            item_path = os.path.join(self.current_directory, item)
            if os.path.exists(item_path):
                permissions = os.stat(item_path).st_mode & 0o777
                return oct(permissions)[-3:]
            return None

    '''def set_permissions(self, item, permissions):
        item_path = os.path.join(self.current_directory, item)
        if os.path.exists(item_path):
            try:
                permissions = int(permissions, 8)
                if 0 <= permissions <= 0o777:
                    os.chmod(item_path, permissions)
                    print(f"Permissions for '{item}' set to '{permissions:o}'.")
                else:
                    print("Invalid permissions value. Use octal notation (0-777).")
            except ValueError:
                print("Invalid permissions value. Use octal notation (0-777).")
        else:
            print(f"'{item}' does not exist.")'''
    def set_permissions(self, item, permissions):
        permissions = permissions[2:]  # Strip the initial '0o'
        octal_permissions = int(permissions, 8)
        if 0 <= octal_permissions <= 0o777:
            os.chmod(os.path.join(self.current_directory, item), octal_permissions)
            print(f"Permissions for '{item}' set to '{octal_permissions:o}'.")
        else:
            print("Invalid permissions value. Use octal notation (0-777).")

    def get_metadata(self, item):
        item_path = os.path.join(self.current_directory, item)
        if os.path.exists(item_path):
            item_stat = os.stat(item_path)
            metadata = {
                "Name": item,
                "Type": "Directory" if os.path.isdir(item_path) else "File",
                "Timestamp": datetime.fromtimestamp(item_stat.st_mtime),
                "Size": f"{item_stat.st_size} B",
                "Permissions": self.get_permissions(item) or "N/A",
            }
            return "\n".join([f"{key}: {value}" for key, value in metadata.items()])
        return None
        
    def print_working_directory(self):
        print(f"Current working directory: {self.current_directory}")

    def list_directory_contents(self):
        print(f"Contents of directory '{self.current_directory}':")
        contents = os.listdir(self.current_directory)
        for item in contents:
            item_path = os.path.join(self.current_directory, item)
            if os.path.isfile(item_path):
                print(f"File: {item}")
            elif os.path.isdir(item_path):
                print(f"Directory: {item}")

    def create_file(self, filename, content=""):
        
        file_path = os.path.join(self.current_directory, filename)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"File '{filename}' created.")
        # To upate the meta-data dictionary for new files
        self.metadata[filename] = FileSystem(filename)

    def create_directory(self, directory):
        new_directory = os.path.join(self.current_directory, directory)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
            print(f"Directory '{directory}' created.")
            # To upate the meta-data dictionary for new directories
            self.metadata[directory] = FileSystem(directory)
        else:
            print(f"Directory '{directory}' already exists.")

    def remove_file(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File '{filename}' removed.")
        else:
            print(f"File '{filename}' does not exist.")

    def remove_directory(self, directory):
        directory_path = os.path.join(self.current_directory, directory)
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)
            print(f"Directory '{directory}' removed.")
        else:
            print(f"Directory '{directory}' does not exist.")

    def rename(self, old_name, new_name):
        old_path = os.path.join(self.current_directory, old_name)
        new_path = os.path.join(self.current_directory, new_name)
        
        if os.path.exists(new_path):
            print(f"'{new_name}' already exists. Rename operation failed.")
        elif os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"'{old_name}' renamed to '{new_name}'.")
        else:
            print(f"'{old_name}' does not exist.")

    
    def cat(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read()
                print(content)
        else:
            print(f"File '{filename}' does not exist.")

    def echo(self, text, filename):
        file_path = os.path.join(self.current_directory, filename)
        with open(file_path, "w") as file:
            file.write(text)
        print(f"Text written to '{filename}'.")

    def nano(self, filename):
        file_path = os.path.join(self.current_directory, filename)

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_content = file.read()

            print("Existing content:\n", existing_content)

            print("Do you want to (a)ppend or (o)verwrite the content?")
            choice = input().lower()

            if choice == "a":
                print("Enter new content (type 'exit' on a new line to save and exit):")
                new_content = []
                while True:
                    line = input()
                    if line.strip().lower() == "exit":
                        break
                    new_content.append(line)

                with open(file_path, "a") as file:
                    file.write("\n" + "\n".join(new_content))

                print("Content appended to file.")
            elif choice == "o":
                print("Enter new content (type 'exit' on a new line to save and exit):")
                new_content = []
                while True:
                    line = input()
                    if line.strip().lower() == "exit":
                        break
                    new_content.append(line)

                with open(file_path, "w") as file:
                    file.write("\n".join(new_content))

                print("Content overwritten in file.")
            else:
                print("Invalid choice. Use 'a' to append or 'o' to overwrite.")
        else:
            print(f"File '{filename}' does not exist.")

    def copy(self, source, destination):  
            source_path = os.path.join(self.current_directory, source)
            destination_path = os.path.abspath(destination)  # Get the full path of the destination

            if os.path.exists(source_path):
                if os.path.isfile(source_path):
                    if os.path.isdir(os.path.dirname(destination_path)):
                        shutil.copy2(source_path, destination_path)
                        print(f"'{source}' copied to '{destination}'.")
                    else:
                        print(f"The destination directory '{os.path.dirname(destination_path)}' does not exist.")
                elif os.path.isdir(source_path):
                    if os.path.isdir(os.path.dirname(destination_path)):
                        destination_dir = os.path.join(destination_path, os.path.basename(source_path))
                        if not os.path.exists(destination_dir):
                            shutil.copytree(source_path, destination_dir)
                            print(f"Directory '{source}' copied to '{destination}'.")
                        else:
                            # Destination directory exists, copy contents to it
                            for item in os.listdir(source_path):
                                item_source = os.path.join(source_path, item)
                                item_destination = os.path.join(destination_dir, item)
                                if os.path.isfile(item_source):
                                    shutil.copy2(item_source, item_destination)
                                elif os.path.isdir(item_source):
                                    shutil.copytree(item_source, item_destination)
                            print(f"Directory contents of '{source}' copied to '{destination}'.")
                    else:
                        print(f"The destination directory '{os.path.dirname(destination_path)}' does not exist.")
            else:
                print(f"'{source}' does not exist.")
    def move(self, source, destination):
            source_path = os.path.join(self.current_directory, source)
            destination_path = os.path.abspath(destination)  # Get the full path of the destination

            if os.path.exists(source_path):
                if os.path.isdir(source_path):
                    if os.path.isdir(destination_path):
                        destination_path = os.path.join(destination_path, os.path.basename(source_path))
                    shutil.move(source_path, destination_path)
                    print(f"'{source}' moved to '{destination}'.")
                else:
                    # Check if the destination is a directory, if so, append the filename of the source
                    if os.path.isdir(destination_path):
                        destination_path = os.path.join(destination_path, os.path.basename(source_path))
                    shutil.move(source_path, destination_path)
                    print(f"'{source}' moved to '{destination}'.")
            else:
                print(f"'{source}' does not exist.")

    def change_directory(self, directory):
        if directory == "..":
            # Move up to the parent directory
            self.current_directory = os.path.dirname(self.current_directory)
        else:
            new_directory = os.path.join(self.current_directory, directory)
            if os.path.isdir(new_directory) and directory in os.listdir(self.current_directory):
                self.current_directory = new_directory
            else:
                print(f"Directory '{directory}' does not exist.")
'''# path
root_path = "C:/Users/DELL/Desktop/FILESYSTEM/root"

if not os.path.exists(root_path):
    os.makedirs(root_path)

file_system = FileSystem(root_path)'''

# To Prompt Users for root path
root_path = input("Enter the root path for the file system: ")

if not os.path.exists(root_path):
    os.makedirs(root_path)

file_system = FileSystem(root_path)

command = input("Enter a command: ")
while command != "exit":
    if command == "pwd":
        file_system.print_working_directory()
    elif command == "ls":
        file_system.list_directory_contents()
    elif command.startswith("create "):
        _, filename = command.split(" ", 1)
        file_system.create_file(filename)
    elif command.startswith("rm "):
        _, filename = command.split(" ", 1)
        file_system.remove_file(filename)
    elif command.startswith("cd "):
        _, directory = command.split(" ", 1)
        file_system.change_directory(directory)
    elif command.startswith("mkdir "):
        _, directory = command.split(" ", 1)
        file_system.create_directory(directory)
    elif command.startswith("rmdir "):
        _, directory = command.split(" ", 1)
        file_system.remove_directory(directory)
    elif command.startswith("rename "):
        _, old_name, new_name = command.split(" ", 2)
        file_system.rename(old_name, new_name)
    elif command.startswith("move "):
        _, source, destination = command.split(" ", 2)
        file_system.move(source, destination)
    elif command.startswith("copy "):
        _, source, destination = command.split(" ", 2)
        file_system.copy(source, destination)
    elif command.startswith("cat "):
        _, filename = command.split(" ", 1)
        file_system.cat(filename)
    elif command == "ls -l":
        file_system.list_all()
    else:
        print("Invalid command.")

    command = input("Enter a command: ")

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 