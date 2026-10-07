import argparse, os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EPISODES = {"20": ("episodes/20_softmax_attention_finale/scene.py", "SoftmaxAttentionFinale"), "19": ("episodes/19_softmax_entropy/scene.py", "SoftmaxEntropy"), "18": ("episodes/18_softmax_lse/scene.py", "SoftmaxLSE"), "17": ("episodes/17_softmax_sigmoid/scene.py", "SoftmaxSigmoid"), "16": ("episodes/16_softmax_jacobian/scene.py", "SoftmaxJacobian"), "15": ("episodes/15_softmax_temperature/scene.py", "SoftmaxTemperature"), "14": ("episodes/14_softmax_ratio/scene.py", "SoftmaxRatio"), "13": ("episodes/13_softmax_shift/scene.py", "SoftmaxShift"), "12": ("episodes/12_softmax_intro/scene.py", "SoftmaxIntroduction"), "11": ("episodes/11_sigmoid_finale/scene.py", "SigmoidFinale"), "10": ("episodes/10_sigmoid_cdf/scene.py", "SigmoidCDF"), "09": ("episodes/09_sigmoid_distribution/scene.py", "SigmoidDistribution"), "08": ("episodes/08_sigmoid_saturation/scene.py", "SigmoidSaturation"), "07": ("episodes/07_sigmoid_derivative/scene.py", "SigmoidDerivative"), "06": ("episodes/06_sigmoid_intro/scene.py", "SigmoidIntroduction"), "05": ("episodes/05_computation_simplification/scene.py", "ComputationSimplification"), "04": ("episodes/04_irreversibility/scene.py", "Irreversibility"), "03": ("episodes/03_relu_change_magnitude/scene.py", "ReLUChangeMagnitude"), "01": ("episodes/01_relu/scene.py", "ReLUIntroduction"), "02": ("episodes/02_relu_information_loss/scene.py", "ReLUInformationLoss"), "legacy": ("archive/relu_short.py", "ReLUShort")}
EPISODES["gpu01"] = ("episodes/gpu01_formula_to_gpu/scene.py", "FormulaToGPU")
EPISODES["gpu02"] = ("episodes/gpu02_warp/scene.py", "WarpIntroduction")
EPISODES["gpu03"] = ("episodes/gpu03_memory_access/scene.py", "MemoryAccessIntroduction")

EPISODES["gpu04"] = ("episodes/gpu04_memory_spaces/scene.py", "MemorySpacesIntroduction")

EPISODES["gpu05"] = ("episodes/gpu05_naive_gemm/scene.py", "NaiveGEMMIntroduction")

EPISODES["gpu06"] = ("episodes/gpu06_tiled_gemm/scene.py", "TiledGEMMIntroduction")

EPISODES["gpu07"] = ("episodes/gpu07_tile_size/scene.py", "TileSizeIntroduction")

EPISODES["gpu08"] = ("episodes/gpu08_register_occupancy/scene.py", "RegisterOccupancyIntroduction")

EPISODES["gpu09"] = ("episodes/gpu09_bank_conflict/scene.py", "BankConflictIntroduction")
EPISODES["la01"] = ("episodes/la01_matrix_relations/scene.py", "MatrixRelations")
EPISODES["la02"] = ("episodes/la02_matrix_vector_product/scene.py", "MatrixVectorProduct")
EPISODES["la03"] = ("episodes/la03_matrix_paths/scene.py", "MatrixPaths")
EPISODES["la04"] = ("episodes/la04_repeated_patterns/scene.py", "RepeatedPatterns")
EPISODES["la05"] = ("episodes/la05_pattern_filter/scene.py", "PatternFilter")
EPISODES["la06"] = ("episodes/la06_nullspace/scene.py", "Nullspace")
EPISODES["la07"] = ("episodes/la07_independence/scene.py", "Independence")
EPISODES["la08"] = ("episodes/la08_rank/scene.py", "Rank")
EPISODES["la09"] = ("episodes/la09_rank_factorization/scene.py", "RankFactorization")

EPISODES["la10"] = ("episodes/la10_svd_channels/scene.py", "SVDChannels")

