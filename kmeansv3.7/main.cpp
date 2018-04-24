#include <cstdlib>
#include <iostream>
#include <random>
#include <string>
#include <vector>
#include <sstream>
#include <limits>
#include <ctime>
#include <cmath>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <typeinfo>
#include <chrono>
#include <time.h>
using namespace std;

const vector<string> explode(const string& s, const char& c)
{
	string buff{""};
	vector<string> v;
	
	for(auto n:s)
	{
		if(n != c) buff+=n; else
		if(n == c && buff != "") { v.push_back(buff); buff = ""; }
	}
	if(buff != "") v.push_back(buff);
	
	return v;
}


void centroideCreator(int k,vector<std::string> &centroidesVector,vector<std::string> &vectorData);
void coseno(double* pangulosAcumulados,int k,vector<std::string> &centroidesVector,vector<std::string> &vectorData,vector<vector<std::string>>  &clusters);
void minimo(double* mini,vector<double> &num);
void recalcularCentroide(vector<std::string>  &centroidesVector,vector<vector<std::string>>  &clusters);

int main(int argc, char *argv[]) {
    vector<std::string>  miVector;
    vector<std::string>  centroidesVector;
    vector<vector<std::string>>  clusters;
    int k = 1;
    k = stoi(argv[1]);
    double angulosAcumulados = 0;
    double angulosAcumuladosAfter = 0;
    double* pangulosAcumulados = NULL;
    pangulosAcumulados = &angulosAcumulados;
    int iter = 0;
    
    ifstream myfile("dataCombinadoCalificacion.txt");
    ofstream salidaErrorCuadratico;
    salidaErrorCuadratico.open ("salidaErrorCuadratico.txt");
    std::string line;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
             miVector.push_back(line);
        }
        myfile.close();
     }
    cout << "\n";
    
    centroideCreator(k,centroidesVector,miVector);
    /*cout << "Centroides" << "\n";    
    for(auto y: centroidesVector){
        cout << y << "\n";
    }*/
    
    /*
    cout << "DataSheet" << "\n";  
    for(auto y: miVector){
       cout << y << "\n";
    }*/
    
    
    
    cout << "llamada funcion numerador" << "\n\n";
    clock_t clkStart;
    clock_t clkFinish;
    clkStart = clock();
    while(true){
        cout << "Iteracion: " << iter <<endl;
        coseno(pangulosAcumulados,k,centroidesVector,miVector,clusters);
        if(iter == 0){
            angulosAcumuladosAfter = angulosAcumulados;            
        }else if ((angulosAcumuladosAfter-angulosAcumulados) == 0){
            break;    
        }else if (angulosAcumuladosAfter-angulosAcumulados < 0){
            break;    
        }
        angulosAcumuladosAfter = angulosAcumulados;        
            
                
        recalcularCentroide(centroidesVector,clusters);
        clusters.clear();
        iter+=1;
        
    }
    clkFinish = clock();
    cout << clkFinish - clkStart;
    salidaErrorCuadratico << angulosAcumuladosAfter;
    salidaErrorCuadratico.close();
    cout << endl << endl << endl;
    return 0;
}



void centroideCreator(int k,vector<std::string> &centroidesVector,vector<std::string> &vectorData){
    for (int i = 0; i < k; i++) {
        centroidesVector.push_back(vectorData[i]);        
    }
}


