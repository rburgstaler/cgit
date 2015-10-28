#!/c/python27/python
#NOTE: Msysgit pays no attention to the directory in the shebang path, it only looks at the
#word after the last slash.  It then uses that word to lookup the exe based on the path variable.  It also
#ignores any parameters.  So here it would find the first python.exe found while searching through
#the paths in the PATH environmental variable.  This means that it is possible to have a python.exe
#located in c:\python27\python but not use it or find it.
#Currently the logic that makes this occur is in compat/mingw.c @ parse_interpreter()

# This script uses Pygments, markdown, and Python2. You must have ALL installed
# for this to work.
#
# http://pygments.org/
# http://python.org/
# http://pythonhosted.org/Markdown
#
# It may be used with the source-filter or repo.source-filter settings
# in cgitrc.
#
# The following environment variables can be used to retrieve the
# configuration of the repository for which this script is called:
# CGIT_REPO_URL        ( = repo.url       setting )
# CGIT_REPO_NAME       ( = repo.name      setting )
# CGIT_REPO_PATH       ( = repo.path      setting )
# CGIT_REPO_OWNER      ( = repo.owner     setting )
# CGIT_REPO_DEFBRANCH  ( = repo.defbranch setting )
# CGIT_REPO_SECTION    ( = section        setting )
# CGIT_REPO_CLONE_URL  ( = repo.clone-url setting )


import sys
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
import markdown


# read stdin and decode to utf-8. ignore any unkown signs.
data = sys.stdin.read().decode(encoding='utf-8', errors='ignore')
filename = sys.argv[1]
formatter = HtmlFormatter(encoding='utf-8', style='pastie')

try:
	lexer = guess_lexer_for_filename(filename, data, encoding='utf-8')
except ClassNotFound:
	# check if there is any shebang
	if data[0:2] == '#!':
		lexer = guess_lexer(data, encoding='utf-8')
	else:
		lexer = TextLexer(encoding='utf-8')
except TypeError:
	lexer = TextLexer(encoding='utf-8')

#Check if this is mark down (hightlight does not yet support markdown)
if filename[-3:].lower() == '.md':
	sys.stdout.write(markdown.markdown(data))
else:
	# highlight! :-)
	# printout pygments' css definitions as well
	sys.stdout.write('<style>')
	sys.stdout.write(formatter.get_style_defs('.highlight'))
	sys.stdout.write('</style>')
	highlight(data, lexer, formatter, outfile=sys.stdout)
