
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

import os
import  joblib
import hashlib
import lime
from lime import lime_tabular
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from managed_db import *

html_temp = """
		<div style="background-color:{};padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Kalp hastaligi Web Uygulamasi ML-Streamlit </h1>
		<h5 style="color:white;text-align:center;">Kalp Hastaligi </h5>
		</div>
		"""
prescriptive_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:10px">Kalp Hastaligindan Kurtulma Yollari</h3>
		<ul>
		<li style="text-align:justify;color:black;padding:10px">Gunluk Egzersiz</li>
		<li style="text-align:justify;color:black;padding:10px">Dinlenme</li>
		<li style="text-align:justify;color:black;padding:10px">Dusuk Alkol</li>
		<li style="text-align:justify;color:black;padding:10px">Duzenli Diet</li>
		<li style="text-align:justify;color:black;padding:10px">Duzenli Spor</li>
		<li style="text-align:justify;color:black;padding:10px">Bol Temiz Hava ve Su</li>
		<li style="text-align:justify;color:black;padding:10px">Stresten Uzak Durma</li>
		<ul>
	</div>
	"""


descriptive_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:10px">Tanim</h3>
		<p>Kalp hastalığı, kalpte meydana gelen ve kalbi etkileyen herhangi bir bozukluğu kapsayan bir terimdir. Kalp hastalığı başlığı altında koroner arter hastalığı gibi kan damar hastalıkları, kalp ritmi problemleri (aritmiler) ve bu hastalıkların yanında doğuştan gelen kalp kusurları yer alır..</p>
	</div>
	"""

def load_image(img):
    im = Image.open(os.path.join(img))
    return im


