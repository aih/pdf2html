import os
import subprocess

def convert(pdffilepath):
    subprocess.call(['pdftotext', '-layout', pdffilepath])
    p = subprocess.Popen(['txt2html', '-tables', '--xhtml', pdffilepath.rstrip('.pdf')+'.txt'], bufsize=-1, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr= subprocess.PIPE, close_fds = True)
    htmltext, stderr_text = p.communicate() 
    return htmltext

#TODO: Create hash for url, store html with hash ID, return url to user, display html at url
