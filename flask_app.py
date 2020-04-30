# -*- coding: utf-8 -*-
import csv
import numpy as np
from math import *
import sys
import json
from flask import *

    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)

data_competences_certif = np.genfromtxt('data_pix.csv',delimiter=',', usecols=np.arange(0,16),skip_header=1)
data_competences_pos = np.genfromtxt('data_pix_pos.csv',delimiter=',', usecols=np.arange(0,16),skip_header=1)

requis=[4,4,4,4,4,4,3,4,3,4,3,4,3,3,3,3]
nom = [ 'Mener une recherche et une veille d\'information','Gérer des données','Traiter des données','Interagir','Partager et publier','Collaborer','S\'insérer dans le monde numérique','Développer des documents textuels','Développer des documents multimedia','Adapter les documents à  leur finalité','Programmer', 'Sécuriser l\'environnement numérique','Protéger les données personnelles et la vie privée','Protéger la santé le biennaître et l\'environnement','Résoudre des problèmes techniques','Construire un environnement numérique']
cle = ['1.1', '1.2','1.3','2.1','2.2','2.3','2.4','3.1','3.2','3.3','3.4','4.1','4.2','4.3','5.1','5.2']
#retourne un tableau contenant la moyenne de chaque compétence 
def moyenne(data):
    tab=[]
    for c in range(len(data[0])):
        tab.append(0)
        notes=[]
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=np.mean(notes)
    return tab



#retourne un tableau contenant la médiane de chaque compétence 
def mediane(data):
    tab=[]
    for c in range(len(data[0])):
        tab.append(0)
        notes=[]
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=np.median(notes)
    return tab




#retourne un tableau contenant le premier quartile de chaque compétence

def pre_quartile(data):
    tab=[]
    for c in range(len(data[0])):
        notes=[]
        tab.append(0)
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=np.percentile(notes,25)
    return tab



#retourne un tableau contenant le quartile de chaque compétence
def quartile(data):
    tab=[]
    for c in range(len(data[0])):
        notes=[]
        tab.append(0)
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=np.percentile(notes,50)
    return tab



#retourne un tableau contenant le troisieme quartile de chaque compétence 

def tri_quartile(data):
    tab=[]
    for c in range(len(data[0])):
        notes=[]
        tab.append(0)
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=np.percentile(notes,75)
    return tab



#retourne un tableau contenant lécart type de chaque compétence 
def ecart_type(data):
    tab=[]
    for c in range(len(data[0])):
        notes=[]
        tab.append(0)
        for i in range(len(data)):
            notes.append(data[i][c])
        tab[c]=sqrt(np.var(notes))
    return tab




#tableau représentant le nb de personnes ayant chaque note pour la competence c
def nb_note(c,data):
    tab=[0,0,0,0,0,0]
    for i in range(len(data)):
        tab[int(data[i][c])]=tab[int(data[i][c])]+1
    return tab



    
    
#tableau représentant le nb de personnes ayant le niveau requis par competence 
def nb_requis(data):
    tab = []
    global requis
    for i in range(16):
        tab.append(0)
        tab_1 = nb_note(i,data)
        for j in range(requis[i],6):
            tab[i] =tab[i] + (tab_1[j])
    return tab




#nombre d'élèves qui ont le niveau requis - n compétences 
def requis_moins(data,n):
    if(len(data[0]) ==  16):
        global requis
    c=0
    for i in range(len(data)):
        d=0
        for g in range(len(requis)) :
            if int(data[i][g]) < requis[g] :
                d=d+1
        if d==n:
            c=c+1
    return c






    #return un tableau contenant 16 cases représentant le nb de fois que chaque compétence n a été la seule à ne pas être validée

def seule_competence_invalidee_aux(data, l):
    d=0
    if(len(data[0]) ==  16):
        global requis
    for g in range(len(requis)):
        if int(l[g]) < requis[g] :
            d=d+1
    if d==1:
        return True
    return False

def seule_competence_invalidee(data):
    if(len(data[0]) ==  16):
        global requis
    tab=[]
    for i in range(len(data[0])):
            tab.append(0)
    for i in range(len(data)):
        if seule_competence_invalidee_aux(data, data[i])==True:
            for g in range(len(requis)) :
                if data[i][g] < requis[g] :
                    tab[g]=tab[g]+1
    return tab




#retourne tableau représentant le nb d'étudiants ayant 0 puis 1 puis... puis 16 tirets
def nb_etu_par_nb_non_cert(data):
    c=0
    tab=[]
    for i in range(len(data[0])+1):
            tab.append(0)
    for i in range(len(data)):
        d=0
        for g in range(len(data[0])) :
            if int(data[i][g]) == 0 :
                d=d+1
        tab[d]=tab[d]+1
    return tab




#retourne tableau représentant pour chaque compétence le nb d'étudiants non certifiés qu'ont eu les étudiants
def nb_etu_non_certifies(data):
    tab=[]
    for i in range(len(data[0])):
        tab.append(0)
    for j in range(len(data)):
        for g in range(len(data[0])):
            if data[j][g]==0:
                tab[g]=tab[g]+1
    return tab

