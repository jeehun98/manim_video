#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
void check(cudaError_t e){if(e!=cudaSuccess){fprintf(stderr,"%s\n",cudaGetErrorString(e));exit(1);}}
__global__ void readData(const float*A,float*B,int N){int i=blockIdx.x*blockDim.x+threadIdx.x;if(i<N){float x=A[i];B[i]=x*2.0f;}}
int main(int argc,char**argv){float a[256],b[256],*da,*db;for(int i=0;i<256;++i)a[i]=float(i+1);check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(b)));check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));readData<<<2,128>>>(da,db,256);check(cudaGetLastError());check(cudaMemcpy(b,db,sizeof(b),cudaMemcpyDeviceToHost));for(int i=0;i<256;++i)if(b[i]!=2*a[i])return 2;printf("PASS readData all256; A5=6 B5=12; no cache/DRAM state or timing measured\n");std::ofstream f(argc>1?argv[1]:"cuda_trace.json");f<<"{\"N\":256,\"A5\":6,\"B5\":12,\"measured_dram_state\":false,\"values\":[";for(int i=0;i<256;++i){if(i)f<<",";f<<b[i];}f<<"]}";check(cudaFree(da));check(cudaFree(db));}
