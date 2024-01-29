import sys
import os
import re

def main(dir: str):
    assert os.path.isdir(dir)
    for file in  os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith('.ls'):
            path = os.path.join(dir, filename)
            lines = []
            new_lines = []
            with open(path, 'r') as f:
                lines = [line.strip() for line in f.readlines()]
                main_encountered = False
                for i in range(len(lines)):
                    line = lines[i]
                    if main_encountered:
                        line = re.sub(r'\[([\d,]+):.+?\]', r'[\1]', line)
                        line = re.sub(r'\d+?:', r'', line)
                        new_lines.append(line)
                    else:
                        main_encountered = (line == '/MN')

            with open(path, 'w') as f2:
                for line in new_lines:
                    f2.write(line + '\n')

if __name__ == '__main__':
    assert len(sys.argv) == 2
    dir = sys.argv[1]
    main(
        dir=dir
    )
