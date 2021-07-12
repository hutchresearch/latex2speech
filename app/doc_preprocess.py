from app.logger import logging, writelog

import re
    
def doc_preprocess(file_name):
    with open(file_name, 'r+') as file:
        text = file.read()

        # Remove comments (handled elsewhere but better safe than sorry)
        text = re.sub(r'(^.*?)(?=%.*$)', r'\0', text, flags=re.MULTILINE)

        # Remove \left and \right
        text = re.sub(r'\\left|\\right', '', text)

        # Replace \def with \newcommand
        def def_to_newcommand(match):
            out = r'\newcommand{' + match.group('name') + r'}'
            if match.group('args'):
                max_arg = 1
                for c in match.group('args'):
                    try:
                        arg = int(c)
                        if arg > max_arg:
                            max_arg = arg
                    except ValueError:
                        pass
                out += r'[{}]'.format(max_arg)
            out += match.group('repl')
            return out

        text = re.sub(
            r'\\def[\s]*(?P<name>\\[a-zA-Z]+)[\s]*(?P<args>(\[?#[0-9]\]?)*)[\s]*(?P<repl>\{.*\})',
            def_to_newcommand,
            text
        )

        # Account for white space between arguments
        text = re.sub(r'(?<=\}|\])[\s]+(?=\{|\[)', '', text)

        # Remove double backslash
        text = re.sub(r'\\\\', '', text)

        # Remove backslash canceled whitespace
        text = re.sub(r'\\(?=[\s])', '', text)

        # Replace file contents
        file.truncate(0)
        file.write(text)