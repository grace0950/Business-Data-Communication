#include <iostream>
#include <fstream>

using namespace std;

int main(){

	ofstream bigfile;
	bigfile.open ("bigfile.txt");

	for(int i=0; i<4000000; i++){
		bigfile << "dd " << i << endl;
	}

	bigfile.close();

}
