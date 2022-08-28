from fastapi import FastAPI, Response, File, UploadFile, WebSocket
from typing import Optional, List
from fastapi.responses import FileResponse
import shutil
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import json

app = FastAPI()

@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"Hello": "World"}

@app.post('/uploadfile')
async def get_file(response: Response, files: List[UploadFile]):
    response.headers["Access-Control-Allow-Origin"] = "*"
    filenames = []
    for file in files:
        file_name = file.filename
        file_name = file_name.split('/')[-1]
        path = f'../../text_folda/{file_name}'
        filenames.append(file_name)
        with open(path, 'w+b') as buffer:
                shutil.copyfileobj(file.file, buffer)
    return filenames

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    await websocket.send_text('0%')
    filenames = data['filenames']

    path_model = 'C:/Users/maron/qc-data/models/'
    error_files = []
    files_dic = {}

    for file_name in filenames:
        path = f'../../text_folda/{file_name}'
        try:
            f = open(path, 'r')
            lines = f.readlines()
            list_ = []
            for i in lines:
                if i[0] == "*" or i[0] == '#':
                    continue
                try:
                    a = i[:-1].split('\t')
                    tth = float(a[0])
                except:
                    a = i[:-1].split(' ')
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
            files_dic[file_name] = x_testt
        except:
            error_files.append(file_name)

    aico = 5.0
    aico_delta = 0.025
    dic_detection = {"A": [], "B": [], "C": []}
    list__=[]
    model_num = 2
    for i in range(model_num):
        tf.keras.backend.clear_session()
        load_model = tf.keras.models.load_model(path_model+str(round(aico+aico_delta*i, 3))+'_'+str(round(aico+aico_delta*(i+1), 3))+'__'+str(12)+'__'+str(256), compile=False)
        for file_name in files_dic:
            try:
                x_testt = files_dic[file_name]
                pred = load_model.predict(x_testt)[0][1]
                pred = round(pred, 5)
                list__.append(pred)
                if pred < 0.95:
                    continue

                if 0.95 <= pred < 0.99:
                    dic_detection['C'].append([file_name, pred, round(aico+aico_delta*i, 3)])
                elif 0.99 <= pred < 0.999:
                    dic_detection['B'].append([file_name, pred, round(aico+aico_delta*i, 3)])
                else:
                    dic_detection['A'].append([file_name, pred, round(aico+aico_delta*i, 3)])
            except:
                error_files.append(file_name)
        await websocket.send_text(str((i+1)*100/model_num)+'%')
        

    sortsecond = lambda val : val[1]
    dicA_sorted = sorted(dic_detection['A'], key = sortsecond, reverse = True)
    dicB_sorted = sorted(dic_detection['B'], key = sortsecond, reverse = True)
    dicC_sorted = sorted(dic_detection['C'], key = sortsecond, reverse = True)

    def remove_overlap(list_sorted, file_names):
        for __ in list_sorted[:]:
            file_name = __[0]
            if file_name in file_names:
                list_sorted.remove(__)
            else:
                file_names.append(file_name)
        return list_sorted, file_names

    remove_overlap_files = 1
    if remove_overlap_files == 1:
        file_names = []
        dicA_sorted, file_names = remove_overlap(dicA_sorted, file_names)
        dicB_sorted, file_names = remove_overlap(dicB_sorted, file_names)
        dicC_sorted, file_names = remove_overlap(dicC_sorted, file_names)

    dic_None = {'A': 0, 'B': 0, 'C': 0}
    for i in dic_detection:
        if len(dic_detection[i]) == 0:
            dic_detection[i] = [['None', 'None', 'None']]
            dic_None[i] = -1

    num_Adata, num_Bdata, num_Cdata = len(dicA_sorted)+dic_None['A'], len(dicB_sorted)+dic_None['B'], len(dicC_sorted)+dic_None['C']
    AJson = json.dumps({"A":list(dicA_sorted)})
    BJson = json.dumps({"B":list(dicB_sorted)})
    CJson = json.dumps({"C":list(dicC_sorted)})
    numJson = json.dumps({"numA" : num_Adata, "numB" : num_Bdata, "numC" : num_Cdata})
    hogehoge = list(set(error_files))
    errorJson = json.dumps({"error" : hogehoge}) 
    await websocket.send_json({"A" : dicA_sorted, "B": dicB_sorted, "C" : dicC_sorted, "error" : list(set(error_files)), "numA" : num_Adata, "numB" : num_Bdata, "numC" : num_Cdata})