EPISODES["svd01"] = ("episodes/svd01_optimal_forgetting/scene.py", "SVD01")
EPISODES["svd02"] = ("episodes/svd02_difference_survival/scene.py", "SVD02")
EPISODES["svd03"] = ("episodes/svd03_sensitivity_map/scene.py", "SVD03")
EPISODES["svd04"] = ("episodes/svd04_independent_questions/scene.py", "SVD04")
EPISODES["svd05"] = ("episodes/svd05_ellipse_extrema/scene.py", "SVD05")
EPISODES["svd06"] = ("episodes/svd06_condition_number/scene.py", "SVD06ConditionNumber")
EPISODES["svd07"] = ("episodes/svd07_inverse_error/scene.py", "SVD07InverseError")
EPISODES["svd08"] = ("episodes/svd08_near_parallel_lines/scene.py", "SVD08NearParallelLines")
EPISODES["svd09"] = ("episodes/svd09_singular_matrix/scene.py", "SVD09SingularMatrix")
EPISODES["svd10"] = ("episodes/svd10_null_space/scene.py", "SVD10NullSpace")
EPISODES["svd11"] = ("episodes/svd11_rank/scene.py", "SVD11Rank")
EPISODES["svd12"] = ("episodes/svd12_pseudoinverse/scene.py", "SVD12Pseudoinverse")
EPISODES["svd13"] = ("episodes/svd13_low_rank_approximation/scene.py", "SVD13LowRankApproximation")
EPISODES["svd14"] = ("episodes/svd14_image_compression/scene.py", "SVD14ImageCompression")
EPISODES["svd15"] = ("episodes/svd15_best_rank_k/scene.py", "SVD15BestRankK")
EPISODES["svd16"] = ("episodes/svd16_rank_choice/scene.py", "SVD16RankChoice")
EPISODES["svd17"] = ("episodes/svd17_finale/scene.py", "SVD17Finale")
EPISODES["eml01"] = ("episodes/eml01_single_operator/scene.py", "EMLSingleOperator")
EPISODES["eml02"] = ("episodes/eml02_log_tree/scene.py", "EMLLogTree")
EPISODES["eml03"] = ("episodes/eml03_addition_graph/scene.py", "EMLAdditionGraph")
EPISODES["eml04"] = ("episodes/eml04_primitive_finale/scene.py", "EMLPrimitiveFinale")
EPISODES["flash01"] = ("episodes/flash01_attention_storage/scene.py", "FlashAttentionStorage")
EPISODES["flash02"] = ("episodes/flash02_io_awareness/scene.py", "FlashAttentionIO")
EPISODES["flash03"] = ("episodes/flash03_online_softmax/scene.py", "OnlineSoftmax")
EPISODES["flash04"] = ("episodes/flash04_output_accumulator/scene.py", "AttentionOutputAccumulator")
EPISODES["flash05"] = ("episodes/flash05_finale/scene.py", "FlashAttentionFinale")
EPISODES["quant01"] = ("episodes/quant01_what_is_quantization/scene.py", "WhatIsQuantization")
EPISODES["quant02"] = ("episodes/quant02_bits_and_levels/scene.py", "BitsAndLevels")
EPISODES["quant03"] = ("episodes/quant03_scale/scene.py", "QuantizationScale")
EPISODES["quant04"] = ("episodes/quant04_zero_point/scene.py", "QuantizationZeroPoint")
EPISODES["quant05"] = ("episodes/quant05_quantization_error/scene.py", "QuantizationError")
EPISODES["quant06"] = ("episodes/quant06_outlier/scene.py", "QuantizationOutlier")
EPISODES["quant07"] = ("episodes/quant07_int8_memory/scene.py", "INT8Memory")
EPISODES["quant08"] = ("episodes/quant08_quantized_matmul/scene.py", "QuantizedMatMul")
EPISODES["quant09"] = ("episodes/quant09_weight_vs_activation/scene.py", "WeightVsActivation")
EPISODES["quant10"] = ("episodes/quant10_ptq_vs_qat/scene.py", "PTQvsQAT")
EPISODES["quant11"] = ("episodes/quant11_binary_ternary/scene.py", "BinaryTernaryNetworks")
EPISODES["prune01"] = ("episodes/prune01_zero_weights/scene.py", "ZeroWeights")
EPISODES["prune02"] = ("episodes/prune02_why_not_10x/scene.py", "WhyNotTenTimes")
EPISODES["prune03"] = ("episodes/prune03_why_2_4/scene.py", "WhyTwoOfFour")
EPISODES["prune04"] = ("episodes/prune04_hardware_aware/scene.py", "HardwareAwareOptimization")
EPISODES["gpuops01"] = ("episodes/gpuops01_fma/scene.py", "GPUFMAIntroduction")
EPISODES["gpuops02"] = ("episodes/gpuops02_constant_folding/scene.py", "GPUConstantFolding")
EPISODES["gpuops03"] = ("episodes/gpuops03_loop_unrolling/scene.py", "GPULoopUnrolling")
EPISODES["gpuops04"] = ("episodes/gpuops04_warp_scheduling/scene.py", "GPUWarpScheduling")
EPISODES["gpuops05"] = ("episodes/gpuops05_epilogue_fusion/scene.py", "GPUEpilogueFusion")
EPISODES["gpuops06"] = ("episodes/gpuops06_reduction_fusion/scene.py", "GPUReductionFusion")
EPISODES["gpuops07"] = ("episodes/gpuops07_softmax_fusion/scene.py", "GPUSoftmaxFusion")
EPISODES["gpuops08"] = ("episodes/gpuops08_register_pressure/scene.py", "GPURegisterPressure")
EPISODES["gpuops09"] = ("episodes/gpuops09_relu_memory_fusion/scene.py", "GPUReLUMemoryFusion")
EPISODES["gpuops10"] = ("episodes/gpuops10_softmax_parallel/scene.py", "GPUSoftmaxParallel")
EPISODES["gpuops11"] = ("episodes/gpuops11_softmax_cross_entropy/scene.py", "GPUSoftmaxCrossEntropy")
EPISODES["gpuops12"] = ("episodes/gpuops12_dropout_rng/scene.py", "GPUDropoutRNG")
EPISODES["gpuops13"] = ("episodes/gpuops13_layernorm/scene.py", "GPULayerNorm")
EPISODES["nnmath01"] = ("episodes/nnmath01_intrinsic_dimension/scene.py", "NeuralMathIntrinsicDimension")
EPISODES["nnmath02"] = ("episodes/nnmath02_overparameterization_geometry/scene.py", "NeuralMathOverparameterization")
EPISODES["nnmath03"] = ("episodes/nnmath03_parameter_symmetry/scene.py", "NeuralMathParameterSymmetry")
EPISODES["nnmath04"] = ("episodes/nnmath04_mode_connectivity/scene.py", "NeuralMathModeConnectivity")
EPISODES["nnmath05"] = ("episodes/nnmath05_hessian_spectrum/scene.py", "NeuralMathHessianSpectrum")
EPISODES["nnmath06"] = ("episodes/nnmath06_flatness_generalization/scene.py", "NeuralMathFlatnessGeneralization")
EPISODES["nnmath07"] = ("episodes/nnmath07_double_descent/scene.py", "NeuralMathDoubleDescent")
EPISODES["nnmath08"] = ("episodes/nnmath08_optimization_implicit_bias/scene.py", "NeuralMathOptimizationImplicitBias")
EPISODES["nnmath09"] = ("episodes/nnmath09_beyond_loss_value/scene.py", "NeuralMathBeyondLossValue")
EPISODES["nnmath10"] = ("episodes/nnmath10_overparameterization_compressibility/scene.py", "NeuralMathOverparameterizationCompressibility")
EPISODES["nnmath11"] = ("episodes/nnmath11_series_finale/scene.py", "NeuralMathSeriesFinale")
EPISODES["nnmath2p01"] = ("episodes/nnmath2p01_neural_collapse/scene.py", "NeuralMathPart2NeuralCollapse")
EPISODES["nnmath2p02"] = ("episodes/nnmath2p02_superposition/scene.py", "NeuralMathPart2Superposition")
EPISODES["nnmath2p03"] = ("episodes/nnmath2p03_polysemanticity/scene.py", "NeuralMathPart2Polysemanticity")
EPISODES["nnmath2p04"] = ("episodes/nnmath2p04_identifiability/scene.py", "NeuralMathPart2Identifiability")
EPISODES["nnmath2p05"] = ("episodes/nnmath2p05_causal_intervention/scene.py", "NeuralMathPart2CausalIntervention")
EPISODES["nnmath2p06"] = ("episodes/nnmath2p06_grokking/scene.py", "NeuralMathPart2Grokking")
EPISODES["nnmath2p07"] = ("episodes/nnmath2p07_feature_vs_lazy/scene.py", "NeuralMathPart2FeatureLazy")
EPISODES["nnmath2p08"] = ("episodes/nnmath2p08_spectral_bias/scene.py", "NeuralMathPart2SpectralBias")
EPISODES["nnmath2p09"] = ("episodes/nnmath2p09_edge_of_stability/scene.py", "NeuralMathPart2EdgeOfStability")
EPISODES["nnmath2p09a"] = ("episodes/nnmath2p09a_stability_boundary/scene.py", "NeuralMathPart2StabilityBoundary")
EPISODES["nnmath2p09b"] = ("episodes/nnmath2p09b_edge_dynamics/scene.py", "NeuralMathPart2EdgeDynamics")
EPISODES["nnmath2p10"] = ("episodes/nnmath2p10_catapult/scene.py", "NeuralMathPart2Catapult")
EPISODES["nnmath2p11"] = ("episodes/nnmath2p11_benign_overfitting/scene.py", "NeuralMathPart2BenignOverfitting")
EPISODES["nnmath2p12"] = ("episodes/nnmath2p12_mode_connectivity/scene.py", "NeuralMathPart2ModeConnectivity")
EPISODES["dist01"] = ("episodes/dist01_what_is_distribution/scene.py", "WhatIsDistribution")
EPISODES["dist02"] = ("episodes/dist02_where_is_center/scene.py", "WhereIsCenter")
EPISODES["dist03"] = ("episodes/dist03_what_is_variance/scene.py", "WhatIsVariance")
EPISODES["dist04"] = ("episodes/dist04_same_mean_variance/scene.py", "SameMomentsDifferentDistributions")
EPISODES["dist05"] = ("episodes/dist05_two_variables/scene.py", "TwoVariablesTogether")
EPISODES["dist06"] = ("episodes/dist06_covariance/scene.py", "WhatIsCovariance")
EPISODES["dist07"] = ("episodes/dist07_covariance_direction/scene.py", "CovarianceDirection")
EPISODES["dist08"] = ("episodes/dist08_eigen_directions/scene.py", "CovarianceEigenDirections")
EPISODES["dist09"] = ("episodes/dist09_pca_finale/scene.py", "WhyMatrixAndPCA")
EPISODES["dist10"] = ("episodes/dist10_mahalanobis_distance/scene.py", "DistributionSetsDistance")
EPISODES["dist11"] = ("episodes/dist11_gaussian_ellipse/scene.py", "WhyGaussianEllipse")
EPISODES["dist12"] = ("episodes/dist12_gaussian_generation/scene.py", "GaussianFromOneCircle")
EPISODES["dist13"] = ("episodes/dist13_gaussian_mixture/scene.py", "GaussianMixtureDiscovery")
EPISODES["dist14"] = ("episodes/dist14_responsibility/scene.py", "ResponsibilityDiscovery")
EPISODES["dist15"] = ("episodes/dist15_latent_variable/scene.py", "LatentVariableDiscovery")
EPISODES["dist16"] = ("episodes/dist16_expectation_maximization/scene.py", "ExpectationMaximizationDiscovery")
EPISODES["dist17"] = ("episodes/dist17_elbo/scene.py", "ELBOFootsteps")
EPISODES["dist17_local"] = ("episodes/dist17_local_optimum/scene.py", "LocalOptimumDiscovery")
EPISODES["dist17_singularity"] = ("episodes/dist17_gmm_singularity/scene.py", "GMMSingularityDiscovery")

