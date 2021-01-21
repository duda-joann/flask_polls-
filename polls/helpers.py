

def allowed_file(filename: str):
    """ checking if loaded by resource file is an extension png, jpg, jpeg  or gif """
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']
