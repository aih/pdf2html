import os
import subprocess

def convertpdf2html(pdffilepath):
    subprocess.call(['pdftotext', '-layout', pdffilepath])
    p = subprocess.Popen(['txt2html', '-tables', '--xhtml', pdffilepath.rstrip('.pdf')+'.txt'], bufsize=-1, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr= subprocess.PIPE, close_fds = True)
    htmltext, stderr_text = p.communicate() 
    return htmltext

