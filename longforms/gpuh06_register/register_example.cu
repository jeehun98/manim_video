#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
static void check(cudaError_t e){if(e!=cudaSuccess){std::fprintf(stderr,"%s\n",cudaGetErrorString(e));std::exit(1);}}
__global__ void vectorAdd(const float* A,const float* B,float* C,int N){
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i<N){float a=A[i];float b=B[i];float sum=a+b;C[i]=sum;}
}
int main(int argc,char**argv){
    const int N=1536;float a[N],b[N],c[N];for(int i=0;i<N;++i){a[i]=float(i+1);b[i]=float(i+2);}
    float *da,*db,*dc;check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(b)));check(cudaMalloc(&dc,sizeof(c)));
    check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));check(cudaMemcpy(db,b,sizeof(b),cudaMemcpyHostToDevice));
    vectorAdd<<<12,128>>>(da,db,dc,N);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(c,dc,sizeof(c),cudaMemcpyDeviceToHost));
    for(int i=0;i<N;++i)if(c[i]!=a[i]+b[i])return 2;
    cudaFuncAttributes attr;check(cudaFuncGetAttributes(&attr,vectorAdd));
    std::printf("PASS all 1536 outputs; Thread 2: A[2]=%.0f B[2]=%.0f C[2]=%.0f\n",a[2],b[2],c[2]);
    std::printf("Actual compiled vectorAdd: %d registers/thread, %zu local bytes/thread\n",attr.numRegs,attr.localSizeBytes);
    if(argc>1){std::ofstream f(argv[1]);f<<"{\"N\":1536,\"registers_per_thread\":"<<attr.numRegs<<",\"local_bytes\":"<<attr.localSizeBytes<<",\"selected_thread\":2,\"a\":3,\"b\":4,\"sum\":7,\"outputs\":[";for(int i=0;i<N;++i){if(i)f<<",";f<<c[i];}f<<"]}";}
    check(cudaFree(da));check(cudaFree(db));check(cudaFree(dc));
}
