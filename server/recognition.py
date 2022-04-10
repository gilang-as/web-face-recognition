import recognitions as rec_face
import traceback
import storage as st


# ------------------------ Start the main stream ----------------------------
class Rec:
    def __init__(self):
        """
        -db_names: [name1,name2,...,names] string list
        -db_features: array(array,array,...,array) each array represents the characteristics of a user
        """
        self.db_names, self.db_features = st.load_images_to_database()

    def recognize_face(self, im):
        """
        Input:
            -imb64: images
        Output:
            res:{'status': if all goes well it is 'ok' otherwise it returns the error found
                'faces': [(y0,x1,y1,x0),(y0,x1,y1,x0),...,(y0,x1,y1,x0)] ,each tuple represents a detected face
                'names': ['name', 'unknown'] ready with the names he matched}
        """
        try:
            # detect face
            box_faces = rec_face.detect_face(im)
            # conditional in case no face is detected
            if not box_faces:
                res = {
                    'status': 'ok',
                    'faces': [],
                    'names': []}
                return res
            else:
                if not self.db_names:
                    res = {
                        'status': 'ok',
                        'faces': box_faces,
                        'names': ['unknown'] * len(box_faces)}
                    return res
                else:
                    # (continued) extract features
                    actual_features = rec_face.get_features(im, box_faces)
                    # compare actual_features with those stored in the database
                    match_names = rec_face.compare_faces(actual_features, self.db_features, self.db_names)
                    # save
                    res = {
                        'status': 'ok',
                        'faces': box_faces,
                        'names': match_names}
                    return res
        except Exception as ex:
            error = ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
            res = {
                'status': 'error: ' + str(error),
                'faces': [],
                'names': []}
            return res