void coseno(double* pangulosAcumulados,int k,vector<std::string> &centroidesVector,vector<std::string> &vectorData,vector<vector<std::string>>  &clusters) {
    vector<std::string>  numeradorVectorU;
    vector<std::string>  numeradorVectorV;
    vector<std::string> inicializador;
    vector<std::string> usuarioInfo;
    vector<std::string> usuarioInfoTMP;
       
    std::string numberU;
    std::string numberU2;
    std::string numberV;
    std::string numberV2;
    std::string workingLine;    
    
    double dnumberU = 0;
    double dnumberU2 = 0;
    double dnumberV = 0;
    double dnumberV2 = 0;
    double numeradorSum = 0;
    double denominadorU = 0;
    double denominadorV = 0;
    double denominadorTotal = 0;
    double distancia = 0;
    double angulo = 0;
    double angulosAcumuladosSalida = 0;
    double angulosAcumuladosDivisor = 0;
    double anguloMasCorto[2];
    vector<double> denominadoresV;
    vector<double> angulosVector;    
    bool switchDenominadorU = true;  
    
    /*INICIO INICIALIZANDO clusterVector*/
    inicializador.push_back("");
    for (int i = 0; i < k; i++) {
        clusters.push_back(inicializador);
    }
    /*FIN    INICIALIZANDO clusterVector*/
    
    /*INICIO CALCULANDO NORMAS DE LOS CENTROIDES*/
    for(int x = 0; x < centroidesVector.size(); x++){
        workingLine = centroidesVector[x];
        vector<string> workingLineVetor{explode(workingLine, ' ')};
        for (int i = 2; i < workingLineVetor.size(); i += 2) {
            /*cout << workingLineVetor[i] << " ";*/
            dnumberV2 = stod(workingLineVetor[i]);
            denominadorV += pow(dnumberV2, 2);
        }
        /*cout << "DenominadorV sin sacarle raiz: " << denominadorV << "\n";*/
        denominadorV = sqrt(denominadorV);                
        denominadoresV.push_back(denominadorV);
        denominadorV = 0;        
    }
    /*cout << "\n";*/
    
    /*cout << "#################VECTOR denominadoresV##################" << "\n";
    for(auto y:denominadoresV){
        cout << y << " ";
    }*/
    /*cout << "\n\n";*/
    /*FIN CALCULANDO NORMAS DE LOS CENTROIDES*/
    
    /*INICIO CALCULANDO COSENO*/
    /*cout << "INICIO CALCULANDO COSENO" << "\n";*/
    
    for(int x = 0; x < vectorData.size(); x++){
        usuarioInfo.push_back(vectorData[x]); 
        /*cout << "IMPRESION USUARIO: " << vectorData[x] << "\n";*/        
        for(int y = 0; y < centroidesVector.size(); y++){
            /*cout << "numU, Iteracion centroide: "<< y << "\n";*/
            /*INICIO CALCULO NUMERADOR Y NORMA U*/
            string workingLineU = vectorData[x];
            vector<string> workingLineVetorU{explode(workingLineU, ' ')};
            for(int i = 2; i < workingLineVetorU.size(); i+=2){
                /*cout << "U: " << workingLineVetorU[i-1] << " " << workingLineVetorU[i] << "\n";*/
                dnumberU = stod(workingLineVetorU[i]);
                dnumberU2 = stod(workingLineVetorU[i-1]);
                if (switchDenominadorU) {
                    denominadorU += pow(dnumberU, 2);
                }
                /*INICIO CALCULO DENOMINADOR Y NORMA V*/
                string workingLineV = vectorData[y];
                vector<string> workingLineVetorV{explode(workingLineV, ' ')};
                for (int i = 2; i < workingLineVetorV.size(); i += 2) {
                    /*cout << "V: " << workingLineVetorV[i - 1] << " " << workingLineVetorV[i] << "\n";*/
                    dnumberV = stod(workingLineVetorV[i]);
                    dnumberV2 = stod(workingLineVetorV[i-1]);
                    if(dnumberU2 == dnumberV2){
                        /*cout << "Numerador " << dnumberU*dnumberV << "\n";*/
                        numeradorSum += dnumberU*dnumberV;
                        break;
                    }
                
                }                
                /*FIN    CALCULO DENOMINADOR Y NORMA V*/
            } 
            /*cout << "Numerador Sum: " << numeradorSum << "\n";*/
            if (switchDenominadorU) {
                denominadorU = sqrt(denominadorU);
            }
            /*cout << "DenominadorU: " << denominadorU << "\n";*/
            /*cout << "DenominadorV: " << denominadoresV[y] << "\n";*/
            switchDenominadorU = false;
            
            /*INICIO norma|U| * norma|V|  */
            denominadorTotal = denominadorU * denominadoresV[y];
            /*cout << "IMPRESION denominadorU*denominadoresV[y] " << denominadorTotal << "\n";*/
            /*FIN    norma|U| * norma|V|  */
            
            /*INICIO ( numeradorSum/denominadorTotal )  */
            distancia = numeradorSum / denominadorTotal;
            /*cout << "IMPRESION numeradorSum/denominadorTotal " << distancia << "\n";*/
            /*FIN    ( numeradorSum/denominadorTotal )  */
            
            /*INICIO  acos(distancia) */
            if (distancia > 0.98) {
                distancia = 1.0;
            }
            angulo = acos(distancia);            
            /*cout << "IMPRESION acos(distancia) Akka Angulo " << angulo << "\n";            */
            /*FIN     acos(distancia) */
            
            /*INICIO push_back al vector angulosVector  */
            angulosVector.push_back(angulo);
            /*FIN    push_back al vector angulosVector  */
            
            numeradorSum = 0;
            /*FIN    CALCULO NUMERADOR Y NORMA U*/                
            /*cout << "\n";*/
        }
        /*INICIO Seleccion angulo mas corto  */
        minimo(anguloMasCorto, angulosVector);
       /* cout << "Los angulos son: " << "\n";
        for (auto y : angulosVector) {
            cout << y << "\n";
        }*/
        /*cout << "El angulo mas corto es " << anguloMasCorto[0] << "\n";*/
        /*cout << "El index del angulo mas corto es " << anguloMasCorto[1] << "\n";*/
        *pangulosAcumulados += anguloMasCorto[0];
        angulosAcumuladosDivisor += 1;
        /*cout << "IMPRESION angulosAcumulados: " << angulosAcumulados << "\n\n";*/
        /*FIN    Seleccion angulo mas corto  */
        
        
        /*INICIO agregando usuario al cluster  */
        clusters[anguloMasCorto[1]].push_back(usuarioInfo[0]);        
        /*FIN    agregando usuario al cluster  */               
        
        usuarioInfo.clear();
        angulosVector.clear();             
        denominadorU = 0;
        switchDenominadorU = true;
    }   
       
    
    cout << "Suma del error cuadratico: " << *pangulosAcumulados / angulosAcumuladosDivisor << "\n";
    angulosAcumuladosSalida = *pangulosAcumulados/angulosAcumuladosDivisor;
    *pangulosAcumulados = 0;
    /*cout << "LOS CLUSTERS SON: " << "\n";
    for (int i = 0; i < clusters.size(); i++) {
        cout << "Cluster: " << i << "\n";
        cout << "------------------";
        for (int j = 0; j < clusters[i].size(); j++) {
            string workingLineRC = clusters[i][j];
            vector<string> workingLineVectorRC{explode(workingLineRC, ' ')};
            for (int k = 0; k < workingLineVectorRC.size(); k++) {
                cout << workingLineVectorRC[k];
            }cout << "\n";
            
        }cout << "\n";        
    }*/
    *pangulosAcumulados = angulosAcumuladosSalida;
}

 /*FIN    CALCULANDO COSENO*/