bagimsiz_degiskenler = ['age',
'anaemia',                      
'creatinine_phosphokinase',      
'diabetes',                      
'ejection_fraction',             
'high_blood_pressure',           
'platelets',                   
'serum_creatinine',            
'serum_sodium',                  
'sex'         ,                  
'smoking'    ,                   
'time'           ,               
]
cinsiyet_d = {'Erkek':0,'Kadin':1}
ozel_dict = {"Hayir":0,"Evet":1}

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value
def get_key(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

def get_fvalue(val):
    ozel_dict = {"Hayir": 0, "Evet": 1}
    for key,value in ozel_dict.items():
        if val == key:
            return value

def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model
    


def generate_hashes(parola):
    return hashlib.sha256(str.encode(parola)).hexdigest()

def verify_hashes(parola,hashed_text):
    if generate_hashes(parola) == hashed_text:
        return hashed_text
    return False

def main():
    '''Kalp Sagligi-Gelecek Tahminleme Web Uygulmasi'''
    st.title('Kalp Hastaligi Gelecek Tahminleme Web Uygulmasi')
    menu =['Anasayfa', 'Giris', 'KayitOl']
    sub_menu = ["Grafik","Gelecek_Tahminleme","Metrics"]
    st.markdown(html_temp.format('royalblue'),unsafe_allow_html=True)
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == 'Anasayfa':
        st.header('Anasayfa')
        #st.text('Heart Hastaligi Nedir?')
        st.markdown(descriptive_message_temp, unsafe_allow_html=True)
        st.markdown(prescriptive_message_temp,unsafe_allow_html=True)
        st.image(load_image('/home/fingolfin/PycharmProjects/heart_app/1.jpg'))
    elif choice == 'Giris':
        kullanici_adi =st.sidebar.text_input('Kullanici Adi')
        parola         =st.sidebar.text_input('Parola',type='password')
        if st.sidebar.checkbox('Giris'):
            create_usertable()
            hashes_pswd = generate_hashes(parola)
            result =login_user(kullanici_adi,verify_hashes(parola,hashes_pswd))
            #if parola == '1234":
            if result:
                st.success('Hosgeldiniz {}'.format(kullanici_adi))
                activity = st.selectbox('Activity',sub_menu)
                if activity == "Grafik":
                    st.subheader("Grafik Gorselleme")
                    df = pd.read_csv("/home/fingolfin/PycharmProjects/heart_app/clean_heart_dataset.csv")
                    st.dataframe(df)
                    freq_df = pd.read_csv('/home/fingolfin/PycharmProjects/heart_app/freq_df_heart_dataset.csv')
                    st.bar_chart(freq_df['count'])

                    if st.checkbox('Area Chart'):
                        all_columns =df.columns.to_list()

                        feat_choices  =st.multiselect('Sec Bir Ozellik',all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)



                    df['death_event'].value_counts().plot(kind="bar")
                    st.pyplot()
                elif activity == 'Gelecek_Tahminleme':
                    st.subheader('Gelecek Tahminleme')

                    age =st.number_input('Yas',40,95)
                    sex =st.radio('Cinsiyet',tuple(cinsiyet_d.keys()))
                    anaemia =st.selectbox('Anemi',tuple(ozel_dict.keys()))
                    diabetes =st.selectbox('Diabet',tuple(ozel_dict.keys()))
                    high_blood_pressure =st.selectbox('Yuksek Kan Basinci',tuple(ozel_dict.keys()))
                    smoking =st.selectbox('Sigara',tuple(ozel_dict.keys()))
                    creatinine_phosphokinase =st.number_input('Kreatinin_Fosfokinaz',23,7900)
                    ejection_fraction =st.number_input('Ejeksiyon Fraksiyonu',14,80    )
                    platelets =st.number_input('trombositler',25000,850000)
                    serum_creatinine =st.number_input('Serum Kreatinin',0,10)
                    serum_sodium =st.number_input('Serum Sodyum',110,150)
                    time =st.number_input('Zaman',4,285)
                    feature_list = [age,get_value(sex,cinsiyet_d),get_fvalue(anaemia),
                                    get_fvalue(diabetes),get_fvalue(high_blood_pressure),get_fvalue(smoking),
                                    creatinine_phosphokinase,ejection_fraction,platelets,serum_creatinine,serum_sodium,time]
                    st.write(bagimsiz_degiskenler)
                    pretty_result = {"age":age,'sex':sex,'anaemia':anaemia,'diabetes':diabetes,
                                     'high_blood_pressure':high_blood_pressure,'smoking':smoking,
                                     'creatinine_phosphokinase':creatinine_phosphokinase,'ejection_fraction':ejection_fraction,
                                     'platelets':platelets,'serum_creatinine':serum_creatinine,'serum_sodium':serum_sodium,
                                     'time':time
                                     }
                    st.json(pretty_result)
                    single_sample = np.array(feature_list).reshape(1,-1)

                    model_choice = st.selectbox('Sec Modelini:',['LR','KNN','DecisionTree'])
                    if st.button('Tikla'):
                        if model_choice == 'KNN':
                            loaded_model =load_model('/home/fingolfin/PycharmProjects/heart_app/KNN_Heart_Result.pkl')
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)
                        elif model_choice == 'DecisionTree':
                            loaded_model = load_model('/home/fingolfin/PycharmProjects/heart_app/Decision Tree_Heart_Result.pkl')
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)
                        else:
                            loaded_model = load_model('/home/fingolfin/PycharmProjects/heart_app/LR_Heart_Result.pkl')
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)

                        st.write(prediction)
                        if prediction == 1:
                            st.warning('Hasta Oluyor.')
                        else:
                            st.success('Hasta Yasiyor.')
                            pred_probability_score = {"Olum": pred_prob[0][0] * 100, "Yasa": pred_prob[0][1] * 100}
                            st.subheader("Gelecek Tahminin Olasiligi: {}".format(model_choice))
                            st.json(pred_probability_score)
                    if st.checkbox("Interpret"):
                        if model_choice == "KNN":
                            loaded_model = load_model("/home/fingolfin/PycharmProjects/heart_app/KNN_Heart_Result.pkl")
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)



                        elif model_choice == "DecisionTree":
                            loaded_model =load_model('/home/fingolfin/PycharmProjects/heart_app/Decision Tree_Heart_Result.pkl')
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)

                        else:
                            loaded_model = load_model("/home/fingolfin/PycharmProjects/heart_app/LR_Heart_Result.pkl")
                            prediction = loaded_model.predict(single_sample)

                            pred_prob = loaded_model.predict_proba(single_sample)


                            # loaded_model = load_model("models/logistic_regression_model.pkl")
                            # 1 Die and 2 Live
                            df = pd.read_csv("/home/fingolfin/PycharmProjects/heart_app/clean_heart_dataset.csv")
                            x = df[['age',
                                     'anaemia',
                                     'creatinine_phosphokinase',
                                     'diabetes',
                                     'ejection_fraction',
                                    'high_blood_pressure',
                                    'platelets',
                                    'serum_creatinine',
                                    'serum_sodium',
                                    'sex'         ,
                                    'smoking'    ,
                                    'time'           ,
                                    ]]

                            feature_names = ['age',
                                     'anaemia',
                                     'creatinine_phosphokinase',
                                     'diabetes',
                                     'ejection_fraction',
                                    'high_blood_pressure',
                                    'platelets',
                                    'serum_creatinine',
                                    'serum_sodium',
                                    'sex'         ,
                                    'smoking'    ,
                                    'time'           ,   ]
                            class_names = ['Die(1)', 'Live(0)']
                            explainer = lime.lime_tabular.LimeTabularExplainer(x.values, feature_names=feature_names,
                                                                               class_names=class_names,
                                                                               discretize_continuous=True)
                            # The Explainer Instance
                            exp = explainer.explain_instance(np.array(feature_list), loaded_model.predict_proba_1,
                                                             num_features=13, top_labels=1)
                            exp.show_in_notebook(show_table=True, show_all=False)
                            # exp.save_to_file('lime_oi.html')
                            st.write(exp.as_list())
                            new_exp = exp.as_list()
                            label_limits = [i[0] for i in new_exp]
                            # st.write(label_limits)
                            label_scores = [i[1] for i in new_exp]
                            plt.barh(label_limits, label_scores)
                            st.pyplot()
                            plt.figure(figsize=(20, 10))
                            fig = exp.as_pyplot_figure()
                            st.pyplot()




                    



            else:
                st.warning('Hatali Giris Kullanici Adi veya Sifre')

    if choice == 'KayitOl':
        yeni_kullanici = st.text_input('Kullanici Adi')
        yeni_parola    = st.text_input('Parola',type='password')

        onayla_parola = st.text_input('Yeniden Parola',type='password')

        if yeni_parola == onayla_parola:
            st.success('Parola Dogrulandi.')
        else:
            st.warning('Parola ayni degil.')

        if st.button('KabulEt'):
            create_usertable()
            hashed_yeni_parola = generate_hashes(yeni_parola)
            add_userdata(yeni_kullanici,hashed_yeni_parola)
            st.success('Basarili sekilde yeni bir kullanici olusturuldu.')
            st.info('Kabul Edildi.')

















if __name__ == '__main__':
    main()

