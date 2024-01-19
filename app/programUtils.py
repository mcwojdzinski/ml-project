import os

def welcome_user():
    print("""\033[1;36m 
          
    
                       _ _                                   _        _ _ 
     /\               | (_)                                 | |      (_|_)
    /  \   _ __   __ _| |_ ______ _    ___ ___ _ __     __ _| | _____ _ _ 
   / /\ \ | '_ \ / _` | | |_  / _` |  / __/ _ \ '_ \   / _` | |/ / __| | |
  / ____ \| | | | (_| | | |/ / (_| | | (_|  __/ | | | | (_| |   < (__| | |
 /_/    \_\_| |_|\__,_|_|_/___\__,_|  \___\___|_| |_|  \__,_|_|\_\___| |_|
                                                                    _/ |  
    \033[0m \033[1;32m
                                                                                                                                                                                                                                                                    
                                                                                                                  
1000                                                                                                             
                                      ███                                          
                                     █  █                                          
800                                 ██   █                                         
                              ███   █    ██                                        
                             ██  ███      █                              ███       
600                          ██            █                             █         
                           ███             █████                        █          
             ██   ██      █                    █                       █           
400       ███ ██ ██ ██ ████                    ██                     ██           
        ███    ██    █ █ █                      █   ██          █     █            
       █             ███                         █ ███         ███    █            
200                                               █   █       █  █████            
                                                      ███    ██                 
                                                         ████                     
0                                                                          
                                                                                                                     
           
          
    \033[0m""")
    print("Wybierz aktywo(a) do analizy:")
    
    datasets_folder = "../datasets"
    available_assets = [file.split('.')[0] for file in os.listdir(datasets_folder) if file.endswith('.csv')]

    for index, asset in enumerate(available_assets, start=1):
        print(f"{index}. {asset}")

    while True:
        try:
            user_input = int(input("\nWypisz indeks aktywa do analizy:\n- ").strip())
            
            selected_asset = available_assets[user_input - 1]


            print(f"\nAnaliza dla: \033[1;32m{selected_asset}\033[0m")

            break

        except (ValueError, IndexError):
            print("\033[1;31mNiepoprawna wartość.\033[0m")

    # Return the selected assets
    return selected_asset


class LibraryChecker:

    def __init__(self):
        self.libraries_with_min_version = self.read_requirements_file()

    def read_requirements_file(self, filename='requirements.txt'):
        libraries_with_min_version = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('==')
                        library_name = parts[0].lower()
                        min_version = parts[1] if len(parts) > 1 else None
                        libraries_with_min_version[library_name] = min_version
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        return libraries_with_min_version

    def check_library(self, library_name, min_version=None):
        try:
            module = __import__(library_name)
            version = getattr(module, '__version__', None)

            if version is not None:
                print(f"{library_name} werji {version}  - jest zainstalowana..")
                if min_version and version < min_version:
                    print(f"Warning: {library_name} wersji {min_version} jest potrzebna do uruchomienia.")
                    return False
                return True
            else:
                print(f"{library_name} - brak informacji o wersji.")
                return True

        except ImportError:
            print(f"{library_name} - nie jest zainstalowana.")
            return False

    def check_all_libraries(self):
        missing_libraries = []

        for lib, min_version in self.libraries_with_min_version.items():
            if not self.check_library(lib, min_version):
                missing_libraries.append(lib)


        if not missing_libraries:
            print("Wszystkie biblioteki zainstalowane.")
            return True
        else:
            print(f"\nBrakuje {len(missing_libraries)} moduł(ów) lub mają nieprawidłowe wersje."
                  f"Zainstaluj je poniższymi komendami:")
            for lib in missing_libraries:
                print(f"pip install --upgrade {lib}")
            return False

