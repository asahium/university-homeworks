#include <fstream>

int main() {
    const double f[12] = {12,5,10,9,0,2, 8, 4, 3, 6, 7, 11};

    std::ofstream ofile("in.bin", std::ios::binary);

    for (const double & i : f)
        ofile.write((char*) &i, sizeof(double));
}