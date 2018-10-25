import os
import unittest
import os
from flask import Flask
from routes.fileRoutes import fileApi;
from database import db
from StringIO import StringIO
from fileOperations.common import *
from flask import Flask
from fileOperations.fileUtilities import fileUtilities
from fileOperations.models import File

filename = 'hello_world.txt'
dupfilename = 'hello_world_tmp.txt'
TEST_DB = 'test121.db'
filePath = UPLOAD_FOLDER + "/" + filename
dupfilePath = UPLOAD_FOLDER + "/" + dupfilename
md5 = "bbdde322c6040753b8289fe8addf17b9"
fileContents = 'my file contents'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        # application.config['TESTING'] = True
        application = Flask(__name__)

        application.register_blueprint(fileApi,
                                       url_prefix="/file")  ### Registers a blueprint. All /file  requests will be routed to  fileApi

        application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/" + TEST_DB  ## fileStore is SQLITE DB name

        application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = application
        with self.app.app_context():
            db.init_app(self.app)
            # db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    # os.path.exists(filePath) and os.remove(filePath)

    # executed after each test
    def tearDown(self):
        print "\n\n**********************************"

    ###############
    #### tests ####
    ###############

    def a_init(self):
        with self.app.app_context():
            db.drop_all()
            os.remove(UPLOAD_FOLDER)

    def test_b_Upload(self):
        print "1: API Test Case  ==> Test Case : 1 - File Uploading"
        d = {
            'file': (StringIO(fileContents), filename),
        }
        response = self.client.post('file/uploads', data=d)
        print "### checking response code  for uploading ###"
        self.assertEqual(response.status_code, 302)
        print "###  checking if file exists in disk  ###"
        self.assertEqual(os.path.exists(filePath), True)
        print  "### checking if entry is added to database ###"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getFileName(filename), filename)

    def test_c_download(self):
        print "2: API Test Case  ==> File Downloading"
        response = self.client.get('file/uploads/' + filename)
        print "### checking response code for downloading ###"
        self.assertEqual(response.status_code, 200)  ## checking response code
        print "### checking fileContents ###"
        self.assertEqual(response.data, fileContents)  ## checking file cpntents

    def test_d_model(self):
        print "3:Unit Test  ==> Testing Model"
        self.File = File(md5, filename, filename)
        self.assertEqual(isinstance(self.File, File), True)

    def test_e_checkMd5Exist(self):
        print "4: Unit Test ==> Testing if md5 exists in db after file insertion"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.checkMd5Exist(md5), filename)

    def test_f_getMd5(self):
        print "5: Unit Test ==> Testing getmd5 () to retreive md5 for a filename"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getMd5(filename), md5)

    def test_g_getFileName(self):
        print "6: Unit Test  ==> Testing etFileName () to filename having same md5"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getFileName(filename), filename)

    def test_h_fileDeDuping(self):
        print "7: Unit Test ==> Checking if deduping works fine"

        print "Uploading File with same content again"
        d = {
            'file': (StringIO(fileContents), dupfilename),
        }
        response = self.client.post('file/uploads', data=d)
        print "Checking if second file is uploaded again or not in the disk"
        self.assertEqual(os.path.exists(dupfilePath), False)
        print  "### checking if  second file  content is mapped to first file in db ###"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getFileName(dupfilename), filename)

    def test_i_isafeDelete(self):
        print "8: Unit Test ==> Testing safeDelete () to check if a file can be safely deleted if it's content is being reused by another file"
        with self.app.app_context():
            db.init_app(self.app)
            print "Checking if original file can be deleted"
            self.assertEqual(fileUtilities.safeDelete(filename), False)
            print "Checking if duplicate file can be deleted"
            self.assertEqual(fileUtilities.safeDelete(dupfilename), True)

    def test_j_zdelete(self):
        print "9: API Test Case : 5 - File deleting"

        print "deleting duplicate file"
        response = self.client.delete('file/uploads/' + dupfilename)
        print "Checking if file original file exist"
        self.assertEqual(os.path.exists(filePath), True)

        print "deleting original file"
        response = self.client.delete('file/uploads/' + filename)

        print "### checking response code for deleting ###"
        self.assertEqual(response.status_code, 200)  ## checking response code
        print  "### checking if file exists in the device after deletion of original and duplicate files ###"
        self.assertEqual(os.path.exists(filePath), False)
        print  "### checking if entry is deleted from database ###"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getFileName(filename), None)


if __name__ == "__main__":
    unittest.main()

