
#include <fstream>
#include <sstream>
#include <vector>
#include "custClass.h"
#include <algorithm>
#include <math.h>
using namespace std;


double TF_IDF_CAL(char *s,  int numOfDoc)  //calculate the TF_IDF value for string s
{
   double TF_IDF=0;
   const int nod = numOfDoc;
   double frequency[nod];
   double probability[nod];
   double sum=0;
   string tempString;
   string fileName;
   string readString;
   stringstream ssm;
   fstream fr;

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
          if(readString == s)
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
     probability[i] = (frequency[i]+1)/(sum+numOfDoc);
     TF_IDF += log(probability[i]);
    // cout << TF_IDF<< "/" << probability[i] << endl;
   }



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
    double tf_idf;
    vector<word> wordSet;
    vector<string> checked;
    vector<string>::iterator it;
    fstream configReader;
    fstream textReader1;
    fstream textReader2;
    stringstream ssm;


    configReader.open("text/fconfig.config",ios::in); //read the config file
    configReader >> numOfDoc;
    configReader.close();

    for(docCounter=0;docCounter<numOfDoc;docCounter++)
    {
       ssm << docCounter;
       ssm >> tempString;
       fileName = "text/" + tempString;
       ssm.clear();
       ssm.str("");

       textReader1.open(&fileName[0],ios::in);
       while (textReader1>>content)
    {
          progress += 1;
          it = find(checked.begin(),checked.end(),content);
          if (it == checked.end())   //the word cannot be found in the checked list
          {
            tf_idf = TF_IDF_CAL(&content[0],numOfDoc);
      //    cout<<tf_idf<<endl;
      //    cout<<"aaa"<<endl;;
            if (tf_idf <= 25)
            {
              word* bufferWord = new word();
              checked.push_back(content);   //add this word to the checked list
              bufferWord->ANO = docCounter;
              bufferWord->content = content;
              bufferWord->setTF_IDF(tf_idf);
              wordSet.push_back(*bufferWord);
              bufferWord->disp();
              delete bufferWord;
            //  cout<<progress<<endl;
            }
          }
       }
       textReader1.close();
    }



    return 0;
}



