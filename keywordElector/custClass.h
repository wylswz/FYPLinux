#ifndef CUSTCLASS_H_INCLUDED
#define CUSTCLASS_H_INCLUDED
#endif // CUSTCLASS_H_INCLUDED

#include <string>
#include <iostream>
using namespace std;
class word
{
  private:

   float TF_IDF;

  public:
   void setTF_IDF(float tf_idf)
   {
     TF_IDF = tf_idf;
   }


   word()
   {
      TF_IDF = 0;
      content = "";
   }

   ~word()
   {

   }
   void disp()
   {
      cout<<"word: "<<content<<endl;
      cout<<"TF_IDF: "<<TF_IDF<<endl;
   }
  string content;
  int ANO;  //the NO. of article
};
