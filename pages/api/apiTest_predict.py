from fastapi import FastAPI, Response, File, UploadFile
from typing import Optional, List
import shutil
import numpy as np
import tensorflow as tf

app = FastAPI()

@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"Hello": "World"}

@app.post('/file')
async def get_file(response: Response, files: List[UploadFile]):
    response.headers["Access-Control-Allow-Origin"] = "*"

    path_exptdata = 'D:/MLmodels_for_PXRDidentification/PiQC_detection_screening/Models/'

    error_files = []

    files_dic = {}
    for file in files:
        file_name = file.filename
        file_name = file_name.split('/')[-1]
        path = f'C:/Users/Hiro/PXRD_HiguchiLab/{file_name}'
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

            # try:
            #     lines = content.split('\n')
            #     lines = lines[0].split('\r')
            #     for i in lines:
            #         a = i[:-1].split(' ')
            #         tth = float(a[0])
            #         if 20 <= tth <80:
            #             Intensity = float(a[1])
            #             list_.append(Intensity)
            # except:
            #     lines = content.split('\r\n')
            #     for i in lines:
            #         a = i[:-1].split(' ')
            #         #list_.append(a[0])
            #         try:
            #             tth = float(a[0])
            #             if 20 <= tth <80:
            #                 Intensity = float(a[1])
            #                 list_.append(Intensity)
            #         except:
            #             pass

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
        load_model = tf.keras.models.load_model(path_exptdata+str(round(aico+aico_delta*i, 3))+'_'+str(round(aico+aico_delta*(i+1), 3))+'__'+str(12)+'__'+str(256), compile=False)
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
