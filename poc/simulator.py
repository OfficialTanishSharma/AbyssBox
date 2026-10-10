#!/usr/bin/env python3
"""
AbyssBox :: Reference Proof-of-Concept Simulator (v1.0.0)
Author: Tanish Sharma (@OfficialTanishSharma)

Simulates acoustic high-frequency echo return ingestion, point cloud clustering,
and real-time 3D Oriented Bounding Box (Hitbox) wireframe extraction in hadal depths.
"""

import math
import random
import time

def generate_synthetic_echo_cloud(center_x, center_y, depth_z, length, width, height, num_points=120):
    """Generates synthetic high-frequency acoustic echo return points scattered across an ellipsoidal biomass."""
    points = []
    for _ in range(num_points):
        # Parametric ellipsoid with gaussian sensor noise
        u = random.random()
        v = random.uniform(0, 2 * math.pi)
        theta = random.uniform(0, math.pi)
        
        rx = (length / 2) * math.sin(theta) * math.cos(v) + random.gauss(0, 0.4)
        ry = (width / 2) * math.sin(theta) * math.sin(v) + random.gauss(0, 0.3)
        rz = (height / 2) * math.cos(theta) + random.gauss(0, 0.3)
        
        points.append((center_x + rx, center_y + ry, depth_z + rz))
    return points

def compute_3d_hitbox(points):
    """Computes Centroid and Axis-Aligned/Oriented extents from point cloud returns."""
    k = len(points)
    if k == 0:
        return None
    
    # 1. Centroid
    cx = sum(p[0] for p in points) / k
    cy = sum(p[1] for p in points) / k
    cz = sum(p[2] for p in points) / k
    
    # 2. Extents
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    min_z = min(p[2] for p in points)
    max_z = max(p[2] for p in points)
    
    ext_l = max_x - min_x
    ext_w = max_y - min_y
    ext_h = max_z - min_z
    
    return {
        "centroid": (round(cx, 2), round(cy, 2), round(cz, 2)),
        "extents": (round(ext_l, 2), round(ext_w, 2), round(ext_h, 2)),
        "volume_m3": round(ext_l * ext_w * ext_h, 2),
        "point_count": k
    }

def print_ascii_hitbox(hitbox, label, velocity_kts):
    cx, cy, cz = hitbox["centroid"]
    l, w, h = hitbox["extents"]
    
    print("\n" + "=" * 70)
    print("     ABYSSBOX :: ACOUSTIC 3D HITBOX EXTRACTION PROTOCOL (v1.0.0)")
    print("=" * 70)
    print(f"[STATUS] Hydrophone Array: 165 kHz Ultrasonic Carrier Active.")
    print(f"[STATUS] Acoustic Speed c_sw: 1,484.2 m/s | Ambient Pressure: 82.4 MPa")
    print(f"[STATUS] Target Acquired in Trench Depth: {cz} meters.")
    print("-" * 70)
    print("  CALCULATED ORIENTED BOUNDING BOX (HITBOX):")
    print(f"    Spatial Centroid : X: {cx:+0.1f}m | Y: {cy:+0.1f}m | Depth Z: {cz:0.1f}m")
    print(f"    Bounding Extents : Length: {l:.1f}m | Width: {w:.1f}m | Height: {h:.1f}m")
    print(f"    Calculated Vol   : {hitbox['volume_m3']:,} m^3 (Echo Density: {hitbox['point_count']} pts)")
    print(f"    Estimated Speed  : {velocity_kts:.1f} knots (Kinematic Vector: Hydro-Dynamic)")
    print(f"    Classification   : {label}")
    print("-" * 70)
    print("[HUD WIREFRAME VISUALIZATION]:")
    print("               +---------------------------------------+")
    print("              /                                       /|")
    print("             /                                       / |")
    print("            +---------------------------------------+  |")
    print(f"            |  [ HITBOX ID: #BB-8492 ]              |  |")
    print(f"            |  LENGTH: {l:<5.1f}m | WIDTH: {w:<4.1f}m       |  +")
    print(f"            |  DEPTH : {cz:<7.1f}m                    | /")
    print(f"            |  SPEED : {velocity_kts:<4.1f} kts                    |/")
    print("            +---------------------------------------+")
    print("=" * 70 + "\n")

def main():
    print("[INIT] Initializing AbyssBox Core Signal Ingestion...")
    time.sleep(0.3)
    
    # Simulate an anomalous 54-meter benthic leviathan entity in Puerto Rico Trench (-8,240m)
    center_x = 185.4
    center_y = 92.1
    depth_z = -8240.5
    length = 54.0
    width = 13.5
    height = 9.8
    
    echoes = generate_synthetic_echo_cloud(center_x, center_y, depth_z, length, width, height)
    hitbox = compute_3d_hitbox(echoes)
    
    classification = "ANOMALOUS_HADAL_MACRO_ORGANISM (Conf: 99.1%)"
    velocity_kts = 21.6
    
    print_ascii_hitbox(hitbox, classification, velocity_kts)
    print("[SUCCESS] Telemetry packed: 32-byte binary frame ready for acoustic uplink.")

if __name__ == "__main__":
    main()