@app.post('/file')
async def get_file(response: Response, files: List[UploadFile]):
    response.headers["Access-Control-Allow-Origin"] = "*"

    path_model = 'C:/Users/maron/qc-data/models/'
    #path_model = 'D:/MLmodels_for_PXRDidentification/PiQC_detection_screening/Models/'

    error_files = []

    files_dic = {}
    for file in files:
        file_name = file.filename
        file_name = file_name.split('/')[-1]
        path = f'../../text_folda/{file_name}'
        try:
            with open(path, 'w+b') as buffer:
                shutil.copyfileobj(file.file, buffer)
            f = open(path, 'r')
            lines = f.readlines()

            list_ = []
            for i in lines:
                if i[0] == "*" or i[0] == '#':
                    continue
                try:
                    a = i[:-1].split('\t')
                    tth = float(a[0])
                except:
                    a = i[:-1].split(' ')
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
            files_dic[file_name] = x_testt

        except:
            error_files.append(file_name)


    aico = 5.0
    aico_delta = 0.025
    dic_detection = {"A": [], "B": [], "C": []}
    list__=[]
    for i in range(2):
        tf.keras.backend.clear_session()
        load_model = tf.keras.models.load_model(path_model+str(round(aico+aico_delta*i, 3))+'_'+str(round(aico+aico_delta*(i+1), 3))+'__'+str(12)+'__'+str(256), compile=False)
        for file_name in files_dic:
            try:
                x_testt = files_dic[file_name]
                pred = load_model.predict(x_testt)[0][1]
                pred = round(pred, 5)
                list__.append(pred)
                if pred < 0.95:
                    continue

                if 0.95 <= pred < 0.99:
                    dic_detection['C'].append([file_name, pred, round(aico+aico_delta*i, 3)])
                elif 0.99 <= pred < 0.999:
                    dic_detection['B'].append([file_name, pred, round(aico+aico_delta*i, 3)])
                else:
                    dic_detection['A'].append([file_name, pred, round(aico+aico_delta*i, 3)])
            except:
                error_files.append(file_name)



    sortsecond = lambda val : val[1]
    dicA_sorted = sorted(dic_detection['A'], key = sortsecond, reverse = True)
    dicB_sorted = sorted(dic_detection['B'], key = sortsecond, reverse = True)
    dicC_sorted = sorted(dic_detection['C'], key = sortsecond, reverse = True)

    def remove_overlap(list_sorted, file_names):
        for __ in list_sorted[:]:
            file_name = __[0]
            if file_name in file_names:
                list_sorted.remove(__)
            else:
                file_names.append(file_name)
        return list_sorted, file_names

    remove_overlap_files = 1
    if remove_overlap_files == 1:
        file_names = []
        dicA_sorted, file_names = remove_overlap(dicA_sorted, file_names)
        dicB_sorted, file_names = remove_overlap(dicB_sorted, file_names)
        dicC_sorted, file_names = remove_overlap(dicC_sorted, file_names)

    dic_None = {'A': 0, 'B': 0, 'C': 0}
    for i in dic_detection:
        if len(dic_detection[i]) == 0:
            dic_detection[i] = [['None', 'None', 'None']]
            dic_None[i] = -1

    num_Adata, num_Bdata, num_Cdata = len(dicA_sorted)+dic_None['A'], len(dicB_sorted)+dic_None['B'], len(dicC_sorted)+dic_None['C']

    #return [num_Adata, dicA_sorted],[num_Bdata, dicB_sorted], [num_Cdata, dicC_sorted]
    return dicA_sorted, dicB_sorted, dicC_sorted, num_Adata, num_Bdata, num_Cdata, list(set(error_files))

@app.get('/fig/{filename}', response_class=FileResponse)
def draw_fig(response: Response, filename: str):
    response.headers["Access-Control-Allow-Origin"] = "*"

    path = f'../../text_folda/{filename}'
    f = open(path, 'r')
    lines = f.readlines()

    list_ = []
    for i in lines:
        if i[0] == "*" or i[0] == '#':
            continue
        try:
            a = i[:-1].split('\t')
            tth = float(a[0])
        except:
            a = i[:-1].split(' ')
            tth = float(a[0])
        if 20 <= tth <80:
            Intensity = float(a[1])
            list_.append(Intensity)

    x_data = np.linspace(20,80,len(list_))
    y_data = list_
    fig, ax = plt.subplots()
    ax.tick_params(labelleft=False)
    ax.plot(x_data,y_data,c='black')
    ax.set_xlabel("2θ [deg.]")
    ax.set_ylabel("Intensity [a.u.]")
    path_fig = f'../../fig/{filename}.png'
    plt.savefig(path_fig)
    plt.gca().clear()
    return path_fig
