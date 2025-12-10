#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <omp.h>
#include <iomanip>
#include <fstream> // <-- Added for CSV file writing

using namespace std;

// -----------------------------------------------------------
// CONFIGURATION: Choose Data Type and Range
// -----------------------------------------------------------
bool USE_FLOATS = false;   // true → [0,1), false → integers [0,100000]

// -----------------------------------------------------------
// RANDOM ARRAY GENERATION
// -----------------------------------------------------------
template <typename T>
vector<T> generate_random_array(size_t n) {
    vector<T> arr(n);
    random_device rd;
    mt19937 gen(rd());

    if constexpr (is_floating_point<T>::value) {
        uniform_real_distribution<> dis(0.0, 1.0);
        for (size_t i = 0; i < n; ++i)
            arr[i] = dis(gen);
    } else {
        uniform_int_distribution<> dis(0, 100000);
        for (size_t i = 0; i < n; ++i)
            arr[i] = dis(gen);
    }

    return arr;
}

// -----------------------------------------------------------
// SEQUENTIAL CPU SORT
// -----------------------------------------------------------
template <typename T>
double cpu_sort(vector<T> arr) {
    auto start = chrono::high_resolution_clock::now();
    sort(arr.begin(), arr.end());
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    return elapsed.count();
}

// -----------------------------------------------------------
// PARALLEL SORT USING OpenMP (Simulated GPU)
// -----------------------------------------------------------
template <typename T>
double gpu_sort_openmp(vector<T> arr) {
    size_t n = arr.size();
    auto start = chrono::high_resolution_clock::now();

    #pragma omp parallel
    {
        int num_threads = omp_get_num_threads();
        int thread_id = omp_get_thread_num();
        size_t chunk = n / num_threads;
        size_t start_idx = thread_id * chunk;
        size_t end_idx = (thread_id == num_threads - 1) ? n : start_idx + chunk;
        sort(arr.begin() + start_idx, arr.begin() + end_idx);
    }

    inplace_merge(arr.begin(), arr.begin() + n / 2, arr.end());

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    return elapsed.count();
}

// -----------------------------------------------------------
// MAIN FUNCTION
// -----------------------------------------------------------
int main() {
    vector<size_t> sizes = {100000, 1000000, 10000000};

    // Choose output filename based on data type
    string filename = USE_FLOATS ? "sorting_results_float.csv" : "sorting_results_int.csv";
    ofstream file(filename);
    file << "ArraySize,CPUTime,OpenMPTime,Speedup\n";

    cout << fixed << setprecision(6);
    cout << "\nCPU vs GPU (OpenMP) Sorting Performance Comparison\n";
    cout << "-------------------------------------------------------------\n";
    cout << "Data Type: " << (USE_FLOATS ? "float [0,1)" : "int [0,100000]") << endl;
    cout << "Threads Used: " << omp_get_max_threads() << endl;
    cout << "-------------------------------------------------------------\n";
    cout << setw(12) << "Array Size"
         << setw(15) << "CPU Time (s)"
         << setw(20) << "OpenMP Time (s)"
         << setw(15) << "Speedup\n";
    cout << "-------------------------------------------------------------\n";

    if (USE_FLOATS) {
        for (auto size : sizes) {
            vector<float> arr = generate_random_array<float>(size);
            double cpu_time = cpu_sort(arr);
            double gpu_time = gpu_sort_openmp(arr);
            double speedup = cpu_time / gpu_time;
            cout << setw(12) << size
                 << setw(15) << cpu_time
                 << setw(20) << gpu_time
                 << setw(15) << speedup << "x\n";
            file << size << "," << cpu_time << "," << gpu_time << "," << speedup << "\n";
        }
    } else {
        for (auto size : sizes) {
            vector<int> arr = generate_random_array<int>(size);
            double cpu_time = cpu_sort(arr);
            double gpu_time = gpu_sort_openmp(arr);
            double speedup = cpu_time / gpu_time;
            cout << setw(12) << size
                 << setw(15) << cpu_time
                 << setw(20) << gpu_time
                 << setw(15) << speedup << "x\n";
            file << size << "," << cpu_time << "," << gpu_time << "," << speedup << "\n";
        }
    }

    file.close();
    cout << "-------------------------------------------------------------\n";
    cout << "Results saved to: " << filename << endl;
    cout << "Note: GPU timings use OpenMP parallel regions to emulate GPU parallelism.\n";
    cout << "-------------------------------------------------------------\n";

    return 0;
}
