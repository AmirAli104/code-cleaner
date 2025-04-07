import re, argparse, os

parser = argparse.ArgumentParser(prog='code-cleaner')
parser.add_argument('-n','--line',help='files to clear line numbers',nargs='+')
parser.add_argument('-s','--shell',help='file to clear shell prompts',nargs='+')
parser.add_argument('-d','--directory',help="Consider the values given to '--shell' and '--line' as directories. You must give the" \
                    " file extentions you want to clean them to this argument. Its default is '.py' files.",nargs='*')
parser.add_argument('-t','--tree',action='store_true',help="If the both '--directory' and '--tree' are enabled it searches" \
                    " all subdirectories to find files")
parser.add_argument('-l','--log',action='store_true',help='enable logging')
args = parser.parse_args()

possible_exceptions = (FileNotFoundError,PermissionError)
current_process = None
LINE_NUMBER_PATTERN = (re.compile(r'^[^\S\r\n]*\d+(?=.)*',re.MULTILINE),)
SHELL_PATTERNS = (re.compile(r'^[^\S\r\n]*>>> ?(?=.)*',re.MULTILINE), re.compile(r'^[^\S\r\n]*\.\.\. ?(?=.)*',re.MULTILINE))

def logger(cleaner_func):

    def wrapper(file_path,pattern):
        print(f'{current_process} {file_path} ... ',end='')
        try:
            cleaner_func(file_path,pattern)
        except possible_exceptions as err:
            print(err)
        else:
            print('Done.')

    return wrapper

def cleaner(file_path, patterns):
        with open(file_path) as f:
            content = f.read()

        for pattern in patterns:
            content = pattern.sub('',content)

        with open(file_path, 'w') as f:
            f.write(content)

def send_multiple_files_to_cleaner(file_paths,patterns):

    for file_path in file_paths:
        try:
            cleaner(file_path,patterns)

        except possible_exceptions as err:
            print(err)
    

def run_the_cleaners(cleaner_func):
    global current_process

    if args.line:
        current_process = 'Cleaning line numbers on'
        cleaner_func(args.line,LINE_NUMBER_PATTERN)

    if args.shell:
        current_process = 'Cleaning shell prompts on'
        cleaner_func(args.shell,SHELL_PATTERNS)

def verify_file_and_clean_file(file_path,target_file_extentions,patterns):
    try:
        if os.path.splitext(file_path)[1] in target_file_extentions and os.path.isfile(file_path):
            cleaner(file_path,patterns)
    except possible_exceptions as err:
        print(err)

def directory_mode(directories_list,patterns):
        
        if args.directory == []:
            target_file_extentions = ['.py']
        else:
            target_file_extentions = args.directory

        if args.tree:
            for directory in directories_list:
                try:
                    if not os.path.isdir(directory):
                        raise FileNotFoundError(f'The system cannot find the path specified {directory!r}')
                    for path in os.walk(directory):
                        for file_name in path[2]:
                            file_path = os.path.join(path[0],file_name)
                            verify_file_and_clean_file(file_path,target_file_extentions,patterns)
                except possible_exceptions as err:
                    print(err)

        else:
            for directory in directories_list:
                try:
                    for file_name in os.listdir(directory):
                        file_path = os.path.join(directory,file_name)
                        verify_file_and_clean_file(file_path,target_file_extentions,patterns)
                except possible_exceptions as err:
                    print(err)

if __name__ == '__main__':
    try:
        if args.log:
            cleaner = logger(cleaner)

        if args.directory is not None:
            run_the_cleaners(directory_mode)

        else:
            run_the_cleaners(send_multiple_files_to_cleaner)

    except KeyboardInterrupt:
        pass