EPISODES["dist17_2"] = ("episodes/dist17_2_singularity_explained/scene.py", "SingularityExplained")

EPISODES["info01"] = ("episodes/info01_eliminating_possibilities/scene.py", "InformationEliminates")

EPISODES["info02"] = ("episodes/info02_prior_probability/scene.py", "PriorProbabilityInformation")

EPISODES["info03"] = ("episodes/info03_multiplication_depth/scene.py", "MultiplicationDepth")

EPISODES["info04"] = ("episodes/info04_expected_information/scene.py", "ExpectedInformation")

EPISODES["info05"] = ("episodes/info05_predictable_cost/scene.py", "PredictableBitCosts")

EPISODES["info06"] = ("episodes/info06_wrong_price/scene.py", "WrongProbabilityPrice")

EPISODES["info07"] = ("episodes/info07_extra_bill/scene.py", "ExtraPredictionBill")

EPISODES["info08"] = ("episodes/info08_known_bit/scene.py", "AlreadyKnownBit")

EPISODES["info09"] = ("episodes/info09_same_input/scene.py", "SameInputProcessing")

EPISODES["info10"] = ("episodes/info10_typical_worlds/scene.py", "TypicalWorlds")

EPISODES["info11"] = ("episodes/info11_density_shell/scene.py", "DensityShell")
EPISODES["info12"] = ("episodes/info12_landauer/scene.py", "LandauerErasure")
EPISODES["info13"] = ("episodes/info13_uncompute/scene.py", "ReversibleUncompute")
EPISODES["info14"] = ("episodes/info14_maxwell_demon/scene.py", "MaxwellDemon")
EPISODES["info15"] = ("episodes/info15_szilard_engine/scene.py", "SzilardEngine")
EPISODES["info16"] = ("episodes/info16_no_free_lunch/scene.py", "NoFreeLunch")

