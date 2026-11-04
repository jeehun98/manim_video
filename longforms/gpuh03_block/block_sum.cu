#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
static void check(cudaError_t e){if(e!=cudaSuccess){std::fprintf(stderr,"%s\n",cudaGetErrorString(e));std::exit(1);}}
__global__ void blockSum(const float* input,float* output){
    __shared__ float s[128];
    int t=threadIdx.x;
    s[t]=input[t];
    __syncthreads();
    for(int stride=64;stride>0;stride>>=1){
        if(t<stride){s[t]+=s[t+stride];}
        __syncthreads();
    }
    if(t==0){output[0]=s[0];}
}
// Debug companion: additional barriers protect snapshot reads from later writes.
// It checks algorithm states; it is not a hardware scheduling trace or benchmark.
__global__ void blockSumTrace(const float* input,float* trace){
    __shared__ float s[128];int t=threadIdx.x;
    s[t]=input[t];__syncthreads();
    trace[t]=s[t];__syncthreads();int stage=1;
    for(int stride=64;stride>0;stride>>=1){
        if(t<stride)s[t]+=s[t+stride];
        __syncthreads();trace[stage*128+t]=s[t];__syncthreads();++stage;
    }
}
int main(int argc,char** argv){
    float input[128],output=0,states[8*128],cpu[128];
    for(int t=0;t<128;++t)input[t]=cpu[t]=float(t+1);
    float *di,*doo,*ds;check(cudaMalloc(&di,sizeof(input)));check(cudaMalloc(&doo,sizeof(output)));check(cudaMalloc(&ds,sizeof(states)));
    check(cudaMemcpy(di,input,sizeof(input),cudaMemcpyHostToDevice));
    blockSum<<<1,128>>>(di,doo);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(&output,doo,sizeof(output),cudaMemcpyDeviceToHost));
    if(output!=8256)return 2;std::printf("PASS blockSum<<<1,128>>> output[0]=%.0f\n",output);
    blockSumTrace<<<1,128>>>(di,ds);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(states,ds,sizeof(states),cudaMemcpyDeviceToHost));
    for(int t=0;t<128;++t)if(states[t]!=input[t])return 3;
    for(int stage=1,stride=64;stride;stride>>=1,++stage){
        for(int t=0;t<stride;++t)cpu[t]+=cpu[t+stride];
        for(int t=0;t<128;++t)if(states[stage*128+t]!=cpu[t])return 4;
        std::printf("PASS stride=%d count=%d s[0]=%.0f; all 128 shared slots verified\n",stride,stride,states[stage*128]);
    }
    if(argc>1){
        std::ofstream f(argv[1]);if(!f)return 5;f<<"{\"output\":"<<output<<",\"total_threads\":128,\"stages\":[";
        for(int st=0;st<8;++st){if(st)f<<",";f<<"{\"stride\":";if(st==0)f<<"null";else f<<(128>>st);f<<",\"count\":"<<(128>>st)<<",\"values\":[";
            for(int t=0;t<128;++t){if(t)f<<",";f<<states[st*128+t];}f<<"]}";
        }f<<"]}";
    }
    check(cudaFree(di));check(cudaFree(doo));check(cudaFree(ds));
}
