import os
from aws_polly_render import start_polly

path_to_dir = "/projects/49x/tex2speech/texFiles/"
count = 0
bib_holder = []
log = open("log.log", "w")

for filename in os.listdir(path_to_dir):
    if filename.endswith(".tex"):
         file_holder = []
         count = count + 1
         if count > 0:
             print("\n\n\n" + str(filename) + " FileNum: " + str(count))
             file_holder.append(filename)
             try:
                 start_polly(file_holder, bib_holder)
                 log.write("\n\n" + str(count) + " **SUCCESS {0}".format(str(filename)))
             except (UnicodeDecodeError, RuntimeError, TypeError, NameError, AssertionError, EOFError, AttributeError, IndexError) as e:
                 log.write("\n\n" + str(count)  + " ***Failed to finish {0}: {1}\n".format(str(filename), str(e)))
    else:
        continue