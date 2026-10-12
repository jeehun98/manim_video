# 수학 출처와 확인 범위

- Le Gall & Urrutia, Improved Rectangular Matrix Multiplication using Powers of the Coppersmith-Winograd Tensor: https://people.csail.mit.edu/virgi/6.890/papers/legallurrutia.pdf
- Alman & Vassilevska Williams, A Refined Laser Method and Faster Matrix Multiplication: https://theoretics.episciences.org/14213/pdf
- Alman & Vassilevska Williams, Limits on All Known (and Some Unknown) Approaches to Matrix Multiplication: https://people.csail.mit.edu/virgi/matmultlimits.pdf

M_n=sum x_ij y_jk z_ik. Tensor product pairs all three indices; flatten (i,i') by n*i+i' (0-based). This identifies M_2⊗M_2 with M_4 on every coefficient, not only Kronecker-factorizable numeric inputs. k factors give M_(2^k).

General T=P+Q+S expands into 9 tensor products. This is an ordinary sum, not automatically a direct sum and not automatically matrix multiplication. The final toy restriction uses F=a1*b1*z1+a2*b2*z2+a1*b3*z2; b3=0 removes exactly the unwanted term and leaves two independent scalar multiplication tensors. It illustrates allowable variable restriction only; no general extraction count or complete laser proof is claimed.

z labels output coordinates formally. It is not another numeric multiplication in the algorithm. The 4×4 numeric example uses an arbitrary first row/column (1,2,3,4); result30.

## v2 편집 범위

도입·전환·결론의 비교는 보통 합과 독립 직합을 구별한다. 직합의 텐서곱은 분배되어 독립 변수 공간의 직합으로 남지만, 일반 부분합의 전개에는 그러한 독립성 보장이 없다. 모든 일반 텐서가 반드시 변수를 공유한다고 주장하지 않는다. v1의 마지막 b3=0 예제는 이번 영상에서 제외했다. 독립적인 행렬곱 추출의 구체적인 허용 변환은 다음 막에서 다룬다.
