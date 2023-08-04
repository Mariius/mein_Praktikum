import os
import sys
from pprint import pprint

# >> add two parend folders below to syspath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# << add two parend folders below to syspath

from source.file_handle import read_json_file, write_json_file

# >>> sha and ref will set by run gui (at build process as well) <<<

# filename
file_name = os.path.join('source','build','build_info.json')
# read file
build_info = read_json_file(file_name)
# change content
if 'RUNNER_OS' in list(os.environ.keys()):
    build_info['system'] = 'github-runner'
    build_info['number'] = os.environ['GITHUB_RUN_NUMBER'] + '.' + os.environ['GITHUB_RUN_ATTEMPT']
else:
    build_info['number'] = build_info['number']+1

pprint(build_info)


# write file
write_json_file(file_name, build_info)