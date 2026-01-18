#!/usr/bin/env python3
"""
Fractal Wallpaper Generator - "Order from Chaos"
Julia Set with philosophical depth: the boundary between stability and infinity.

For MacBook Pro 14" (3024x1964)
Perfect for OCPD: mathematically precise yet infinitely complex.
"""

from PIL import Image, ImageDraw, ImageFilter
from math import sqrt
import colorsys

import numpy as np


W, H = 3024, 1964

def create_julia_wallpaper(c_real=-0.7269, c_imag=0.1889, max_iter=300):
    """
    Julia Set - a map of stability vs chaos.
    
    Each point either escapes to infinity or stays bounded forever.
    The boundary between these two fates is infinitely complex.
    
    Like the mind seeking order: some thoughts stabilize, 
    others spiral endlessly. Beauty lives at the edge.
    """
    
    print("Generating Julia Set fractal...")
    
    # Create coordinate arrays
    # Centered, with aspect ratio correction
    x = np.linspace(-2.0, 2.0, W)
    y = np.linspace(-1.3, 1.3, H)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Julia constant - this specific value creates beautiful spirals
    c = complex(c_real, c_imag)
    
    # Track iterations to escape
    iterations = np.zeros(Z.shape, dtype=np.float64)
    mask = np.ones(Z.shape, dtype=bool)
    
    # Smooth coloring: track final |z| for smooth gradients
    final_z = np.zeros(Z.shape, dtype=np.float64)
    
    print("Iterating fractal...")
    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c    # z=z²+c
        
        # Check escape condition
        escaped = np.abs(Z) > 4
        new_escaped = escaped & mask
        
        # Store iteration count with smooth coloring
        iterations[new_escaped] = i - np.log2(np.log2(np.abs(Z[new_escaped]) + 1))
        final_z[new_escaped] = np.abs(Z[new_escaped])
        
        mask[escaped] = False
        
        if i % 50 == 0:
            print(f"  Iteration {i}/{max_iter}")
    
    iterations[mask] = max_iter    # Points that never escaped
    print("Applying color mapping...")
    
    # Normalize iterations
    iterations_norm = iterations / max_iter
    
    # Create RGB array
    arr = np.zeros((H, W, 3), dtype=np.float32)
    
    # Color palette: deep space theme
    # Interior (stable points) - deep navy/black
    # Exterior (escaping points) - gradient from teal to purple to copper
    
    for y_idx in range(H):
        for x_idx in range(W):
            t = iterations_norm[y_idx, x_idx]
            
            if t >= 0.99:  # Interior - the stable set
                # Deep, almost black with subtle blue
                arr[y_idx, x_idx] = [8, 12, 20]
            else:
                # Exterior - smooth gradient based on escape time
                # Use multiple color bands for richness
                
                # Cycle through colors
                t_cycled = (t * 5) % 1.0  # 5 color cycles
                
                if t_cycled < 0.25:
                    # Deep teal
                    tt = t_cycled / 0.25
                    r = 15 + tt * 25
                    g = 40 + tt * 40
                    b = 60 + tt * 30
                elif t_cycled < 0.5:
                    # Teal to purple
                    tt = (t_cycled - 0.25) / 0.25
                    r = 40 + tt * 50
                    g = 80 - tt * 30
                    b = 90 + tt * 40
                elif t_cycled < 0.75:
                    # Purple to copper
                    tt = (t_cycled - 0.5) / 0.25
                    r = 90 + tt * 60
                    g = 50 + tt * 20
                    b = 130 - tt * 50
                else:
                    # Copper back to deep
                    tt = (t_cycled - 0.75) / 0.25
                    r = 150 - tt * 135
                    g = 70 - tt * 30
                    b = 80 - tt * 20
                
                # Darken based on overall escape time (faster escape = brighter edge)
                brightness = 0.3 + 0.7 * (1 - t)
                arr[y_idx, x_idx] = [r * brightness, g * brightness, b * brightness]
    
    print("Adding vignette...")
    
    # Vignette
    cy, cx = H // 2, W // 2
    max_dist = sqrt(cx**2 + cy**2)
    
    y_coords, x_coords = np.ogrid[:H, :W]
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2) / max_dist
    vignette = 1 - (dist ** 1.8) * 0.4
    
    for i in range(3):
        arr[:, :, i] *= vignette
    
    print("Adding subtle grain...")
    
    # Subtle grain
    grain = np.random.normal(0, 4, arr.shape)
    arr += grain
    
    # Clip and convert
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    return img


