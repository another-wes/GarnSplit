#! python2
from pyPdf import PdfFileWriter, PdfFileReader
import Tkinter as tk
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import re
def main():
    root = tk.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    out_path = tkFileDialog.askdirectory()#"S:\GARNS FOR E-FILING")-does not work, for some reason
    inputpdf = PdfFileReader(open(file_path, "rb"))
    accounts={}
    re.DOTALL=True
    for i in xrange(0,inputpdf.numPages,4):    
        letter="?"
        page=inputpdf.getPage(i).extractText()
        while "Please Issue: Garnishment" not in page: 
            i+=1#handle blank pages
            print("Blank page detected; page",i,"skipped")#program uses zero-based indexing you see
            try:
                page=inputpdf.getPage(i).extractText()
            except IndexError:
                return
        if "For:  Bank Account" in page: letter="B"
        elif "For:  Wages" in page: letter="M"
        account=re.search("Respondent\(s\):.* (?P<num>[0-9]{4,})\.0[0-9][0-9]", page)
        if account.group('num') not in accounts.keys(): 
            accounts[account.group('num')]={}
            accounts[account.group('num')]['M']=0
            accounts[account.group('num')]['B']=0
            accounts[account.group('num')]['?']=0
        accounts[account.group('num')][letter]+=1
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        output.addPage(inputpdf.getPage(i+1))
        output.addPage(inputpdf.getPage(i+2))
        output.addPage(inputpdf.getPage(i+3))
        with open(out_path+"/"+letter+str(accounts[account.group('num')][letter])+"00000%05d.pdf" % int(account.group('num')), "wb") as outputStream:
            output.write(outputStream)
main()