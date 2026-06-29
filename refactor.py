import os
import re
import shutil

dart_files_mapping = {
    'game_page.dart': 'presentation/pages/game_page.dart',
    'loading_page.dart': 'presentation/pages/loading_page.dart',
    'display_pannel.dart': 'presentation/widgets/display_pannel.dart',
    'input_pannel.dart': 'presentation/widgets/input_pannel.dart',
    'instruction_pannel.dart': 'presentation/widgets/instruction_pannel.dart',
    'show_dialogs.dart': 'presentation/widgets/show_dialogs.dart',
    'single_selection.dart': 'presentation/widgets/single_selection.dart',
    'selection_group.dart': 'presentation/widgets/selection_group.dart',
    'group_shared.dart': 'presentation/widgets/group_shared.dart',
    'popper_generator.dart': 'presentation/widgets/popper_generator.dart',
    'generator.dart': 'domain/usecases/generator.dart',
    'validation_provider.dart': 'presentation/providers/validation_provider.dart',
    'event_bus.dart': 'core/utils/event_bus.dart',
    'scroll_behav.dart': 'core/utils/scroll_behav.dart'
}

lib_dir = 'lib'

# create dirs
for f, new_path in dart_files_mapping.items():
    p = os.path.join(lib_dir, new_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)

# collect all lines from all files
files_to_process = list(dart_files_mapping.keys()) + ['main.dart']

for f in files_to_process:
    if os.path.exists(os.path.join(lib_dir, f)):
        print(f"Moving {f}")
        with open(os.path.join(lib_dir, f), 'r', encoding='utf-8') as file:
            content = file.read()
        
        # update imports
        for old_name, new_path in dart_files_mapping.items():
            package_import = f"package:wordle/{old_name}"
            new_package_import = f"package:wordle/{new_path}"
            content = content.replace(package_import, new_package_import)
            
            # relative imports
            relative_import = f"./{old_name}"
            content = content.replace(relative_import, new_package_import)
            
            # just the name inside quotes
            content = re.sub(rf"['\"]{old_name}['\"]", f"'{new_package_import}'", content)
            
        with open(os.path.join(lib_dir, f), 'w', encoding='utf-8') as file:
            file.write(content)
            
        if f != 'main.dart':
            shutil.move(os.path.join(lib_dir, f), os.path.join(lib_dir, dart_files_mapping[f]))

# Clean Architecture demands a Data layer, let's create placeholders
os.makedirs(os.path.join(lib_dir, 'data', 'models'), exist_ok=True)
os.makedirs(os.path.join(lib_dir, 'data', 'repositories'), exist_ok=True)

print('Done reorganizing.')
