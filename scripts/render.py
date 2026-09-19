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
