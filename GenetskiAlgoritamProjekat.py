import random

global radniDani
radniDani={"Ponedeljak","Utorak","Sreda","Cetvrtak","Petak"}
class GenetskiAlgoritam:
    def __init__(self,ucionice,m):
        self.ucionice=ucionice
        self.m=m
        self.generacija=100
        self.mutacijarate=0.2
        self.elitizam=4
    def optimizacija(self):
        najboljaOcena=-10000
        najboljaJedinka=None
        najboljePocinjanje=None
        populacija,pocinjanje=self.napravljenaPopulacija()
        ocene,populacija,pocinjanje=self.oceni(populacija,pocinjanje)                     #nek budu sortirane
        elitizam = []
        for i in range(0, self.elitizam, 1):
            elitizam.append(populacija[i])
        if ocene[0]>najboljaOcena:
            najboljaOcena=int(ocene[0])
            najboljaJedinka=populacija[0]
        for i in range(0,self.generacija,1):
            selekcija,pocinjanje=self.ruletskaSelekcija(populacija,ocene,pocinjanje)
            populacija,pocinjanje=self.novaGeneracijaK(selekcija,pocinjanje,elitizam)
            elitizam = []
            for i in range(0, self.elitizam, 1):
                elitizam.append(populacija[i])
            populacija,pocinjanje=self.mutacija1(populacija,pocinjanje)
            ocene,populacija,pocinjanje=self.oceni(populacija,pocinjanje)
            if ocene[0]>najboljaOcena:
                najboljaOcena=ocene[0]
                najboljaJedinka=populacija[0]
                najboljePocinjanje=pocinjanje[0]
        najboljaJedinka,najboljePocinjanje=self.mar(najboljaJedinka,najboljePocinjanje)
        return najboljaJedinka,najboljePocinjanje,najboljaOcena
    def napravljenaPopulacija(self):
        populacija=[]
        raspored=[]
        rasporedSati=[]
        kraj = []
        self.n=len(self.ucionice)
        for i in range(0,self.n,1):
            for j in range(0,self.m,1):
                lista=[]
                raspored.append(lista)
                rasporedSati.append(lista)
        with open("data_timetable.txt") as f:
            contents = f.readlines()
        listaSati=[]
        contents=contents[2:]
        self.velicinaPredmeta=len(contents)
        for i in contents:
            a=i.split(" ")
            b=a[-1]
            listaSati.append(int(b))
        brojac=0
        pocinjanje=[]
        sati=[]
        self.populationSize = 100
        for k in range(0,self.populationSize,1):
            pocinjanje=[]
            raspored = []
            rasporedSati = []
            self.n = len(self.ucionice)
            for i in range(0, self.n, 1):
                for j in range(0, self.m, 1):
                    lista = []
                    raspored.append(lista)
                    rasporedSati.append(lista)
            pamtiSate=self.n*self.m*[None]
            neMozebrojac=0
            i=0
            while i<len(contents):
                i=i+1
                broj=random.randint(0,24)
                if raspored[broj]==[]:
                    b=random.randint(0,240)
                    raspored[broj].append(contents[i-1])
                    rasporedSati[broj].append(listaSati[i-1])
                    c=[]
                    d=[]
                    for t in range(len(raspored[broj])):
                        if t%2==0:
                            c.append(raspored[broj][t])
                        else:
                            d.append(raspored[broj][t])
                    raspored[broj]=c
                    rasporedSati[broj]=d
                    pamtiSate[broj]=b
                else:
                    duzinaPredavanja=rasporedSati[broj][-1]
                    proslo=len(raspored[broj])*15
                    for j in range(0,len(raspored[broj]),1):
                        if len(rasporedSati[j])!=0:
                            proslo=proslo+rasporedSati[j][-1]
                    if duzinaPredavanja<(840-proslo-rasporedSati[broj][-1]):
                        raspored[broj].append(contents[i-1])
                        rasporedSati[broj].append(listaSati[i-1])
                    else:
                        if duzinaPredavanja-rasporedSati[broj][-1]>=15:
                            raspored[broj].append(contents[broj])
                            rasporedSati[broj].append(listaSati[broj])
                            pamtiSate[i-1]=pamtiSate[i-1]-duzinaPredavanja-15
                        else:
                            i=i-1
            populacija.append(raspored)
            p=[]
            for sat in pamtiSate:
                p.append(sat)
            pocinanje = p
            kraj.append(pocinanje)
            sati.append(rasporedSati)
        return populacija,kraj

    def oceni(self,populacija,pocinjanje):
        ocene=[]
        for i in range(0,len(populacija),1):
            zbir=0
            r=0
            raspored=populacija[i]
            vremena=pocinjanje[i]
            for j in range(0,len(raspored),1):
                a=raspored[j]
                r=r+len(a)
                if a==[]:
                    pr=840*840
                else:
                    try:
                        pauza=int(vremena[j])
                        pauza = pauza + (len(a) - 1) * 15
                        for k in range(0, len(a), 1):
                            b = int(a[k].split(" ")[-1])
                            pauza = pauza + b
                        pr = vremena[j] * (840 - pauza)
                    except:
                        pr=840*840
                zbir=zbir+pr
            ocene.append(zbir)
        for i in range(0,len(ocene),1):
            for j in range(i+1,len(ocene),1):
                if ocene[j]>ocene[i]:
                    ocene[i],ocene[j]=ocene[j],ocene[i]
                    populacija[i],populacija[j]=populacija[j],populacija[i]
                    pocinjanje[i],pocinjanje[j]=pocinjanje[j],pocinjanje[i]
        return ocene,populacija,pocinjanje
    def mar(self,raspored,pocinjanje):
        for i in range(0,len(raspored),1):
            danIuc=raspored[i]
            if danIuc==[] and pocinjanje[i]!=None:
                for j in range(i+1,len(pocinjanje),1):
                    if pocinjanje[j]==None:
                        pocinjanje[i],pocinjanje[j]=pocinjanje[j],pocinjanje[i]
        for i in range(0,len(raspored),1):
            if raspored[i]==[]:
                pocinjanje[i]=None
        return raspored,pocinjanje

    def ruletskaSelekcija(self,populacija,ocene,pocinjanje):
        selekcija=[]
        pocinjanje1=[]
        for i in range(0,len(populacija),2):
            prilagodjenost=[]
            for j in range(0,len(ocene),1):
                b=random.random()
                podocena=b*ocene[j]
                prilagodjenost.append(podocena)
            sort,pocinjanje2=self.sortiraj(populacija,prilagodjenost,pocinjanje)
            selekcija.append(sort[0])
            selekcija.append(sort[1])
            pocinjanje1.append(pocinjanje2[0])
            pocinjanje1.append(pocinjanje2[1])
        return selekcija,pocinjanje1
    def sortiraj(self,populacija,prilagodjenost,pocinjanje):
        for i in range(0,len(populacija),1):
            for j in range(i+1,len(populacija),1):
                if prilagodjenost[j]>prilagodjenost[i]:
                    prilagodjenost[i],prilagodjenost[j]=prilagodjenost[j],prilagodjenost[i]
                    populacija[i], populacija[j] = populacija[j], populacija[i]
                    pocinjanje[i],pocinjanje[j]=pocinjanje[j],pocinjanje[i]
        return populacija,pocinjanje

    def novaGeneracijaK(self,selekcija,prilagodjenost,elitizam):
        lista=[]
        brojac=0
        for i in range(0,self.elitizam,1):
            lista.append(elitizam[i])
        while brojac<=len(selekcija)-self.elitizam:
            a=random.randint(0,len(selekcija)-1)
            b = random.randint(0, len(selekcija)-1)
            otac=selekcija[a]
            majka=selekcija[b]
            pr1=prilagodjenost[a]
            pr2=prilagodjenost[b]
            sin,cerka,prilagodjenost1,prilagodjenost2=self.ukrsti1(otac,majka,pr1,pr2)
            brojac=brojac+2
            selekcija[a]=sin
            selekcija[b]=cerka
            prilagodjenost[a]=prilagodjenost1
            prilagodjenost[b]=prilagodjenost2
        return selekcija,prilagodjenost
    def ukrsti1(self,otac,majka,prilagodjenost1,prilagodjenost2):                             #DODATI DA SE I SATI SVAPUJU
        o1=otac
        o2=majka
        r=random.randint(0,len(otac)-1)
        for i in range(0,r+1,1):
            otac[i],majka[i]=majka[i],otac[i]
        brojac=0
        for i in range(0,len(otac),1):
            o=otac[i]
            for j in range(0,len(o),1):
                brojac=brojac+1
        if brojac==60:
            return otac,majka,prilagodjenost2,prilagodjenost1
        else:
            return o1,o2,prilagodjenost1,prilagodjenost2

    def mutacija1(self,populacija,prilagodjenost):
        lista=[]
        for i in range(0,len(populacija),1):
            gen=populacija[i]
            a=prilagodjenost[i]
            if gen!=[]:
                for j in range(0,len(gen),1):
                    dan=gen[j]
                    try:
                        pocetak = int(a[j])
                        danIucionica = prilagodjenost[i]
                        r = random.random()
                        if r < self.mutacijarate:
                            velicina = self.n * self.m - 1
                            b = random.randint(0, velicina)
                            dan = gen[b]
                            try:
                                vreme = danIucionica[b]
                                d = random.randint(0, vreme - 1)
                                pocetak[i] = d
                            except:
                                yyy = 5
                    except:
                        yyy=5
        return populacija,prilagodjenost
