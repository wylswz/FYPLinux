// MatrixGenerator.cpp : main project file.

#include "stdafx.h"
using namespace std;

int main(void)
{
    int test = 99;
	fstream textReader;
	fstream keyReader;
	fstream matrixWrite;
	fstream configReader;
	stringstream ssm;
	string scanner;
	string keyScanner;
	string key;
	string PATH;
	string fileNameS;
	string tempStr;
	vector<string> keyArray;
	vector<string> textArray;
	char* buffer;
	char* fileName;
	int textSize = 0;
	int keyLength = 0;
	int sourceLength = 0;
	int tempCounter = 0;
	int docIndex = 0;
	int wordIndex = 10;
	int numOfDoc = 0;
	int numOfWord = 0;
    int k = 0;
	int **matrix;


cout<<"asd";
    configReader.open("text/fconfig.config",ios::in); //read the config file
    configReader >> numOfDoc;
    configReader >> numOfWord;
    configReader.close();

	keyReader.open("text/key.txt", ios::in);  //count the number of keys
    if (keyReader.is_open() == 0)
	 {
		cout << "cannot open file key"<<endl;
	 }
    while (keyReader >> keyScanner)
	 {
	    //numOfWord += 1;
		keyArray.push_back(keyScanner);
	 }
	 keyReader.close();

     matrix = new int*[numOfDoc];
     for(int j=0;j<numOfDoc;j++)
     {
       matrix[j] = new int[numOfWord];
     }                              //initialize the matrix, based on the number of documents and keywords



	for (int i = 0; i < numOfDoc; i++)
	{
		for (int j = 0; j < numOfWord; j++)
		{
			matrix[i][j] = 0;
		}
	}









	//begin to count number of keys in the text



		int c1 = 0;
        k = 0;
		for (k = 0; k < numOfDoc; k++)
		{
			for (c1 = 0; c1 < numOfWord; c1++)
			{
				ssm << k + 1;
				ssm >> tempStr;
				fileNameS = "text/" + tempStr;
				cout << "Analyzing: " << fileNameS << endl;
				ssm.clear();
				ssm.str("");       //clear the stream
				fileName = &fileNameS[0];
				textReader.open(fileName, ios::in);
				tempCounter = 0;
				while (textReader >> scanner)
				{
					if (scanner.find(keyArray[c1], 0) != string::npos && scanner.length() - keyArray[c1].length() < 2)
					{
						tempCounter += 1;
					}

				}
                matrix[k][c1] = tempCounter;
				textReader.close();

			}
		}
	keyReader.close();
////////////////////////////////////////////////////////////////////////////////////////////////
	for (int i = 0; i < keyArray.size(); i++)
	{
		cout << "\t" << keyArray[i];
	}
	cout << endl;
	for (int i = 0; i < numOfDoc; i++)
	{
		cout << "a" << i+1<<"\t";
		for (int j = 0; j < numOfWord; j++)
		{
			cout  << matrix[i][j]<<"\t";
		}
		cout << endl;
	}

	cout <<"Writing Data......"<< endl;

	matrixWrite.open("matrix.txt", ios::out);
	for (int i = 0; i < numOfDoc; i++)
	{
		for (int j = 0; j < numOfWord; j++)
		{
			matrixWrite << matrix[i][j] << "\t";
		}
		matrixWrite << endl;
	}
	matrixWrite.close();
	cout <<"Complete!" << endl;
    return 0;
}
