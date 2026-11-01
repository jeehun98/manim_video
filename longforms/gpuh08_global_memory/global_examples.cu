#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <set>
void check(cudaError_t e){if(e!=cudaSuccess){fprintf(stderr,"%s\n",cudaGetErrorString(e));exit(1);}}
__global__ void vectorAdd(const float*A,const float*B,float*C,int N){int i=blockIdx.x*blockDim.x+threadIdx.x;if(i<N){float a=A[i];float b=B[i];C[i]=a+b;}}
__global__ void patternRead(const float*A,float*O,int stride,bool reverse){int i=threadIdx.x;int j=reverse?31-i:i*stride;float x=A[j];O[i]=x;}
int main(int argc,char**argv){
 float a[256],b[256],out[256],*da,*db,*dc;for(int i=0;i<256;++i){a[i]=float(i+1);b[i]=float((i+1)*10);}
 check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(b)));check(cudaMalloc(&dc,sizeof(out)));check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));check(cudaMemcpy(db,b,sizeof(b),cudaMemcpyHostToDevice));
 if(reinterpret_cast<uintptr_t>(da)%32!=0)return 2;
 vectorAdd<<<2,128>>>(da,db,dc,256);check(cudaGetLastError());check(cudaMemcpy(out,dc,sizeof(out),cudaMemcpyDeviceToHost));for(int i=0;i<256;++i)if(out[i]!=a[i]+b[i])return 3;
 printf("PASS vectorAdd all256; C[5]=%.0f; cudaMalloc base aligned32B\n",out[5]);
 std::ofstream f(argc>1?argv[1]:"cuda_trace.json");f<<"{\"vector_count\":256,\"C5\":"<<out[5]<<",\"base_alignment\":32,\"patterns\":[";
 for(int p=0;p<3;++p){int stride=p==1?8:1;bool reverse=p==2;patternRead<<<1,32>>>(da,dc,stride,reverse);check(cudaGetLastError());check(cudaMemcpy(out,dc,32*sizeof(float),cudaMemcpyDeviceToHost));std::set<int> sectors;if(p)f<<",";f<<"{\"stride\":"<<stride<<",\"reverse\":"<<(reverse?"true":"false")<<",\"indices\":[";
 for(int i=0;i<32;++i){int j=reverse?31-i:i*stride;if(out[i]!=a[j])return 4;sectors.insert(j*4/32);if(i)f<<",";f<<j;}
 f<<"],\"values\":[";for(int i=0;i<32;++i){if(i)f<<",";f<<out[i];}f<<"],\"modeled_sectors\":"<<sectors.size()<<"}";
 printf("PASS pattern%d all32 output values; modeled sector count=%zu; no performance measurement\n",p,sectors.size());}
 f<<"],\"sector_bytes\":32,\"useful_bytes\":128,\"measured_traffic\":false}";check(cudaFree(da));check(cudaFree(db));check(cudaFree(dc));
}
