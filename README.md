# file-upload-app
##file-upload-app written in python
This is a python flask app which can upload /download and delete files .
    All the file uploaded will be stored in  the disk with filename and file md5 hash stored in sqlite DB.
    If a different file with same content is uploaded again , then then existing file content will be reused 
    by mapping then the new filename to old md5 in sqlite .
    
    File Name     |  Md5sum
    ------------- | -------------
     File X       |  *abc123*
     File Y       |  xyz456
     File Z       |  *abc123*
     
     Here , File X and File Z shave the same content , Hence Assuming File Z is 
     the latter insertion ,only File X will be  stored in the DISK .
     If we have to retrieve File Z ,which is not in disk , We query the sqliteDB 
     for the md5 of File Z, Again queries the db  with that md5 to retrived File X .
     Then sends File X by just changing the name. 
     
     
     
     To run ** 
              - git clone https://github.com/melvilgit/file-upload-app.git 
              - cd file-upload-app
              - docker-compose build
              - docker-compose  up   **
              
     How to Test ?
           download file (GET)    - curl http://<server>:8080/file/uploads/<filename>
           upload   file (POST)   - curl -i -X POST -H "Content-Type: multipart/form-data"  -F "file=@<filename>" http://server:8080/file/uploads
           delete   file (DELETE) -  curl -X DELETE http://<server>:8080/file/uploads/<filename>
      
            ##sample Test cases #### - python test.py
