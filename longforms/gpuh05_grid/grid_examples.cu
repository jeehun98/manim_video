#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <fstream>
static void check(cudaError_t e){if(e!=cudaSuccess){std::fprintf(stderr,"%s\n",cudaGetErrorString(e));std::exit(1);}}
__global__ void vectorAdd(const float* A,const float* B,float* C,int N){
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i<N)C[i]=A[i]+B[i];
}
// Separate 2D example; not the 12x128 vectorAdd launch.
__global__ void imageKernel(const float* input,float* output,int width,int height){
    int x=blockIdx.x*blockDim.x+threadIdx.x;
    int y=blockIdx.y*blockDim.y+threadIdx.y;
    if(x<width && y<height)output[y*width+x]=input[y*width+x]+1.0f;
}
int main(int argc,char**argv){
    const int N=1536;std::vector<float>a(N),b(N),c(N),orderA(N),orderB(N);
    for(int i=0;i<N;++i){a[i]=float(i);b[i]=float(i*10+1);}
    float *da,*db,*dc;check(cudaMalloc(&da,N*sizeof(float)));check(cudaMalloc(&db,N*sizeof(float)));check(cudaMalloc(&dc,N*sizeof(float)));
    check(cudaMemcpy(da,a.data(),N*sizeof(float),cudaMemcpyHostToDevice));check(cudaMemcpy(db,b.data(),N*sizeof(float),cudaMemcpyHostToDevice));
    int blockSize=128,gridSize=12;
    vectorAdd<<<gridSize,blockSize>>>(da,db,dc,N);check(cudaGetLastError());check(cudaDeviceSynchronize());
    check(cudaMemcpy(c.data(),dc,N*sizeof(float),cudaMemcpyDeviceToHost));
    for(int i=0;i<N;++i)if(c[i]!=a[i]+b[i])return 2;
    const int oa[12]={7,2,9,5,0,8,3,11,4,1,10,6},ob[12]={5,2,8,0,11,1,9,4,10,3,6,7};
    for(int block:oa)for(int t=0;t<128;++t){int i=block*128+t;orderA[i]=a[i]+b[i];}
    for(int block:ob)for(int t=0;t<128;++t){int i=block*128+t;orderB[i]=a[i]+b[i];}
    for(int i=0;i<N;++i)if(orderA[i]!=c[i] || orderB[i]!=c[i])return 3;
    std::printf("PASS vectorAdd<<<12,128>>>: all 1536 outputs; C[5]=%.0f; C[133]=%.0f\n",c[5],c[133]);
    std::puts("PASS two CPU block-order permutations agree with GPU output; independent output ranges, not a measured GPU issue order.");
    check(cudaFree(da));check(cudaFree(db));check(cudaFree(dc));
    for(int test=0;test<2;++test){
        int width=test==0?80:77,height=test==0?64:61;std::vector<float>input(width*height),output(width*height);
        for(int i=0;i<width*height;++i)input[i]=float(i);
        float *di,*doo;check(cudaMalloc(&di,input.size()*sizeof(float)));check(cudaMalloc(&doo,output.size()*sizeof(float)));
        check(cudaMemcpy(di,input.data(),input.size()*sizeof(float),cudaMemcpyHostToDevice));
        dim3 block(16,16);dim3 grid((width+15)/16,(height+15)/16);
        imageKernel<<<grid,block>>>(di,doo,width,height);check(cudaGetLastError());check(cudaDeviceSynchronize());
        check(cudaMemcpy(output.data(),doo,output.size()*sizeof(float),cudaMemcpyDeviceToHost));
        for(int i=0;i<width*height;++i)if(output[i]!=input[i]+1)return 4;
        std::printf("PASS separate imageKernel: image %dx%d, grid %dx%d, block 16x16, all %zu pixels\n",width,height,grid.x,grid.y,output.size());
        check(cudaFree(di));check(cudaFree(doo));
    }
    if(argc>1){
        std::ofstream f(argv[1]);f<<"{\"N\":1536,\"grid\":12,\"block\":128,\"C\":[";
        for(int i=0;i<N;++i){if(i)f<<",";f<<c[i];}f<<"],\"image\":{\"width\":80,\"height\":64,\"grid\":[5,4],\"block\":[16,16],\"selected_tile\":[2,1],\"x_range\":[32,47],\"y_range\":[16,31]}}";
    }
    std::puts("Animation: fictional 4-SM resource example; placement, completion timing, and resident capacity are not measured device traces.");
}
