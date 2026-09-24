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
