import os
from lxml.html.clean import clean_html
import subprocess

def convertpdf2html(pdffilepath):
    subprocess.call(['pdftotext', '-layout', pdffilepath])
    txtfilepath = pdffilepath[:-4] + '.txt'
    with open(txtfilepath, 'rb') as filename:
        txt = filename.read()
    #txt = unicode(txt, "utf-8", errors = 'ignore')
    txt = clean_html(txt)

    with open(txtfilepath, 'wb') as filename:
        filename.write(txt)
    p = subprocess.Popen(['txt2html', '--explicitheadings', 'indentparbreak', 'make_anchors', '--tables', '-8', '--xhtml', txtfilepath ], bufsize=-1, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr= subprocess.PIPE, close_fds = True)
    htmltext, stderr_text = p.communicate() 
    return htmltext

