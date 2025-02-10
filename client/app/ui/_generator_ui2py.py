import os
import re

def generate_all_ui2py(path: str):
    ui_path = str(f"{path}/forms")
    files = os.listdir(ui_path)
    ui_list = []
    pattern = re.compile(r'.*\.ui')

    for item in files:
        if pattern.match(item):
            ui_list.append(item)

    for item in ui_list:
        file_path = os.path.join(ui_path, item)
        file_name_without_extension = file_path.split(os.sep)[-1].removesuffix('.ui')
        cmd = f'pyuic6 {file_path} -o {path}{os.sep}{file_name_without_extension}.py'
        os.popen(cmd)
        print(f'{file_name_without_extension}.ui to .py completed')

if __name__ == '__main__':
    generate_all_ui2py(os.path.dirname(os.path.abspath(__file__)))