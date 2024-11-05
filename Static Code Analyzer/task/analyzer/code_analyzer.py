import sys
import re
from soupsieve.util import lower
import os
from ASTAnalyzer import analyze_file


class Code_Analyzer():

    def __init__(self):
        self.arg = None
        self.file = None
        self.path = None
        self.line_list = []

    def read_input(self):
        self.arg = sys.argv

    def iterateover_files(self):
        if os.path.isfile(self.arg[1]):
            self.path = self.arg[1]
            self.open_file()
        else:
            for dirpath, dirnames, filenames in os.walk(self.arg[1]):
                for filename in filenames:
                    if filename.endswith(".py"):
                        self.path = os.path.join(dirpath, filename)
                        self.open_file()

    def open_file(self):
        self.file = open(f'{self.path}', 'r')
        self.line_number = 0
        analyze_file(self.path)

        for line in self.file:
            self.line = line
            self.line_number += 1
            self.line_list.append(self.line.rstrip())
            self.analyze()
        self.line_list = []
        self.file.close()
        self.line_number = 1

    def analyze(self):
        self.S0001()
        self.S0002()
        self.S0003()
        self.S0004()
        self.S0005()
        self.S0006()
        self.S0007()
        self.S0008()
        self.S0009()

    def S0001(self):
        if len(self.line) > 79:
            print(f'{self.path}: Line {self.line_number}: S001 Too long')

    def S0002(self):
        line_with_spaces = self.line.replace('\t', ' ' * 4)
        number_of_spaces = len(line_with_spaces) - len(line_with_spaces.lstrip(' '))

        if number_of_spaces % 4 != 0:
            print(f'{self.path}: Line {self.line_number}: S002 Indentation is not a multiple of four')

    def S0003(self):
        trimmed_line = self.line.rstrip()
        if trimmed_line:
            code_part = trimmed_line.split('#', 1)[0].rstrip()  # Część przed komentarzem
            if code_part:
                if code_part.endswith(';'):
                    print(f'{self.path}: Line {self.line_number}: S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)')

    def S0004(self):
        trimmed_line = self.line
        comment_index = trimmed_line.find('#')
        if comment_index !=1:
            if comment_index > 2:
                if trimmed_line[comment_index -1] != ' ' or trimmed_line[comment_index -2] != ' ':
                    print(f'{self.path}: Line {self.line_number}: S004 Less than two spaces before inline comments'
                          f'{trimmed_line[comment_index -1]}{trimmed_line[comment_index -2]}')

    def S0005(self):
        trimmed_line = self.line.rstrip()
        if trimmed_line:
            code_part = trimmed_line.split('#')
            try:
                if 'todo' in lower(code_part[1]):
                    print(f'{self.path}: Line {self.line_number}: S005 TUUUDUUU')
            except IndexError:
                pass

    def S0006(self):
        if len(self.line_list) > 3:
            if self.line_list[self.line_number-1] !='':
                if self.line_list[self.line_number-2] == '' and self.line_list[self.line_number-3] == ''and self.line_list[self.line_number-4] == '':
                    print(f'{self.path}: Line {self.line_number}: S006 More than two blank lines preceding a code line (applies to the first non-empty line)'
                          f'{self.line_list[self.line_number-1]}{self.line_list[self.line_number-2]}{self.line_list[self.line_number-3]}')
    def S0007(self):
        trimmed_line = self.line.lstrip()
        if lower(trimmed_line).startswith('def'):
            regexp =r'def [aA-zZ][a-zA-Z0-9]*'
            match_def = re.match(regexp, trimmed_line)
            if match_def is None:
                print(f'{self.path}: Line {self.line_number}: S007 Too many spaces after construction_name (def)')

        if lower(trimmed_line).startswith('class'):
            regexp =r'class [aA-zZ][a-zA-Z0-9]*'
            match_class = re.match(regexp, trimmed_line)
            if match_class is None:
                print(f'{self.path}: Line {self.line_number}: S007 Too many spaces after construction_name (class)')

    def S0008(self):
        trimmed_line = self.line.lstrip()
        if lower(trimmed_line).startswith('class'):
            regexp = r'class +[A-Z][a-zA-Z0-9]*'
            match_camel_case = re.match(regexp, trimmed_line)
            if match_camel_case is None:
                print(f'{self.path}: Line {self.line_number}: S008 Class name class_name should be written in CamelCase')

    def S0009(self):
        trimmed_line = self.line.lstrip()
        if trimmed_line.lower().startswith('def'):
            regexp_multi_word = r'def +([a-z_][a-z0-9_]*)\s*\(.*\):'
            regexp_single_word = r'^[a-z]+(_[a-z]+)*$'
            regexp_magic_def = r'def _{2}\w+_{2}\s*\(\):'
            match_snake_case_multi = re.match(regexp_multi_word, trimmed_line)
            match_snake_case_single = re.match(regexp_single_word, trimmed_line)
            match_magic_def = re.match(regexp_magic_def, trimmed_line)

            if match_snake_case_multi is None and match_snake_case_single is None and match_magic_def is None:
                    print(f'{self.path}: Line {self.line_number}: S009 Function name should be written in snake_case.')


if __name__ == "__main__":
    analyzer = Code_Analyzer()
    analyzer.read_input()
    analyzer.iterateover_files()

