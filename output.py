import json
from db import ConnectDb


class Output:

    file_name = 'output.js'

    def output_to_json(self):
        file = open(self.file_name, 'w')
        documents = ConnectDb.analysis.find()
        json_str = ""
        for doc in documents:
            del doc['_id']
            json_str += ('    '+doc['name'] + ':' + json.dumps(doc['data'])+',\n')
        file.write('analysisData = {\n'+json_str+'}')
        file.close()
        print('\n输出文件: ', self.file_name)
