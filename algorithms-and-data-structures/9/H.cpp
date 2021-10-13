#include<iostream>
#include<vector>
#include<algorithm>
#include<cmath>
#include<iomanip>
using namespace std;

struct point{
  int x;
  int y;

  bool operator<(const point &p)const
   {
    return (x<p.x || (x==p.x && y<p.y));
   }
};

long long cross(point A, point B, point C)
   {
        return (B.x-A.x)*(C.y-A.y)-(B.y-A.y)*(C.x-A.x);
   }



vector<point> ConvexHull(vector<point> P) {
    vector<point> H; //hull
    H.resize(2 * P.size());
    int k=0;

    if (P.size()<3) return H;
    sort(P.begin(),P.end());

    for (int i = 0; i < P.size(); i++) {
        while(k >= 2 && cross(H[k-2],H[k-1],P[i])<=0)
            k--;
        H[k]=P[i];
        k++;
    }

    int t=k+1;

    for (int i=P.size()-2; i>=0 ;i--) {
        while (k >= t && cross(H[k-2], H[k-1],P[i])<=0)
            k--;
        H[k]=P[i];
        k++;
    }

    H.resize(k);
    return H;
};

double perimeter(vector<point> P) {
    double r=0;
    for (int i = 1; i < P.size(); i++)
        r+=sqrt(pow(P[i].x - P[i-1].x,2) + pow(P[i].y - P[i-1].y,2));
    return r;
}

double area(const std::vector<point> & fig) {
	double res = 0;
	for (int i = 0; i < fig.size(); ++i) {
		point p1 = i ? fig[i-1] : fig.back();
        point p2 = fig[i];
		res += (p1.x - p2.x) * (p1.y + p2.y);
	}
	return fabs (res) / 2;
}


int main() {
    int n;
    std::cin >> n;
    vector<point> P;
    P.resize(n);

    for(int i=0;i<n;i++)
        cin>>P[i].x>>P[i].y;

    vector<point> H;
    H = ConvexHull(P);

    cout << std::fixed << std::setprecision(10) << perimeter(H) << "\n";
    cout << std::fixed << std::setprecision(10) << area(H) << "\n";
    return 0;
}