#créer un csv pour permettre à l'utilisateur d'exporter certaines données
def data_generator(data):
    with open('static/data_pour_utilisateur.csv','w+') as new_file:
        global nom
        global cle
        moyenne_                                =  moyenne(data)
        global requis
        mediane_                                =  mediane(data)
        ecar_type_                              =  ecart_type(data)
        premier_quartile_                       =  pre_quartile(data)
        quartile_                               =  quartile(data)
        troisieme_quartile_                     = tri_quartile(data)
        nb_requis_                              = nb_requis(data)
        seule_competence_invalidee_             = seule_competence_invalidee(data)
        fieldnames           = ['index','cle', 'nom','moyenne','requis', 'mediane','ecartype','premier_quartile','quartile','troisieme_quartile','nb_etu_ayant_niveau_requis','nb_de_fois_compétence_seule_invalidée','non_certifies','niveau_1','niveau_2','niveau__3','niveau_4','niveaux__5']
        csv_writer = csv.writer(new_file, delimiter=',')
        csv_writer.writerow(fieldnames)
        for i in range(16):

            line     = []
            nb_note_ =  nb_note(i,data)
            line.append(i+1)
            line.append(cle[i])
            line.append(nom[i])
            line.append(moyenne_[i])
            line.append(requis[i])
            line.append(mediane_[i])
            line.append(ecar_type_[i])
            line.append(premier_quartile_[i])
            line.append(quartile_[i])
            line.append(troisieme_quartile_[i])
            line.append(nb_requis_[i])
            line.append(seule_competence_invalidee_[i])
            for j in range(6):
                line.append(nb_note_[j])
            csv_writer.writerow(line)

data_generator(data_competences_certif)

def data_great(i):
    global data_competences_certif
    global nom
    global cle
    tab = []
    for j in range(len(data_competences_certif[0])):
        per = 100*float(nb_note(j,data_competences_certif)[i])/float(len(data_competences_certif))
        tab.append({"per": str(per), "note":str(nb_note(j,data_competences_certif)[i]),"cle":cle[j],"nom": nom[j]})
    return tab

     
@app.route('/',methods=['POST','GET'])
def accueil():  
    return render_template("acceuil.html")


@app.route('/choix',methods=['POST','GET'])
def choix():
    global requis
    global nom
    global data_competences_certif
    tab_1 = data_great(1)
    tab_2 = data_great(2)
    tab_3 = data_great(3)
    tab_4 = data_great(4)
    tab_5 = data_great(5)
    return render_template("choix.html",niv_1=tab_1,niv_2=tab_2,niv_3=tab_1,niv_4=tab_4,niv_5=tab_5, taille=len(data_competences_certif),nom=nom)


