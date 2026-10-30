#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
static void check(cudaError_t e) { if(e!=cudaSuccess) { std::fprintf(stderr,"%s\n",cudaGetErrorString(e)); std::exit(1); } }
__global__ void vectorAdd(const float* A,const float* B,float* C) {
    int i=threadIdx.x;
    C[i]=A[i]+B[i];
}
__global__ void branchExample(float* A) {
    int i=threadIdx.x;
    if(i<16) A[i]=A[i]*2.0f;
    else A[i]=A[i]+1.0f;
}
__global__ void uniformExample(float* A) {
    int i=threadIdx.x;
    if(i<32) A[i]*=2.0f;
}
__global__ void pathMembership(unsigned* masks) {
    int i=threadIdx.x;
    // All 32 threads call both collectives. These are predicate-membership masks,
    // not a trace of the compiler's actual instruction execution masks.
    unsigned mul=__ballot_sync(0xffffffffu,i<16);
    unsigned add=__ballot_sync(0xffffffffu,i>=16);
    if(i==0) { masks[0]=mul; masks[1]=add; }
}
__global__ void laneIndices(int* lanes) {
    int i=threadIdx.x;
    lanes[i]=i%32; // One-dimensional block: local index and lane differ at i >= 32.
}
int main() {
    float a[32],b[32],c[32];for(int i=0;i<32;++i){a[i]=float(i+1);b[i]=10*a[i];}
    float *da,*db,*dc;const size_t bytes=sizeof(a);
    check(cudaMalloc(&da,bytes));check(cudaMalloc(&db,bytes));check(cudaMalloc(&dc,bytes));
    check(cudaMemcpy(da,a,bytes,cudaMemcpyHostToDevice));check(cudaMemcpy(db,b,bytes,cudaMemcpyHostToDevice));
    vectorAdd<<<1,32>>>(da,db,dc);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(c,dc,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<32;++i)if(c[i]!=a[i]+b[i])return 2;
    std::printf("PASS vectorAdd 32 outputs; lanes 0,1,6,31: %g %g %g %g\n",c[0],c[1],c[6],c[31]);
    branchExample<<<1,32>>>(da);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(c,da,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<32;++i)if(c[i]!=(i<16?a[i]*2:a[i]+1))return 3;
    std::printf("PASS branchExample 32 outputs; lanes 0,15,16,31: %g %g %g %g\n",c[0],c[15],c[16],c[31]);
    check(cudaMemcpy(da,a,bytes,cudaMemcpyHostToDevice));uniformExample<<<1,32>>>(da);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(c,da,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<32;++i)if(c[i]!=2*a[i])return 4;
    std::puts("PASS uniformExample all 32 take the true path");
    unsigned *dm,mask[2];check(cudaMalloc(&dm,sizeof(mask)));pathMembership<<<1,32>>>(dm);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(mask,dm,sizeof(mask),cudaMemcpyDeviceToHost));
    if(mask[0]!=0x0000ffffu||mask[1]!=0xffff0000u)return 5;
    std::printf("PASS path membership masks: 0x%08X 0x%08X (not instruction trace)\n",mask[0],mask[1]);
    int* dl;int lanes[64];check(cudaMalloc(&dl,sizeof(lanes)));laneIndices<<<1,64>>>(dl);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(lanes,dl,sizeof(lanes),cudaMemcpyDeviceToHost));
    for(int i=0;i<64;++i)if(lanes[i]!=i%32)return 6;
    std::printf("PASS 1D lane indices: threadIdx.x=6 -> %d; threadIdx.x=38 -> %d\n",lanes[6],lanes[38]);
    check(cudaFree(da));check(cudaFree(db));check(cudaFree(dc));check(cudaFree(dm));check(cudaFree(dl));
}