void recalcularCentroide(vector<std::string>  &centroidesVector,vector<vector<std::string>> &clusters) {
    /*cout << "CENTROIDES:  " << endl;
    for (auto y : centroidesVector) {
        cout << y << "\n";
    }*/
    int DivisorVector[4490];
    int index = 0;
    double clusterNumber = 0;
    double centroideNumber = 0;
    double suma = 0;
    double divisionNumber = 0;
    
    /*workingLineVectorRC es el cluster*/
    /*workingLineVectorRC2 es el centroide*/
    for (int i = 0; i < clusters.size(); i++) {
        /*cout << "Cluster: " << i << "\n";
        cout << "------------------";*/
        for (int j = 0; j < clusters[i].size(); j++) {
            string workingLineRC = clusters[i][j];
            vector<string> workingLineVectorRC{explode(workingLineRC, ' ')};
            for (int k = 1; k < workingLineVectorRC.size(); k+=2) {
                string workingLineRC2 = centroidesVector[i];
                vector<string> workingLineVectorRC2{explode(workingLineRC2, ' ')};
                for(int z = 1; z < workingLineVectorRC2.size(); z+=2){
                   /* cout << "cluster: " << workingLineVectorRC[k] << " centroide " << workingLineVectorRC2[z] << endl;*/
                    if(workingLineVectorRC[k] == workingLineVectorRC2[z]){
                        /*cout << "son iguales" << "\n";*/
                        workingLineVectorRC2[z+1] = '0';                        
                        break;
                    }
                }
                string tmp;
                for(int q = 0; q <workingLineVectorRC2.size();q++){
                    tmp.append(workingLineVectorRC2[q]);
                    tmp.append(" ");
                }
                centroidesVector[i] = tmp;
                tmp = "";
                /*cout << endl;*/
            }/*cout << "\n";*/
            
        }/*cout << "\n";        */
    }
    
    
    for (int i = 0; i < clusters.size(); i++) {
        /*cout << "Cluster: " << i << "\n";
        cout << "------------------\n";        */
        for (int j = 0; j<clusters[i].size();j++) {
            /*cout << clusters[i][j] << endl;*/
            string workingLineRC = clusters[i][j];
            vector<string> workingLineVectorRC{explode(workingLineRC, ' ')};
            for(int k = 1;k<workingLineVectorRC.size();k+=2){
                /*cout << "workingLineVectorRC[k] " << workingLineVectorRC[k]<<endl;*/
                string workingLineRC2 = centroidesVector[i];
                vector<string> workingLineVectorRC2{explode(workingLineRC2, ' ')};
                for (int z = 1; z < workingLineVectorRC2.size(); z+=2) {
                    /*cout << workingLineVectorRC2[z];*/
                    if (workingLineVectorRC[k] == workingLineVectorRC2[z]) {
                        clusterNumber = stod(workingLineVectorRC[k+1]);
                        centroideNumber = stod(workingLineVectorRC2[z+1]);
                        suma = clusterNumber + centroideNumber;                        
                        workingLineVectorRC2[z+1] = to_string(suma);
                        DivisorVector[stoi(workingLineVectorRC2[z])] += 1;
                        /*cout << endl << "workingLineVectorRC2[z]: " << workingLineVectorRC2[z] << endl;*/
                        break;
                    }
                } /*cout << endl;                */
                
                string tmp;
                for (int q = 0; q < workingLineVectorRC2.size(); q++) {
                    tmp.append(workingLineVectorRC2[q]);
                    tmp.append(" ");
                }
                centroidesVector[i] = tmp;
                tmp = "";
            }
            /*cout << endl;*/

        
        }/*cout << endl;*/
        string workingLineRC3 = centroidesVector[i];
        vector<string> workingLineVectorRC3{explode(workingLineRC3, ' ')};
        for(int g = 1;g < workingLineVectorRC3.size();g+=2){
            /*cout << workingLineVectorRC3[g] << endl;*/
            index = stoi(workingLineVectorRC3[g]);
            divisionNumber = stod(workingLineVectorRC3[g+1])/DivisorVector[index];
            /*cout << "DivisionNumber: " << divisionNumber << endl;*/
            workingLineVectorRC3[g+1] = to_string(divisionNumber);
        }
        
        string tmp;
        for (int q = 0; q < workingLineVectorRC3.size(); q++) {
            tmp.append(workingLineVectorRC3[q]);
            tmp.append(" ");
        }
        centroidesVector[i] = tmp;
        tmp = "";
        fill_n(DivisorVector, 4490, 0);

    }
    
    /*
    cout << "CENTROIDES RECALCULADOS " << endl;
    for(auto y:centroidesVector){
        cout << y << "\n";
    }*/

}


void minimo(double* mini,vector<double> &num){
  double min = 0;
  double index = 0;
  min = 2;
  for(double i = 0; i < num.size(); i++){    
    if (num[i] < min){
      min = num[i];
      index = i;
    }
  }
  mini[0] = min;
  mini[1] = index;
}

    