@app.route('/pix',methods=['POST','GET'])
def pix():
    global cle
    global nom
    global data_competences_certif
    global data_competences_pos
    size_certif = len(data_competences_certif)
    size_pos = len(data_competences_pos)
    moyenne_ = []
    moyenne_certif = moyenne(data_competences_certif)
    moyenne_pos = moyenne(data_competences_pos)
    for i in range(16):
        moyenne_.append({"note":str(moyenne_certif[i]),"cle":cle[i], "nom": nom[i], "id":"cert" })
        moyenne_.append({"note":str(moyenne_pos[i]),"cle":cle[i], "nom": nom[i], "id":"pos" })
    
    mediane_ = []
    mediane_certif = mediane(data_competences_certif)
    mediane_pos = mediane(data_competences_pos)
    for i in range(16):
        mediane_.append({"note":str(mediane_certif[i]),"cle":cle[i], "nom": nom[i], "id":"cert" })
        mediane_.append({"note":str(mediane_pos[i]),"cle":cle[i], "nom": nom[i], "id":"pos" })
    
    nb_requis_ = []
    nb_requis_certif = nb_requis(data_competences_certif)
    nb_requis_pos = nb_requis(data_competences_pos)
    for i in range(16):
        per_certif = 100*float(nb_requis_certif[i])/float(size_certif)
        per_pos = 100*float(nb_requis_pos[i])/float(size_pos)
        nb_requis_.append({ "per": str(per_certif),"note":str(nb_requis_certif[i]),"cle":cle[i], "nom": nom[i], "id":"cert" })
        nb_requis_.append({"per": str(per_pos),"note":str(nb_requis_pos[i]),"cle":cle[i], "nom": nom[i], "id":"pos" })
    print(nb_requis_)
    requis_moins_ = []
    for i in range(17):
        per_certif = 100*float(requis_moins(data_competences_certif,i))/float(size_certif)
        per_pos = 100*float(requis_moins(data_competences_pos,i))/float(size_pos)
        requis_moins_.append({"per": str(per_certif),"note":str(requis_moins(data_competences_certif,i)),"nom":"Nombre des étudiants","cle":str(i), "id":"cert" })
        requis_moins_.append({"per": str(per_pos),"note":str(requis_moins(data_competences_pos,i)),"nom":"Nombre des étudiants","cle":str(i),  "id":"pos" })
    
    seule_competence_invalidee_ = []
    seule_competence_invalidee_certif = seule_competence_invalidee(data_competences_certif)
    seule_competence_invalidee_pos = seule_competence_invalidee(data_competences_pos)
    for i in range(16):
        per_certif = 100*float(seule_competence_invalidee_certif[i])/float(size_certif)
        per_pos = 100*float(seule_competence_invalidee_pos[i])/float(size_pos)
        seule_competence_invalidee_.append({"per": str(per_certif),"note":str(seule_competence_invalidee_certif[i]),"cle":str(i), "nom": nom[i], "id":"cert" })
        seule_competence_invalidee_.append({"per": str(per_pos),"note":str(seule_competence_invalidee_pos[i]),"cle":str(i), "nom": nom[i], "id":"pos" })
    nb_etu_par_nb_non_cert_ = []
    nb_etu_par_nb_non_cert_certif =  nb_etu_par_nb_non_cert(data_competences_certif)
    nb_etu_par_nb_non_cert_pos =  nb_etu_par_nb_non_cert(data_competences_pos)
    for i in range(17):
        per_certif = 100*float(nb_etu_par_nb_non_cert_certif[i])/float(size_certif)
        per_pos = 100*float(nb_etu_par_nb_non_cert_pos[i])/float(size_pos)
        nb_etu_par_nb_non_cert_.append({"per": str(per_certif),"note":str( nb_etu_par_nb_non_cert_certif[i]),"nom":"Nombre des étudiants","cle":str(i),  "id":"cert" })
        nb_etu_par_nb_non_cert_.append({"per": str(per_pos),"note":str( nb_etu_par_nb_non_cert_pos[i]),"nom":"Nombre des étudiants","cle":str(i),  "id":"pos" })
     
    nb_etu_non_certifies_   = []
    nb_etu_non_certifies_certif =  nb_etu_non_certifies (data_competences_certif)
    nb_etu_non_certifies_pos =  nb_etu_non_certifies (data_competences_pos)
    for i in range(16):
        per_certif = 100*float(nb_etu_non_certifies_certif[i])/float(size_certif)
        per_pos = 100*float(nb_etu_non_certifies_pos[i])/float(size_pos)
        nb_etu_non_certifies_.append({"per": str(per_certif),"note":str( nb_etu_non_certifies_certif[i]),"cle":cle[i], "nom": "Nombre des étudiants", "id":"cert" })
        nb_etu_non_certifies_.append({"per": str(per_pos),"note":str( nb_etu_non_certifies_pos[i]),"cle":cle[i], "nom": "Nombre des étudiants", "id":"pos" })
    

    boxplotdata = []
    quartile_= quartile(data_competences_certif)
    pre_quartile_= pre_quartile(data_competences_certif)
    tri_quartile_= tri_quartile(data_competences_certif)
    bornes = [0,5]
    for i in range(16):
        element = {"cle":str(i+1), "quartile":[pre_quartile_[i],quartile_[i],tri_quartile_[i]], "bornes":bornes}
        boxplotdata.append(element)
    choix = int(request.form.get('choix'))
    data = []
    code=0
    size_data = 0
    if request.method=='POST':
        if choix==13:
            liste=[]
            tab=[]
            code=1
            for i in range(16):
                value=request.form.get(str(i+1))
                if (value!=None):
                    liste.append(i)
            for i in range(len(data_competences_certif[0])):
                tab.append(0)
            for etu in data_competences_certif:
                c=0
                for j in liste:
                    if(etu[j]<requis[j]):
                        break
                    c=c+1
                    if(c==len(liste)):
                        size_data = size_data+1
                        for k in range(16):
                            if(etu[k]>=requis[k]):
                                tab[k]=tab[k]+1
            for i in range(len(data_competences_certif[0])):
                if(not(i in liste)):
                    per_data = 100*float(tab[i])/float(size_data)
                    data.append({"per": str(per_data),"note":str(tab[i]), "nom": nom[i], "cle":cle[i]})
        
    return render_template("svg.html",boxplotdata=boxplotdata, data=data,code=code,moyenne = moyenne_, mediane = mediane_,nb_etu_non_certifies=nb_etu_non_certifies_,nb_etu_par_nb_non_cert=nb_etu_par_nb_non_cert_,seule_competence_invalidee= seule_competence_invalidee_,requis_moins=requis_moins_,nb_requis=nb_requis_,choix=choix,nom=nom,size_certif=size_certif,size_pos=size_pos,size_data=size_data)




#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
   app.run(debug=True)



#com=1 : par compétences
#com=2 : par domaines

#pos=1 : positionnement
#pos=2 : notes
#pos=3 : comparaison

#choix=1 : Graphique
#choix=2 : Moyenne
#choix=3 : Médiane
#choix=4 : Niveau requis
#choix=5 : Seule compétence invalidée
#choix=6 : Non certifiés
#choix=7 : Requis moins
#choix=8 : nombre d'étuditiants par nombre de non certification
