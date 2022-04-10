from flask import Flask, request
from flask_cors import CORS
import encoding_img as fenc
import recognition
import storage as st

app = Flask(__name__)
CORS(app)

# -------------------------- Main --------------------------------
# instantiate face recognition
rec_face = recognition.Rec()


@app.route('/')
def status():
    res = {'status': True}
    return res


@app.route("/v1/face-recognize", methods=['POST'])
def recognize_face():
    try:
        im_b64 = request.json['im_b64']
    except:
        res = {'status': 'image read error'}
        return res
    im = fenc.decodingImage(im_b64)
    res = rec_face.recognize_face(im)
    return res


@app.route("/v1/users/register", methods=['POST'])
def user_register():
    try:
        im_b64 = request.json['im_b64']
    except:
        res = {'status': 'image read error'}
        return res
    # decode image
    im = fenc.decodingImage(im_b64)
    try:
        name = request.json['id_user']
    except:
        res = {'status': 'error Id_user'}
        return res

    # I get the features of the face
    box_face = recognition.rec_face.detect_face(im)
    feat = recognition.rec_face.get_features(im, box_face)
    if len(feat) != 1:
        '''
        this means that there are no faces or there is more than one face
        '''
        res = {'status': 'there is more than one face in the image or there is none'}
        return res
    else:
        # insert the new features into the database
        status = st.insert_new_user(rec_face, name, feat, im)
        '''
        I make a publication informing that a change was made in the database, so that all
         instances update their internal memory
        '''
        # pub_local.publicar()
        # ingest image bucket
        # cursor_storage.insert_bucket_file(im,str(name))
        res = {'status': status}
        return res


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
