# SPEC-01: Ultrasonic Volumetric Bounding-Box (OBB) Protocol Specification

- **Status:** Draft / Proposed Standard
- **Author:** Tanish Sharma ([@OfficialTanishSharma](https://github.com/OfficialTanishSharma))
- **Date:** October 2026
- **Target Implementation:** Autonomous Underwater Vehicles (AUVs), Hadal Probes, High-Resolution Subsea SLAM

---

## 1. Frequency Band Allocation & Biological De-Confliction

| Parameter | Specification | Scientific Rationale |
| :--- | :--- | :--- |
| **Primary Excitation Carrier** | $165.0\text{ kHz} \pm 15.0\text{ kHz}$ | Sub-centimeter spatial resolution while preventing acoustic resonance in cetacean anatomical cavities. |
| **Modulation Schema** | Linear Frequency Modulation (Chirp) | Optimizes Signal-to-Noise Ratio (SNR) in high thermal-stratification zones (Thermoclines). |
| **Pulse Duration** | $5.0\text{ ms} - 25.0\text{ ms}$ | Prevents multi-path destructive superposition across narrow trench walls. |
| **Whale Auditory Band** | $10\text{ Hz} - 1.0\text{ kHz}$ | Zero overlap. Cetaceans (*Mysticetes*) are biologically deaf to $>100\text{ kHz}$ excitation. |

---

## 2. Acoustic Echo to Point Cloud Inversion

The receiver array utilizes a 2D planar hydrophone matrix of dimension $M \times N$.
For an incident wavefront arriving at angle $(\theta, \phi)$, the phase shift $\Delta \Phi_{m,n}$ across element $(m,n)$ is defined as:

$$\Delta \Phi_{m,n} = \frac{2\pi}{\lambda} \left( m \cdot d_x \sin\theta \cos\phi + n \cdot d_y \sin\theta \sin\phi \right)$$

Echo time-of-flight $\tau$ determines distance $R$:
$$R = \frac{c_{\text{seawater}} \cdot \tau}{2}$$
*(Where $c_{\text{seawater}} \approx 1482\text{ m/s} + 4.5 T - 0.05 T^2 + 0.016 D + 1.3 (S - 35)$)*

Sparse point clouds $\mathcal{P} = \{ p_i \in \mathbb{R}^3 \}$ are clustered via Euclidean DBSCAN with dynamic density adaptation $\epsilon = f(R)$.

---

## 3. Real-Time Oriented Bounding Box (Hitbox) Computation

Given a clustered point set $\mathcal{P}_{\text{target}}$ of $K$ spatial return vectors:

1. **Centroid $\mathbf{C}$:**
   $$\mathbf{C} = \frac{1}{K} \sum_{i=1}^{K} p_i$$

2. **Covariance Matrix $\mathbf{\Sigma}$:**
   $$\mathbf{\Sigma} = \frac{1}{K} \sum_{i=1}^{K} (p_i - \mathbf{C})(p_i - \mathbf{C})^T$$

3. **Principal Axes Extraction:**
   Perform Eigenvalue Decomposition:
   $$\mathbf{\Sigma} = \mathbf{V} \mathbf{\Lambda} \mathbf{V}^T$$
   The eigenvectors $\mathbf{V} = [\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3]$ establish the orthogonal spatial axes of the Oriented Bounding Box (Hitbox).

4. **Bounding Extents $(L, W, H)$:**
   Project $\mathcal{P}_{\text{target}}$ onto $\mathbf{V}$ to extract $[\min, \max]$ boundaries:
   $$L = \max(p_i \cdot \mathbf{v}_1) - \min(p_i \cdot \mathbf{v}_1)$$
   $$W = \max(p_i \cdot \mathbf{v}_2) - \min(p_i \cdot \mathbf{v}_2)$$
   $$H = \max(p_i \cdot \mathbf{v}_3) - \min(p_i \cdot \mathbf{v}_3)$$

---

## 4. Telemetry Binary Packet Format (32 Bytes Compact)

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Sync Word (0xAB55)      |       Packet Sequence ID      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Centroid X (float32)                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Centroid Y (float32)                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Centroid Depth Z (float32)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Extent L (uint16)       |       Extent W (uint16)       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Extent H (uint16)       |   Velocity Heading (uint16)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Velocity Mag (uint16)   | Class ID (u8) | Conf (u8)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           CRC32 Checksum                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
*(Transmittable over ultra-low-bandwidth acoustic hydrophone modems across $10\text{ km}$ depth).*
