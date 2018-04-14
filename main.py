#!/usr/bin/python3

import sys, getopt, os
import zipfile
from time import localtime, strftime

def usage():
   usageFile = open(os.path.dirname(os.path.realpath(__file__))+"/usage.txt","r")
   print(usageFile.read())


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def main(argv):

   if len(sys.argv)<2:
      usage()
      sys.exit(2)

   inputfile = ''
   outputfile = ''
   chglogMsg = "\t--------------------------\n\t|  " + strftime("%d.%m.%y  |  %H:%M:%S", localtime()) + "  |\n\t--------------------------\n\n\t-- ";
   isVerbose = False
   includeGit = False
   isChgLog = False

   try:
      opts, args = getopt.getopt(argv,"gvhc:i:o:",["ifile=","ofile=","changelog="])
      # print(opts)
      # print(args)
   except Exception as e:
      print(e)
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-v", "--verbose"):
         isVerbose = True
      elif opt in ("-g", "--git"):
         includeGit = True
      elif opt in ("-c", "--changelog"):
         isChgLog = True
         chglogMsg = chglogMsg + arg

   if(outputfile):
      pass
   else:
      outputfile = inputfile.split("/")[0]

   outputfile = outputfile + "_" + strftime("D%y%m%d_H%H%M%S", localtime()) + ".zip"

   zf = zipfile.ZipFile(outputfile, "w")

   for dirname, subdirs, files in os.walk(inputfile):
      if(includeGit == False):
         dirs = dirname.split("/")
         try:
            dirs.index(".git")
            continue
         except Exception as e:
            pass

            
      if(isVerbose):
         print(dirname)
      zf.write(dirname)
      for filename in files:
         zf.write(os.path.join(dirname, filename))

   if(isChgLog):
      zf.writestr("CHANGE_LOG",chglogMsg)
   zf.close()


   print("\n\n",strftime("%d.%m.%y  %H:%M:%S", localtime()),"\n\n", outputfile," ",convert_bytes(os.stat(outputfile).st_size),"\n\n")
   print("Change Log Message:\n",chglogMsg)
if __name__ == "__main__":
   main(sys.argv[1:])
