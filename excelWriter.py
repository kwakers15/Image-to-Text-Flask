import tempfile
import constants
import os
from s3 import upload_to_bucket
from xlsxwriter import Workbook


def write_to_excel(messages):
    # Create blank excel file and write to it
    temp_dir = tempfile.TemporaryDirectory()
    workbook = Workbook(os.path.join(temp_dir.name, constants.FILE))
    workbook.close()
    # Upload to s3
    upload_to_bucket(os.path.join(temp_dir.name, constants.FILE), constants.FILE)
    temp_dir.cleanup()
