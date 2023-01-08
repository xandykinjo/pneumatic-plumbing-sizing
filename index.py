import numpy as np
from operator import itemgetter
import pandas as pd
import json

schedule_40 = pd.read_csv("./public/Norma_ASTM_A_120_Schedule_40.csv", sep=";")
cotovelo_90_comum = pd.read_csv("./public/cotovelo_comum_90.csv", sep=";")
curva_90_raio_longo = pd.read_csv("./public/curva_90_raio_longo.csv", sep=";")
curva_45 = pd.read_csv("./public/curva_45.csv", sep=";")
curva_180_raio_longo = pd.read_csv("./public/curva_180_raio_longo.csv", sep=";")
te_fluxo_linha = pd.read_csv("./public/te_fluxo_linha.csv", sep=";")
te_fluxo_ramal = pd.read_csv("./public/te_fluxo_ramal.csv", sep=";")
valvula_gaveta = pd.read_csv("./public/valvula_gaveta.csv", sep=";")
valvula_globo = pd.read_csv("./public/valvula_globo.csv", sep=";")
valvula_angular = pd.read_csv("./public/valvula_angular.csv", sep=";")
valvula_retencao_portinhola = pd.read_csv("./public/valvula_retencao_portinhola.csv", sep=";")
uniao_filtroy = pd.read_csv("./public/uniao_filtroy.csv", sep=";")

def diametro(values):

    Q = float(values["Q"])
    L = float(values["L"])
    dP = float(values["dP"])
    P = float(values["P"])

    d = lambda Q, L, dP, P: 10*(np.power( ((1.663785*np.power(1/10, 3)*np.power(Q, 1.85)*L)/(dP*P)) , 1/5))
    
    return d(Q, L, dP, P)

def diametro_nominal(values, singularidade):

    values = json.loads(values)

    if(singularidade):
        values.update({"L": float(values.get("L"))+float(singularidade)})

    d = diametro(values)
    print("Diâmetro Interno (mm): ", d)
    d_nominal = None

    for index in schedule_40.index:
        if(schedule_40.loc[index, "interno (mm)"] >= d):
            d_nominal = schedule_40.loc[index, "nominal (in)"]
            break

    print("Diâmetro Nominal (in): ", d_nominal)
    return d_nominal

def singularidades(values, d_nominal):

    values = json.loads(values)

    if(d_nominal):

        if(d_nominal == "1/4" or d_nominal == "3/8"):
            d_nominal = "1/2"

        L_sing = 0

        for index in values:

            match index:
                case "cotovelo_90_comum":
                    df = cotovelo_90_comum
                case "curva_90_raio_longo":
                    df = curva_90_raio_longo
                case "curva_45":
                    df = curva_45
                case "curva_180_raio_longo":
                    df = curva_180_raio_longo
                case "te_fluxo_linha":
                    df = te_fluxo_linha
                case "te_fluxo_ramal":
                    df = te_fluxo_ramal
                case "valvula_gaveta":
                    df = valvula_gaveta
                case "valvula_globo":
                    df = valvula_globo
                case "valvula_angular":
                    df = valvula_angular
                case "valvula_retencao_portinhola":
                    df = valvula_retencao_portinhola
                case "uniao_filtroy":
                    df = uniao_filtroy

            equivalent = df.loc[df["nominal"] == d_nominal, values.get(index).get("type")]
            qtd = values.get(index).get("qtd")
            L_sing += float(equivalent)*float(qtd)

        print("Singularidades (m): ", L_sing)
        return(L_sing)


# singObj = {
#     "valvula_globo": {
#         "qtd": 1,
#         "type": "rosqueado"
#     },
#     "te_fluxo_ramal": {
#         "qtd": 1,
#         "type": "rosqueado"
#     },
#     "curva_180_raio_longo": {
#         "qtd": 1,
#         "type": "rosqueado"
#     },
# }
        
# values = {
#     "Q": ((800)/12)/2,
#     "L": 8,
#     "dP": 0.3,
#     "P": 8
# }

# result = diametro_nominal(values, None)
# print("nominal: ", result)

# L_sing = singularidades(singObj, result)
# print("L_sing: ", L_sing)

# r = diametro_nominal(values, L_sing)
# print(r)