EPISODES["science01"] = ("episodes/science01_dark_matter/scene.py", "DarkMatterDiscovery")

EPISODES["science02"] = ("episodes/science02_gravitational_lensing/scene.py", "GravitationalLensingDiscovery")

EPISODES["science03"] = ("episodes/science03_bullet_cluster/scene.py", "BulletClusterDiscovery")

EPISODES["science04"] = ("episodes/science04_virial_theorem/scene.py", "VirialMassDiscovery")

EPISODES["science05"] = ("episodes/science05_gravitational_collapse/scene.py", "CollapseVirialization")

EPISODES["science06"] = ("episodes/science06_turnaround/scene.py", "TurnaroundDiscovery")

EPISODES["science07"] = ("episodes/science07_half_radius/scene.py", "HalfRadiusDiscovery")

EPISODES["science08"] = ("episodes/science08_density_growth/scene.py", "DensityGrowthDiscovery")

EPISODES["science09"] = ("episodes/science09_flat_galaxies/scene.py", "FlatGalaxyDiscovery")

EPISODES["science10"] = ("episodes/science10_cosmic_void/scene.py", "CosmicVoidDiscovery")

EPISODES["science11"] = ("episodes/science11_icecube_neutrino/scene.py", "IceCubeNeutrinoDiscovery")

