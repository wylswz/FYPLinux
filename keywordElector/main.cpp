
#include <fstream>
#include <sstream>
#include <vector>
#include "custClass.h"
#include <algorithm>
#include <strings.h>
#include <math.h>
using namespace std;


double TF_IDF_CAL(char *s,  int numOfDoc)  //calculate the TF_IDF value for string s
{
   double TF_IDF=0;
   const int nod = 800;
   double frequency[nod];
   double probability[nod];
   double sum=0;
   string tempString;
   string fileName;
   string readString;
   stringstream ssm;
   fstream fr;
   char * readStringPtr;
   for(int i=0;i<nod;i++)
   {
     frequency[i] = 0;
   }

   for(int i=0;i<nod;i++)
   {
     ssm<<i;
     ssm>>tempString;
     ssm.clear();
     ssm.str("");
     fileName = "text/"+ tempString;
     fr.open(&fileName[0],ios::in);
       while (fr>>readString)
       {
          readStringPtr = &readString[0];
          if(/*!strcasecmp(readStringPtr,s)*/s == readString)

          {
            frequency[i] += 1;

          }
       }
     fr.close();
   }
   for(int i=0;i<nod;i++)
   {
     sum += frequency[i];
   }
   for(int i=0;i<nod;i++)
   {
     probability[i] = (frequency[i]+1)/(sum+nod);
     TF_IDF += probability[i]*log(probability[i])*(2/(1+exp(4-sum)));
    // cout << TF_IDF<< "/" << probability[i] << endl;
   }


   //cout<<TF_IDF;
   return -TF_IDF;
}



int main()
{

    string content;
    string test="asd";
    string fileName;
    string tempString;
    char* contentPtr;
    int artNum;
    int numOfDoc;
    int docCounter;
    int progress=0;
    int tempCounter = 0; //initialize before use!!!
    double tf_idf;
    vector<word> wordSet;
    vector<string> checked;
    vector<string>::iterator it;
    fstream configReader;
    fstream textReader1;
    fstream textReader2;
    fstream keyWordWritter;
    stringstream ssm;
    bool stringFound;//if a string is in checked
    
    configReader.open("text/fconfig.config",ios::in); //read the config file
    configReader >> numOfDoc;
    configReader.close();

    for(docCounter=0;docCounter<500;docCounter++)
    {
       ssm << docCounter;
       ssm >> tempString;
       fileName = "text/" + tempString;
       ssm.clear();
       ssm.str("");

       textReader1.open(&fileName[0],ios::in);
       while (textReader1>>content)
    {
          tempCounter = 0;//initialize the tempCounter
          progress += 1;
          for(int i=0;i<checked.size();i++)
          {
              if (!strcasecmp(&content[0],&checked[i][0]))
                 { 
                  tempCounter += 1;   //found
                 }
     
           }
           
          //if (it == checked.end())   //the word cannot be found in the checked list
          if (tempCounter==0)
          {
            tf_idf = 3; // TF_IDF_CAL(&content[0],numOfDoc);
      //    cout<<tf_idf<<endl;
            if (tf_idf < 100&&tf_idf >= 0&&content.length()>=3)
            {
              word* bufferWord = new word();
              bufferWord->ANO = docCounter;
              bufferWord->content = content;
              bufferWord->setTF_IDF(tf_idf);
              wordSet.push_back(*bufferWord);
              bufferWord->disp();
              delete bufferWord;
            }
          }
       
          checked.push_back(content);   //add this word to the checked list
       }
       textReader1.close();
    }
    keyWordWritter.open("text/key.txt",ios::out);
    for (int i=0;i<wordSet.size();i++)
    {
        keyWordWritter << wordSet[i].content << "\t";
    }
    keyWordWritter.close();


    return 0;
}



