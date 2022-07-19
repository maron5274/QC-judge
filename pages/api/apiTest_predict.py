from fastapi import FastAPI, Response, File, UploadFile
from typing import Optional
import numpy as np
import tensorflow as tf

app = FastAPI()

@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"Hello": "World"}

@app.post('/file')
def get_file(response: Response, file: bytes = File(...)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    content = file.decode('utf-8')
    lines = content.split('\n')
    lines = lines[0].split('\r')
    model_name = 'G:/MLmodels_for_PXRDidentification/PiQC_detection_screening/Models/5.025_5.05__12__256'
    load_model = tf.keras.models.load_model(model_name, compile=False)
    list_ = []
    for i in lines:
        a = i.split('\t')
        tth = float(a[0])
        if 20 <= tth <80:
            Intensity = float(a[1])
            list_.append(Intensity)
    data_num = 1
    x_test = np.array([list_], np.float64)
    x_test = x_test-np.min(x_test, axis = 1).reshape(data_num, 1)
    x_test = x_test/np.max(x_test, axis = 1).reshape(data_num, 1)

    tf.keras.backend.set_floatx('float64')
    x_testt = x_test[..., tf.newaxis]
    pred = load_model.predict(x_testt)
    # return list_
    return {'QC': pred[0][1]}
