#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
void check(cudaError_t e){if(e!=cudaSuccess){fprintf(stderr,"%s\n",cudaGetErrorString(e));exit(1);}}
__global__ void readArray(const float*A,float*B,int N){int i=blockIdx.x*blockDim.x+threadIdx.x;if(i<N){float x=A[i];B[i]=x*2.0f;}}
__global__ void readL2Policy(const float*A,float*B,int N){int i=blockIdx.x*blockDim.x+threadIdx.x;if(i<N){float x=__ldcg(&A[i]);B[i]=x*2.0f;}}
__global__ void sharedRead(const float*A,float*B){__shared__ float s[128];int t=threadIdx.x;int i=blockIdx.x*blockDim.x+t;s[t]=A[i];__syncthreads();B[i]=s[t]*2.0f;}
int main(int argc,char**argv){float a[256],b[256],*da,*db;for(int i=0;i<256;++i)a[i]=float(i+1);check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(b)));check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));
 std::ofstream f(argc>1?argv[1]:"cuda_trace.json");f<<"{\"N\":256,\"A5\":6,\"B5\":12,\"runs\":[";
 for(int k=0;k<3;++k){if(k==0)readArray<<<2,128>>>(da,db,256);if(k==1)readL2Policy<<<2,128>>>(da,db,256);if(k==2)sharedRead<<<2,128>>>(da,db);check(cudaGetLastError());check(cudaMemcpy(b,db,sizeof(b),cudaMemcpyDeviceToHost));for(int i=0;i<256;++i)if(b[i]!=2*a[i])return 2;const char*name=k==0?"readArray":k==1?"readL2Policy":"sharedRead";if(k)f<<",";f<<"{\"kernel\":\""<<name<<"\",\"count\":256,\"values\":[";for(int i=0;i<256;++i){if(i)f<<",";f<<b[i];}f<<"]}";printf("PASS %s all256 output values; A5=6 B5=12; no cache-hit measurement\n",name);}
 f<<"],\"measured_cache_hits\":false}";check(cudaFree(da));check(cudaFree(db));}
