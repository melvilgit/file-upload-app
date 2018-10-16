import hashlib
import os

from .models import File
from werkzeug.utils import secure_filename
from database import db
from .common import *


class fileUtilities:
    """ fileUtilities which serves all the helper functions for file CRUD API's in fileRoutes.py """

    def __init__(self, fileObj):

        self.fileMd5 = hashlib.md5(fileObj.read()).hexdigest()  # read() will moves the file handle to the file start
        fileObj.stream.seek(
            0)  # Moves the file handle to start so that uploaded file is never empty .
        self.filename = secure_filename(fileObj.filename)
        self.fileObj = fileObj
        self.existingFileMd5 = fileUtilities.checkMd5Exist(
            self.fileMd5)  # Check if md5 exists in sqlite , True/False
        if self.existingFileMd5:
            self.File = File(self.fileMd5, self.filename, self.existingFileMd5)
        else:
            self.File = File(self.fileMd5, self.filename, self.filename)  # The File Object Modal

    def savetoDB(self):

        """Function to save filename,md5 to sqlite . """
        try:
            db.session.add(self.File)
            db.session.commit()
            print ('Record was successfully added')
        except Exception as e:
            print e

    def uploadFile(self):

        """ Function to Upload file . existingFileMd5  set in class constructor indicates if file content already exists or not """

        if not self.existingFileMd5:
            self.fileObj.save(os.path.join(UPLOAD_FOLDER, self.filename))
        else:
            print "### File Present not uploading ###"

    @staticmethod
    def checkMd5Exist(md5):

        """ Function to check if md5 of a file exists in DB
            Parameters
              md5 - md5sum
            Return
              filename/None
         """
        try:
            filename = db.session.query(File).filter(File.md5 == md5).first().name
            return filename
        except Exception as e:
            print e
            return None

    @staticmethod
    def getMd5(filename):
        """Function to retreive md5 of a file"""
        md5 = db.session.query(File).filter(
            File.name == filename).one().md5  # Gets md5 of the file requested from sqlite
        return md5

    @staticmethod
    def deletefromDB(filename):
        """ Function to delete a filename from DB
            Parameters
              filename - name of file
            Return
             True/False
        """
        try:
            fileExists = db.session.query(File).filter(File.name == filename).one()
            if fileExists:
                md5 = fileUtilities.getMd5(filename)
                File.query.filter(File.name == filename).delete()
                db.session.commit()
            return md5

        except Exception as e:
            print e

    @staticmethod
    def getFileName(filename):

        """ Function to get filename of the file which stores content of the requested file.
            Parameters
              filename - name of file
            Return
             Filename - It can be the either the same input filename or any other filename with the md5  of requested filename
        """
        try:
            filename = db.session.query(File).filter(
                File.name == filename).first().map  # Get the filename of the file with the md5 from sqlite
            return filename
        except Exception as e:
            print e
            return None

    @staticmethod
    def safeDelete(filename):

        """Function to check if a file can be safely deleted, Similar to unlink system call.
           Check if any other file is using the content , if no file is pointing, it is safe to delete
           Parameters
             filename - name of file
           Return
              True/False
           """


        exists = db.session.query(
            db.session.query(File).filter_by(map=filename).exists()
        ).scalar()

        if exists:
            return False
        else:
            return  True

