import tempfile
import constants
import os
from s3 import upload_to_bucket
from xlsxwriter import Workbook


def write_to_excel(convos):
    # Create blank excel file and write to it
    temp_dir = tempfile.TemporaryDirectory()
    # for convo in convos:
    #     print(convo.getDictRepresentation())
    workbook = Workbook(os.path.join(temp_dir.name, constants.FILE))
    for convo in convos:
        convoDict = convo.getDictRepresentation()
        convoName = next(iter(convoDict))
        worksheet = workbook.add_worksheet(convoName)
        row = 0
        col = 0
        for senderMsg, receiverMsg in convoDict[convoName]:
            worksheet.write(row, col, senderMsg)
            worksheet.write(row, col + 1, receiverMsg)
            row += 1
        worksheet.autofit()
    workbook.close()
    # Upload to s3
    upload_to_bucket(os.path.join(temp_dir.name, constants.FILE), constants.FILE)
    temp_dir.cleanup()
