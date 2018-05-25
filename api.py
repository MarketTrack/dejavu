from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

from dejavu import Dejavu
import json

with open("dejavu.cnf.SAMPLE.backup") as f:
    config = json.load(f)

djv = Dejavu(config)

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
        def get(self):
                return {'hello': 'world'}

class RecognizeAudio(Resource):
        def post(self):
                import zlib
                decodeddata = zlib.decompress(request.data)
                jsondata = json.loads(decodeddata)
                datatorecognize = jsondata['wav_data']
                sample_rate = jsondata['sample_rate']
                from dejavu.recognize import StreamRecognizer
                recognizer = StreamRecognizer(djv)
                results = recognizer.recognize([datatorecognize], sample_rate, 10, 15)
                return results

class FingerprintAudio(Resource):
        def post(self):
                import zlib
                decodeddata = zlib.decompress(request.data)
                jsondata = json.loads(decodeddata)
                result = djv.fingerprint_stream(jsondata['wav_data'], jsondata['sample_rate'], jsondata['name'])
                return result

api.add_resource(HelloWorld, '/')
api.add_resource(RecognizeAudio, '/recognize')
api.add_resource(FingerprintAudio, '/fingerprintaudio')

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')
