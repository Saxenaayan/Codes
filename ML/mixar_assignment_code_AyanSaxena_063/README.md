# Mixar Assignment — Mesh Normalization, Quantization, and Error Analysis  

### Author: Ayan Saxena  
### Topic: SeamGPT Data Processing Technical Assignment  

---

##  Overview  

This assignment implements **3D mesh preprocessing and analysis**, focusing on:
- **Normalization**
- **Quantization**
- **Reconstruction & Error Evaluation**
- and an advanced **Bonus Task** on *rotation/translation invariance and adaptive quantization.*

All the work is done using Python with `NumPy`, `Trimesh`, `SciPy`, and `Matplotlib`.



---

### **Task 1: Load and Inspect the Mesh **  

**What I did:**
- Used the `trimesh` library to load `.obj` mesh files.
- Extracted only the **vertex coordinates** (x, y, z) as a NumPy array.
- Calculated and printed:
  - Total number of vertices
  - Minimum, maximum, mean, and standard deviation per axis
- Saved these values in a structured `stats.json` file for each mesh.

**Outcome:**
- Understood how raw 3D vertices are represented.
- Verified that meshes were read correctly before applying transformations.  

**Code Reference:**  
Functions — `process_mesh()` and the section saving `stats.json`.

---

### **Task 2: Normalize and Quantize the Mesh **  

**What I did:**
- Implemented **two normalization methods**:
  1. **Min–Max Normalization:** scales all vertex coordinates into the range [0, 1].
  2. **Unit Sphere Normalization:** centers the mesh and scales it so all points lie within a sphere of radius 1.
- Applied **quantization** (default 1024 bins) to discretize these continuous values.
- Saved the quantized meshes in `.ply` format.
- Generated **visualizations (bar plots)** showing MSE/MAE errors per axis.
- Compared both normalization techniques to observe which one preserved mesh geometry better.

**Outcome:**
- Min–Max normalization gave very low error for symmetric meshes.
- Unit Sphere normalization was more robust for meshes with irregular or large coordinate ranges.

**Code Reference:**  
Functions — `min_max_normalize()`, `unit_sphere_normalize()`, `quantize()`, and plots in `plot_error_bars()`.

---

### **Task 3: Dequantize, Denormalize, and Measure Error **  

**What I did:**
- Reversed the transformations using:
  - `dequantize()` → maps quantized bins back to normalized space.
  - `min_max_denormalize()` or `unit_sphere_denormalize()` → restores original scale.
- Calculated **Mean Squared Error (MSE)** and **Mean Absolute Error (MAE)** between:
  - Original vertices  
  - Reconstructed vertices
- Visualized per-axis reconstruction errors (X, Y, Z) using Matplotlib.
- Saved all processed meshes (original, normalized, quantized, reconstructed) for visual comparison.

**Outcome:**
- Quantitative and visual evaluation of how much information was lost after normalization + quantization.
- Gained intuition about mesh precision vs. compression trade-offs.

**Code Reference:**  
Functions — `compute_errors()`, `plot_error_bars()`, and reconstruction steps in `process_mesh()`.

---

## 🧪 **Bonus Task: Rotation & Translation Invariance + Adaptive Quantization**  

**What I did:**
- Implemented a **rotation and translation invariant normalization**:
  - Centered the mesh at its centroid.
  - Scaled by RMS (root-mean-square) distance, making it consistent under rotations.
- Applied **random rotations and translations** to simulate different mesh orientations.
- Designed **adaptive quantization**:
  - Used `scipy.spatial.cKDTree` to find local vertex density.
  - Assigned **smaller bins** in dense areas (high geometric detail) and **larger bins** in sparse regions.
- Reconstructed the transformed meshes and computed reconstruction errors for each variant.
- Saved per-transform OBJ files, plots, and error summaries.

**Outcome:**
- Demonstrated how preprocessing can remain stable across orientation and position changes.
- Adaptive quantization improved fidelity in high-detail regions, confirming its usefulness for 3D-aware AI training.

**Code Reference:**  
Functions — `random_transform()`, `invariant_normalize()`, `adaptive_quantize()`, and `bonus_task()`.

---

## 📂 Folder Structure  

```
mixar_assignment_code_bonus/
│
├── mesh_pipeline.py        → Main Python script
├── requirements.txt        → Library dependencies
├── README.md               → Project documentation
│
├── meshes/                 → Input .obj meshes
│   └── sample_mesh.obj
│
└── outputs/                → Auto-generated results
    ├── sample_mesh/
    │   ├── *_normalized.obj
    │   ├── *_quantized.ply
    │   ├── *_summary.csv
    │   └── error plots (.png)
    └── sample_mesh_bonus/
        ├── *_recon_*.obj
        ├── *_mse_*.png
        └── *_bonus_summary.csv
```

---

##  How to Run  

### 1️ Install dependencies:
```bash
pip install -r requirements.txt
```

### 2️ Place your `.obj` meshes in the `meshes/` folder.

### 3️ Run the main script:
**For regular tasks:**
```bash
python mesh_pipeline.py --input_dir ./meshes --output_dir ./outputs
```

**For the Bonus Task:**
```bash
python mesh_pipeline.py --input_dir ./meshes --output_dir ./outputs --bonus
```

---

##  Outputs  

Each mesh generates:
- Original, normalized, quantized, reconstructed `.obj` and `.ply` files.
- CSV summaries of MSE/MAE.
- Per-axis error plots.
- Additional “bonus” outputs for rotated/translated versions with adaptive quantization.

---


---

##  Summary  

| Task | Focus |  Implementation |
|------|--------|-------------------|
| **Task 1** | Mesh loading & inspection | Basic stats via Trimesh |
| **Task 2** | Normalization & Quantization  | Min–Max & Unit Sphere methods |
| **Task 3** | Reconstruction & Error Analysis | MSE/MAE + Visualization |
| **Bonus Task** | Invariance + Adaptive Quantization  | Random rotations, KDTree density, adaptive bins |

---


