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

filename = 'hello_world.txt'
TEST_DB = 'test121.db'
filePath = UPLOAD_FOLDER + "/" + filename

fileContens = 'my file contents'


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

        application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/"+TEST_DB  ## fileStore is SQLITE DB name

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
        pass

    ###############
    #### tests ####
    ###############

    def test_aUpload(self):
        print "\n\nTest Case : 1 - File Uploading"
        d = {
            'file': (StringIO(fileContens), filename),
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

    def test_bdownload(self):
        print "\n\nTest Case : 2 - File Downloading"
        response = self.client.get('file/uploads/hello_world.txt')
        print "### checking response code for downloading ###"
        self.assertEqual(response.status_code, 200)  ## checking response code
        print "### checking fileContents ###"
        self.assertEqual(response.data, fileContens)  ## checking file cpntents

    def test_cdelete(self):
        print "\n\nTest Case : 3 - File deleting"
        print '/file/uploads/' + filename
        response = self.client.delete('file/uploads/hello_world.txt')
        print "### checking response code for deleting ###"
        self.assertEqual(response.status_code, 200)  ## checking response code
        print  "### checking if file exists in the device after deletion ###"
        self.assertEqual(os.path.exists(filePath), False)
        print  "### checking if entry is deleted from database ###"
        with self.app.app_context():
            db.init_app(self.app)
            self.assertEqual(fileUtilities.getFileName(filename), None)


if __name__ == "__main__":
    unittest.main()
