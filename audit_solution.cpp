#include <iostream>
using namespace std;

// meeras museum audit solver
int main() {
    // speed up IO
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    // using long long just in case registration numbers exceed 2^31 - 1
    // also doing O(1) memory to avoid vector overhead and potential TLE
    long long ans = 0;
    for(int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        ans ^= val;
    }

    cout << ans << "\n";

    return 0;
}

