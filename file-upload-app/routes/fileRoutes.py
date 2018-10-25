import os
from flask import Flask, request, redirect, url_for, send_from_directory, abort, jsonify
from flask import Blueprint, request, jsonify, session
from fileOperations.common import *
from fileOperations.fileUtilities import fileUtilities

""" Defines all the file CRUD operations Routes for the App """

fileApi = Blueprint('routes', __name__)


@fileApi.route('/uploads/<filename>', methods=['DELETE'])
def delete_file(filename):
    """
    Route to Delete a File .
    It will delete from DB as well as the disk .
    Parameters:
     filename
       type : str
       Description : The filename
    """

    actualFile = fileUtilities.getFileName(filename)
    if not actualFile:
        abort(404)
    else:
      fileUtilities.deletefromDB(filename)
      fileToDelete = fileUtilities.safeDelete(actualFile)

      if fileToDelete:
         filePath = UPLOAD_FOLDER + "/" + actualFile
         os.path.exists(filePath) and os.remove(filePath)
      resp = jsonify(success=True)
      return resp


@fileApi.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """
     Route to Download a File . It will checks if a file with same name or another file with
     same content exists in server by checking md5 in sqlitedb
     Parameters:
      filename
        type : str
        Description : The filename
    """
    actualFilename = fileUtilities.getFileName(filename)
    if not actualFilename:
        abort(404)
    return send_from_directory(directory=UPLOAD_FOLDER, filename=actualFilename, attachment_filename=filename)


@fileApi.route('/uploads', methods=['POST'])
def upload_file():
    """
     Route to Upload a File
     Parameters:
       Nil
     For each file upload , it's mapped in sqlite as  filename => md5 .
     For all subsequent uploads, it's  md5 is checked if exists in DB.
     if exist:
        Then newfile:oldmd5 map is created
     else:
        newfile:newmd5 map is created and file is also uploaded
    """

    if request.method == 'POST':
        fileObj = request.files['file']
        this = fileUtilities(fileObj)
        this.savetoDB()

        this.uploadFile()
        return redirect(url_for('routes.download_file', filename=this.filename))

@fileApi.route('/ping', methods=['GET'])
def index():
  return "pong"