def create_mandelbrot_detail(center_x=-0.745, center_y=0.186, zoom=200, max_iter=400):
    """
    Mandelbrot Set detail - zoomed into a beautiful spiral region.
    
    The Mandelbrot set: all c values where z = z² + c stays bounded.
    At the boundary: infinite complexity from the simplest equation.
    """
    
    print(f"Generating Mandelbrot detail at ({center_x}, {center_y}), zoom {zoom}x...")
    
    # Calculate bounds based on zoom
    span_x = 3.0 / zoom
    span_y = span_x * H / W
    
    x = np.linspace(center_x - span_x/2, center_x + span_x/2, W)
    y = np.linspace(center_y - span_y/2, center_y + span_y/2, H)
    C = np.zeros((H, W), dtype=np.complex128)
    
    for i in range(H):
        for j in range(W):
            C[i, j] = complex(x[j], y[i])
    
    Z = np.zeros_like(C)
    iterations = np.zeros((H, W), dtype=np.float64)
    mask = np.ones((H, W), dtype=bool)
    
    print("Iterating Mandelbrot...")
    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        
        escaped = np.abs(Z) > 4
        new_escaped = escaped & mask
        
        # Smooth iteration count
        with np.errstate(invalid='ignore', divide='ignore'):
            smooth_val = i - np.log2(np.log2(np.abs(Z[new_escaped]) + 1))
            smooth_val = np.nan_to_num(smooth_val, nan=i)
        iterations[new_escaped] = smooth_val
        
        mask[escaped] = False
        
        if i % 100 == 0:
            print(f"  Iteration {i}/{max_iter}")
    
    iterations[mask] = max_iter
    
    print("Coloring...")
    
    # Normalize
    iter_min = iterations[iterations < max_iter].min() if (iterations < max_iter).any() else 0
    iter_max = iterations[iterations < max_iter].max() if (iterations < max_iter).any() else max_iter
    
    arr = np.zeros((H, W, 3), dtype=np.float32)
    
    for yi in range(H):
        for xi in range(W):
            it = iterations[yi, xi]
            
            if it >= max_iter - 1:
                # Interior
                arr[yi, xi] = [5, 8, 15]
            else:
                # Map to 0-1
                t = (it - iter_min) / (iter_max - iter_min + 0.001)
                
                # Rich color palette
                t_mod = (t * 8) % 1.0
                
                # HSV-like mapping for smooth colors
                hue = 0.55 + t * 0.3  # Teal to purple range
                sat = 0.5 + t_mod * 0.3
                val = 0.2 + (1-t) * 0.6
                
                r, g, b = colorsys.hsv_to_rgb(hue % 1.0, sat, val)
                arr[yi, xi] = [r * 255, g * 255, b * 255]
    
    # Vignette
    cy, cx = H // 2, W // 2
    max_dist = sqrt(cx**2 + cy**2)
    y_coords, x_coords = np.ogrid[:H, :W]
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2) / max_dist
    vignette = 1 - (dist ** 1.8) * 0.35
    
    for i in range(3):
        arr[:, :, i] *= vignette
    
    # Grain
    grain = np.random.normal(0, 3, arr.shape)
    arr += grain
    
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img


if __name__ == "__main__":
    import sys
    
    output_dir = "/home/claude/wallpapers/png"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Choose fractal type
    fractal_type = sys.argv[1] if len(sys.argv) > 1 else "julia"
    
    if fractal_type == "julia":
        # Beautiful spiral Julia set
        img = create_julia_wallpaper(
            c_real=-0.7269,  # Classic beautiful constant
            c_imag=0.1889,
            max_iter=250
        )
        filename = f"{output_dir}/fractal_julia.png"
        
    elif fractal_type == "julia2":
        # Different Julia - more dendritic
        img = create_julia_wallpaper(
            c_real=-0.8,
            c_imag=0.156,
            max_iter=300
        )
        filename = f"{output_dir}/fractal_julia_dendrite.png"
        
    elif fractal_type == "mandelbrot":
        # Mandelbrot seahorse valley detail
        img = create_mandelbrot_detail(
            center_x=-0.745,
            center_y=0.186,
            zoom=150,
            max_iter=350
        )
        filename = f"{output_dir}/fractal_mandelbrot.png"
        
    else:
        print(f"Unknown type: {fractal_type}")
        print("Usage: python fractal_wallpaper.py [julia|julia2|mandelbrot]")
        sys.exit(1)
    
    print(f"Saving to {filename}...")
    img.save(filename, quality=95)
    print("Done!")
    print(f"\nFile saved: {filename}")
