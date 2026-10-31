#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
static void check(cudaError_t e){if(e!=cudaSuccess){std::fprintf(stderr,"%s\n",cudaGetErrorString(e));std::exit(1);}}
__global__ void neighborRead(const float* A,float* B){
    __shared__ float s[128];int t=threadIdx.x;s[t]=A[t];__syncthreads();B[t]=s[(t+1)%128];
}
__global__ void tiledGemm(const float* A,const float* B,float* C){
    const int N=4,T=2;__shared__ float As[T][T],Bs[T][T];
    int tx=threadIdx.x,ty=threadIdx.y,row=blockIdx.y*T+ty,col=blockIdx.x*T+tx;float sum=0;
    for(int m=0;m<N/T;++m){As[ty][tx]=A[row*N+m*T+tx];Bs[ty][tx]=B[(m*T+ty)*N+col];__syncthreads();
        for(int k=0;k<T;++k)sum+=As[ty][k]*Bs[k][tx];__syncthreads();}
    C[row*N+col]=sum;
}
__global__ void bankRead(float* output,int stride){
    __shared__ float s[1024];int t=threadIdx.x;for(int k=t;k<1024;k+=32)s[k]=float(k);__syncthreads();
    if(t<4)output[t]=s[t*stride];
}
int main(int argc,char**argv){
    float a[128],out[128];for(int t=0;t<128;++t)a[t]=float(100+t);
    float *da,*db;check(cudaMalloc(&da,sizeof(a)));check(cudaMalloc(&db,sizeof(out)));check(cudaMemcpy(da,a,sizeof(a),cudaMemcpyHostToDevice));
    neighborRead<<<1,128>>>(da,db);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(out,db,sizeof(out),cudaMemcpyDeviceToHost));
    for(int t=0;t<128;++t)if(out[t]!=a[(t+1)%128])return 2;
    std::printf("PASS neighborRead<<<1,128>>> all128; B[5]=%.0f B[6]=%.0f B[127]=%.0f\n",out[5],out[6],out[127]);
    check(cudaFree(da));check(cudaFree(db));
    float matrix[16],gemm[16];for(int i=0;i<16;++i)matrix[i]=float(i+1);float *ma,*mb,*mc;
    check(cudaMalloc(&ma,sizeof(matrix)));check(cudaMalloc(&mb,sizeof(matrix)));check(cudaMalloc(&mc,sizeof(gemm)));
    check(cudaMemcpy(ma,matrix,sizeof(matrix),cudaMemcpyHostToDevice));check(cudaMemcpy(mb,matrix,sizeof(matrix),cudaMemcpyHostToDevice));
    tiledGemm<<<dim3(2,2),dim3(2,2)>>>(ma,mb,mc);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(gemm,mc,sizeof(gemm),cudaMemcpyDeviceToHost));
    for(int r=0;r<4;++r)for(int c=0;c<4;++c){float v=0;for(int k=0;k<4;++k)v+=matrix[r*4+k]*matrix[k*4+c];if(gemm[r*4+c]!=v)return 3;}
    std::printf("PASS separate tiledGemm N4/T2 all16; selected %.0f %.0f %.0f %.0f\n",gemm[0],gemm[1],gemm[4],gemm[5]);
    check(cudaFree(ma));check(cudaFree(mb));check(cudaFree(mc));float *bo;check(cudaMalloc(&bo,4*sizeof(float)));
    for(int stride: {1,32,0}){float result[4];bankRead<<<1,32>>>(bo,stride);check(cudaGetLastError());check(cudaDeviceSynchronize());check(cudaMemcpy(result,bo,sizeof(result),cudaMemcpyDeviceToHost));
        for(int t=0;t<4;++t)if(result[t]!=float(t*stride))return 4;
        std::printf("PASS bankRead active4lanes stride%d: %.0f %.0f %.0f %.0f; no timing claim\n",stride,result[0],result[1],result[2],result[3]);}
    check(cudaFree(bo));
    if(argc>1){std::ofstream f(argv[1]);f<<"{\"neighbor\":[";for(int t=0;t<128;++t){if(t)f<<",";f<<out[t];}f<<"],\"gemm\":[";for(int i=0;i<16;++i){if(i)f<<",";f<<gemm[i];}f<<"],\"bank_strides\":[1,32,0],\"bank_count\":32,\"active_lanes\":4}";}
    std::puts("Unsafe read animation is a conceptual hazard, not an executed race. Arrival order, capacity and bank service steps are illustrative, not hardware traces.");
}
