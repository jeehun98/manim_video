#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
static void check(cudaError_t e) {
    if (e != cudaSuccess) { std::fprintf(stderr, "%s\n", cudaGetErrorString(e)); std::exit(1); }
}
__global__ void vectorAdd(const float* A, const float* B, float* C, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float a = A[i];
        float b = B[i];
        float sum = a + b;
        C[i] = sum;
    }
}
__global__ void vectorAddLoop(const float* A, const float* B, float* C, int N) {
    // Demonstration contract: launched with exactly one block.
    int t = threadIdx.x;
    int S = blockDim.x;
    for (int j = t; j < N; j += S) C[j] = A[j] + B[j];
}
static void test(int n, bool loop) {
    float a[12], b[12], c[12];
    for(int i=0;i<n;++i) { a[i]=float(i+1); b[i]=float(10*(i+1)); }
    float *da,*db,*dc; size_t bytes=n*sizeof(float);
    check(cudaMalloc(&da,bytes)); check(cudaMalloc(&db,bytes)); check(cudaMalloc(&dc,bytes));
    check(cudaMemcpy(da,a,bytes,cudaMemcpyHostToDevice)); check(cudaMemcpy(db,b,bytes,cudaMemcpyHostToDevice));
    if(loop) vectorAddLoop<<<1,4>>>(da,db,dc,n);
    else vectorAdd<<<(n+3)/4,4>>>(da,db,dc,n);
    check(cudaGetLastError()); check(cudaDeviceSynchronize());
    check(cudaMemcpy(c,dc,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<n;++i) { if(c[i]!=a[i]+b[i]) std::exit(2); std::printf("%g ",c[i]); }
    std::printf("PASS n=%d loop=%d\n",n,int(loop));
    check(cudaFree(da)); check(cudaFree(db)); check(cudaFree(dc));
}
int main() { test(4,false); test(7,false); test(12,true); }
