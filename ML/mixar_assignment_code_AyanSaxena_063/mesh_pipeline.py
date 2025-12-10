
#!/usr/bin/env python3
# Mesh Normalization, Quantization, Error Analysis + Bonus Task (Invariant & Adaptive Quantization)
import argparse
from pathlib import Path
import numpy as np
import trimesh
import matplotlib.pyplot as plt
import csv, json, warnings
from scipy.spatial import cKDTree

warnings.filterwarnings("ignore", category=UserWarning)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def save_mesh(vertices, faces, path):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces if faces is not None and len(faces) > 0 else None, process=False)
    mesh.export(path.as_posix())

def min_max_normalize(V):
    vmin, vmax = V.min(axis=0), V.max(axis=0)
    denom = vmax - vmin
    denom[denom == 0] = 1
    return (V - vmin) / denom, (vmin, vmax)

def min_max_denormalize(N, params):
    vmin, vmax = params
    return N * (vmax - vmin) + vmin

def unit_sphere_normalize(V):
    centroid = V.mean(axis=0)
    centered = V - centroid
    scale = np.linalg.norm(centered, axis=1).max() or 1
    return centered / scale, (centroid, scale)

def unit_sphere_denormalize(N, params):
    c, s = params
    return N * s + c

def quantize(N, bins):
    nmin, nmax = N.min(), N.max()
    if nmin < 0 or nmax > 1:
        N01 = (N + 1) / 2
        mapped = True
    else:
        N01, mapped = N, False
    q = np.floor(N01 * (bins - 1)).astype(int)
    return np.clip(q, 0, bins - 1), {"mapped_to_01": mapped}

def dequantize(q, bins, meta):
    N01 = q.astype(float) / (bins - 1)
    return N01 * 2 - 1 if meta.get("mapped_to_01", False) else N01

def compute_errors(orig, recon):
    diff = orig - recon
    mse, mae = np.mean(diff**2), np.mean(np.abs(diff))
    return {"mse": float(mse), "mae": float(mae),
            "mse_axes": np.mean(diff**2, axis=0).tolist(),
            "mae_axes": np.mean(np.abs(diff), axis=0).tolist()}

def plot_error_bars(errors, title, outpath):
    fig = plt.figure()
    plt.bar(["x", "y", "z"], errors)
    plt.title(title)
    plt.tight_layout()
    fig.savefig(outpath, dpi=200)
    plt.close(fig)

def write_csv(path, rows, header):
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows([header] + rows)

def process_mesh(mesh_path, out_dir, bins):
    name = mesh_path.stem
    out = out_dir / name; ensure_dir(out)
    mesh = trimesh.load(mesh_path.as_posix(), process=False)
    V, F = mesh.vertices.view(np.ndarray), getattr(mesh, "faces", None)

    stats = {"n_vertices": len(V), "min": V.min(0).tolist(),
             "max": V.max(0).tolist(), "mean": V.mean(0).tolist(),
             "std": V.std(0).tolist()}
    json.dump(stats, open(out / "stats.json", "w"), indent=2)
    save_mesh(V, F, out / f"{name}_original.obj")

    all_rows = []
    for label, norm_fn, denorm_fn in [("minmax", min_max_normalize, min_max_denormalize),
                                      ("unitsphere", unit_sphere_normalize, unit_sphere_denormalize)]:
        N, p = norm_fn(V)
        save_mesh(N, F, out / f"{name}_{label}_normalized.obj")
        q, meta = quantize(N, bins)
        save_mesh(q.astype(float), F, out / f"{name}_{label}_quantized.ply")
        N_dq = dequantize(q, bins, meta)
        V_rec = denorm_fn(N_dq, p)
        save_mesh(V_rec, F, out / f"{name}_{label}_reconstructed.obj")
        err = compute_errors(V, V_rec)
        plot_error_bars(err["mse_axes"], f"{name}-{label} MSE", out / f"{name}_{label}_mse.png")
        plot_error_bars(err["mae_axes"], f"{name}-{label} MAE", out / f"{name}_{label}_mae.png")
        all_rows.append([name, label, err["mse"], err["mae"], *err["mse_axes"], *err["mae_axes"]])
    write_csv(out / f"{name}_summary.csv", all_rows,
              ["mesh","method","mse_total","mae_total","mse_x","mse_y","mse_z","mae_x","mae_y","mae_z"])

# ----- BONUS TASK FUNCTIONS -----

def random_transform(V):
    th, ph, ps = np.random.rand(3) * 2*np.pi
    Rz1 = np.array([[np.cos(th), -np.sin(th), 0],
                    [np.sin(th), np.cos(th), 0], [0,0,1]])
    Ry = np.array([[np.cos(ph), 0, np.sin(ph)],
                   [0,1,0],[-np.sin(ph),0,np.cos(ph)]])
    Rz2 = np.array([[np.cos(ps), -np.sin(ps), 0],
                    [np.sin(ps), np.cos(ps), 0], [0,0,1]])
    R = Rz2 @ Ry @ Rz1
    T = np.random.uniform(-0.5,0.5,(1,3))
    return V @ R.T + T

def invariant_normalize(V):
    c = V.mean(0)
    centered = V - c
    rms = np.sqrt(np.mean(np.sum(centered**2,axis=1))) or 1
    return centered / rms, (c, rms)

def adaptive_quantize(V, bins=1024, k=8):
    tree = cKDTree(V)
    dists, _ = tree.query(V, k=k)
    density = 1.0 / (np.mean(dists,1) + 1e-8)
    scale = 0.5 + (density - density.min())/(density.max()-density.min())
    q = np.floor(V * (bins-1) * scale[:,None]).astype(int)
    return np.clip(q,0,bins-1), {"scale_range":[scale.min(),scale.max()]}

def bonus_task(mesh_path, out_dir, bins=1024, n_transforms=3):
    name = mesh_path.stem
    out = out_dir / f"{name}_bonus"; ensure_dir(out)
    mesh = trimesh.load(mesh_path.as_posix(), process=False)
    V, F = mesh.vertices.view(np.ndarray), getattr(mesh, "faces", None)
    rows = []
    for i in range(n_transforms):
        Vt = random_transform(V)
        N, p = invariant_normalize(Vt)
        q, meta = adaptive_quantize(N, bins)
        N_dq = q/(bins-1)
        V_rec = N_dq*p[1]+p[0]
        err = compute_errors(Vt, V_rec)
        save_mesh(V_rec, F, out / f"{name}_recon_{i}.obj")
        plot_error_bars(err["mse_axes"], f"{name} bonus {i}", out / f"{name}_mse_{i}.png")
        rows.append([i, err["mse"], err["mae"], *err["mse_axes"], *err["mae_axes"]])
    write_csv(out / f"{name}_bonus_summary.csv", rows,
              ["transform_id","mse_total","mae_total","mse_x","mse_y","mse_z","mae_x","mae_y","mae_z"])
    print(f"[Bonus] {name}: {n_transforms} transforms done.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", type=str, default="./meshes")
    ap.add_argument("--output_dir", type=str, default="./outputs")
    ap.add_argument("--bins", type=int, default=1024)
    ap.add_argument("--bonus", action="store_true")
    args = ap.parse_args()
    in_dir, out_dir = Path(args.input_dir), Path(args.output_dir)
    ensure_dir(out_dir)
    files = list(in_dir.glob("*.obj"))
    if not files: print(f"No OBJ in {in_dir}"); return
    for f in files:
        process_mesh(f, out_dir, args.bins)
        if args.bonus:
            bonus_task(f, out_dir, args.bins)

if __name__ == "__main__":
    main()
