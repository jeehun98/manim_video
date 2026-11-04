#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
static void check(cudaError_t e){if(e!=cudaSuccess){std::fprintf(stderr,"%s\n",cudaGetErrorString(e));std::exit(1);}}
__global__ void compute(const float* A,float* B,int N){
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i<N){float x=A[i];float y=x*2.0f;B[i]=y;}
}
int main(){
    const int N=1003;float a[N],b[N];for(int i=0;i<N;++i)a[i]=float(i-500)*.25f;
    float *da,*db;check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(b)));
    check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));
    int blockSize=128,gridSize=(N+blockSize-1)/blockSize;
    compute<<<gridSize,blockSize>>>(da,db,N);check(cudaGetLastError());check(cudaDeviceSynchronize());
    check(cudaMemcpy(b,db,sizeof(b),cudaMemcpyDeviceToHost));
    for(int i=0;i<N;++i)if(b[i]!=2*a[i])return 2;
    cudaDeviceProp p;check(cudaGetDeviceProperties(&p,0));cudaFuncAttributes f;check(cudaFuncGetAttributes(&f,compute));
    int blocks;check(cudaOccupancyMaxActiveBlocksPerMultiprocessor(&blocks,compute,128,0));
    std::printf("PASS all %d outputs equal A[i]*2; launch %d blocks x %d threads\n",N,gridSize,blockSize);
    std::printf("GPU: %s; SM count %d; kernel registers/thread %d; static shared %zu bytes\n",p.name,p.multiProcessorCount,f.numRegs,f.sharedSizeBytes);
    std::printf("API theoretical active blocks/SM %d; warps %d; max warps %d; occupancy %.3f\n",blocks,blocks*4,p.maxThreadsPerMultiProcessor/32,float(blocks*128)/p.maxThreadsPerMultiProcessor);
    std::puts("Animation uses a fictional 32-warp SM and illustrative issue order, not these device limits or a measured schedule.");
    check(cudaFree(da));check(cudaFree(db));
}