EPISODES["science12"] = ("episodes/science12_neutrino_telescope/scene.py", "NeutrinoTelescopeDiscovery")

EPISODES["science13"] = ("episodes/science13_ligo_interferometer/scene.py", "LIGOInterferometerDiscovery")
EPISODES["science14"] = ("episodes/science14_attosecond_pulses/scene.py", "AttosecondPulseDiscovery")

EPISODES["act01"] = ("episodes/act01_relu_geometry/scene.py", "ReLUGeometry")
EPISODES["nnmath12"] = ("episodes/nnmath12_parameter_symmetry_quotient/scene.py", "NeuralMathPermutationQuotient")
EPISODES["nnmath13"] = ("episodes/nnmath13_gradient_dynamics/scene.py", "NeuralMathGradientDynamics")
EPISODES["nnmath14"] = ("episodes/nnmath14_hessian_flat_directions/scene.py", "NeuralMathHessianFlatDirections")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("episode", choices=EPISODES)
    p.add_argument("--preview", action="store_true")
    a = p.parse_args()
    source, scene = EPISODES[a.episode]
    env = os.environ.copy()
    env.update(VIDEO_WIDTH="360" if a.preview else "1080", VIDEO_HEIGHT="640" if a.preview else "1920")
    media = ROOT / "media" / a.episode / ("preview" if a.preview else "final")
    subprocess.run([sys.executable, "-m", "manim", "render", source, scene, "--media_dir", str(media)], cwd=ROOT, env=env, check=True)
    latest = max((media / "videos").rglob(scene + ".mp4"), key=lambda p: p.stat().st_mtime)
    output = ROOT / "exports" / (a.episode + ("_preview" if a.preview else "") + ".mp4")
    output.parent.mkdir(exist_ok=True)
    shutil.copy2(latest, output)
    print(f"Export: {output}")
if __name__ == "__main__":
    main()