def procitaj():
    with open("data_timetable.txt") as f:
        contents = f.readlines()
    ucionice1=contents[0].split("rooms: ")
    ucionice2=ucionice1[1].split("\n")
    ucionice3=ucionice2[0].split(", ")
    m=len(radniDani)
    return ucionice3,m

def ispis(rezultat,najboljePocinjanje,ucionice,m):
    raspored=rezultat
    vreme=najboljePocinjanje[0]
    a=int(len(raspored)/m)
    print("Ponedeljak")
    for i in range(0,a,1):
        print(ucionice[i])
        if najboljePocinjanje[i]==None:
            print("U ovoj ucionici nema predavanja")
        else:
            sati=7+najboljePocinjanje[i]//60
            minuti=najboljePocinjanje[i]%60
            print("Predavanja krecu u "+str(sati)+" i "+str(minuti)+"minuta sa pauzama od po 15min")
            for j in raspored[i]:
                print(j[:-1],end=" minuta\n")
    print("Utorak")
    for i in range(len(ucionice), len(ucionice)+a, 1):
        print(ucionice[i-len(ucionice)])
        if najboljePocinjanje[i]==None:
            print("U ovoj ucionici nema predavanja")
        else:
            sati=7+najboljePocinjanje[i]//60
            minuti=najboljePocinjanje[i]%60
            print("Predavanja krecu u "+str(sati)+" i "+str(minuti)+"minuta sa pauzama od po 15min")
            for j in raspored[i]:
                print(j[:-1],end=" minuta\n")
    print("Sreda")
    for i in range(2*len(ucionice),2*len(ucionice)+ a, 1):
        print(ucionice[i-2*len(ucionice)])
        if najboljePocinjanje[i]==None:
            print("U ovoj ucionici nema predavanja")
        else:
            sati=7+najboljePocinjanje[i]//60
            minuti=najboljePocinjanje[i]%60
            print("Predavanja krecu u "+str(sati)+" i "+str(minuti)+"minuta sa pauzama od po 15min")
            for j in raspored[i]:
                print(j[:-1],end=" minuta\n")
    print("Cetvrtak")
    for i in range(3*len(ucionice),3*len(ucionice)+ a, 1):
        print(ucionice[i-3*len(ucionice)])
        if najboljePocinjanje[i]==None:
            print("U ovoj ucionici nema predavanja")
        else:
            sati=7+najboljePocinjanje[i]//60
            minuti=najboljePocinjanje[i]%60
            print("Predavanja krecu u "+str(sati)+" i "+str(minuti)+"minuta sa pauzama od po 15min")
            for j in raspored[i]:
                print(j[:-1],end=" minuta\n")
    print("Petak")
    for i in range(4*len(ucionice),4*len(ucionice)+ a, 1):
        print(ucionice[i-4*len(ucionice)])
        if najboljePocinjanje[i]==None:
            print("U ovoj ucionici nema predavanja")
        else:
            sati=7+najboljePocinjanje[i]//60
            minuti=najboljePocinjanje[i]%60
            print("Predavanja krecu u "+str(sati)+" i "+str(minuti)+"minuta sa pauzama od po 15min")
            for j in raspored[i]:
                print(j[:-1],end=" minuta\n")
if __name__=="__main__":
    ucionice,m=procitaj()
    genetski=GenetskiAlgoritam(ucionice,m)
    rezultat,najboljePocinjanje,najboljaOcena=genetski.optimizacija()
    ispis(rezultat,najboljePocinjanje,ucionice,m)