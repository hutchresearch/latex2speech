import os 

print("HIIII")
  
fileitem = form['filename'] 
  
# check if the file has been uploaded 
if fileitem.filename: 
    # strip the leading path from the file name 
    fn = os.path.basename(fileitem.filename) 
      
   # open read and write the file into the server 
    open(fn, 'wb').write(fileitem.file.read()) 