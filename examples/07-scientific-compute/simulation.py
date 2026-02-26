#!/usr/bin/env python3
"""
Example 7: Scientific Computing (Python → Julia)
Original Python N-body gravitational simulation
"""

import math
import time
import sys
import json

class Body:
    """Celestial body with position, velocity, and mass"""
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

    def kinetic_energy(self):
        """Calculate kinetic energy: 0.5 * m * v^2"""
        v_squared = self.vx**2 + self.vy**2 + self.vz**2
        return 0.5 * self.mass * v_squared

def create_solar_system(num_bodies=1000):
    """
    Create a simplified solar system with N bodies
    - Central massive body (sun)
    - Orbiting bodies with random positions and velocities
    """
    bodies = []

    # Central body (sun-like mass)
    bodies.append(Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.989e30))

    # Generate random orbiting bodies
    import random
    random.seed(42)  # Reproducible results

    for i in range(num_bodies - 1):
        # Random orbital radius (1 AU to 50 AU)
        radius = random.uniform(1.0, 50.0) * 1.496e11

        # Random angle
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)

        # Position on sphere
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)

        # Orbital velocity (circular orbit approximation)
        G = 6.67430e-11  # Gravitational constant
        M = 1.989e30     # Central mass
        v_orbital = math.sqrt(G * M / radius)

        # Velocity perpendicular to radius
        vx = -v_orbital * math.sin(theta)
        vy = v_orbital * math.cos(theta)
        vz = 0.0

        # Random mass (asteroid to planet scale)
        mass = random.uniform(1e20, 1e24)

        bodies.append(Body(x, y, z, vx, vy, vz, mass))

    return bodies

def compute_forces(bodies):
    """
    Compute gravitational forces between all body pairs
    F = G * m1 * m2 / r^2
    """
    G = 6.67430e-11  # Gravitational constant
    n = len(bodies)

    # Initialize force accumulators
    forces = [(0.0, 0.0, 0.0) for _ in range(n)]

    # O(n^2) force calculation (all pairs)
    for i in range(n):
        for j in range(i + 1, n):
            # Vector from body i to body j
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            dz = bodies[j].z - bodies[i].z

            # Distance
            r_squared = dx**2 + dy**2 + dz**2
            r = math.sqrt(r_squared)

            # Avoid division by zero (softening parameter)
            if r < 1e6:  # 1 km minimum distance
                r = 1e6
                r_squared = r**2

            # Force magnitude: F = G * m1 * m2 / r^2
            force_magnitude = G * bodies[i].mass * bodies[j].mass / r_squared

            # Force direction (unit vector)
            fx = force_magnitude * dx / r
            fy = force_magnitude * dy / r
            fz = force_magnitude * dz / r

            # Apply Newton's third law (equal and opposite forces)
            forces[i] = (forces[i][0] + fx, forces[i][1] + fy, forces[i][2] + fz)
            forces[j] = (forces[j][0] - fx, forces[j][1] - fy, forces[j][2] - fz)

    return forces

def update_velocities(bodies, forces, dt):
    """
    Update velocities using computed forces
    v_new = v_old + a * dt
    where a = F / m
    """
    for i, body in enumerate(bodies):
        fx, fy, fz = forces[i]

        # Acceleration: a = F / m
        ax = fx / body.mass
        ay = fy / body.mass
        az = fz / body.mass

        # Update velocity: v = v + a * dt
        body.vx += ax * dt
        body.vy += ay * dt
        body.vz += az * dt

def update_positions(bodies, dt):
    """
    Update positions using velocities
    x_new = x_old + v * dt
    """
    for body in bodies:
        body.x += body.vx * dt
        body.y += body.vy * dt
        body.z += body.vz * dt

def compute_total_energy(bodies):
    """
    Compute total energy (kinetic + potential)
    Used for validation (energy should be conserved)
    """
    G = 6.67430e-11

    # Kinetic energy
    kinetic = sum(body.kinetic_energy() for body in bodies)

    # Potential energy (gravitational)
    potential = 0.0
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            dz = bodies[j].z - bodies[i].z
            r = math.sqrt(dx**2 + dy**2 + dz**2)

            if r > 1e6:  # Avoid singularity
                potential -= G * bodies[i].mass * bodies[j].mass / r

    total = kinetic + potential
    return kinetic, potential, total

def run_simulation(num_bodies=1000, num_steps=100, dt=86400.0):
    """
    Run N-body gravitational simulation
    - num_bodies: Number of celestial bodies
    - num_steps: Number of time steps
    - dt: Time step size (seconds) - default 1 day
    """
    print("╔══════════════════════════════════════════════╗")
    print("║   Python N-Body Gravitational Simulation    ║")
    print("╚══════════════════════════════════════════════╝\n")

    print(f"Configuration:")
    print(f"  Bodies: {num_bodies}")
    print(f"  Time steps: {num_steps}")
    print(f"  Time step size: {dt/86400:.2f} days")
    print(f"  Total simulation time: {num_steps * dt / 86400:.2f} days")
    print()

    # Initialize solar system
    init_start = time.time()
    bodies = create_solar_system(num_bodies)
    init_time = time.time() - init_start
    print(f"  Initialization: {init_time:.3f}s\n")

    # Compute initial energy (for validation)
    ke_initial, pe_initial, total_initial = compute_total_energy(bodies)
    print(f"Initial Energy:")
    print(f"  Kinetic: {ke_initial:.3e} J")
    print(f"  Potential: {pe_initial:.3e} J")
    print(f"  Total: {total_initial:.3e} J\n")

    # Main simulation loop
    print("Running simulation...")
    sim_start = time.time()

    for step in range(num_steps):
        # Compute forces (O(n^2) - bottleneck)
        forces = compute_forces(bodies)

        # Update velocities (O(n))
        update_velocities(bodies, forces, dt)

        # Update positions (O(n))
        update_positions(bodies, dt)

        # Progress reporting
        if (step + 1) % 10 == 0:
            elapsed = time.time() - sim_start
            steps_per_sec = (step + 1) / elapsed
            eta = (num_steps - step - 1) / steps_per_sec if steps_per_sec > 0 else 0
            print(f"  Step {step + 1}/{num_steps} | {steps_per_sec:.2f} steps/sec | ETA: {eta:.1f}s")

    sim_time = time.time() - sim_start
    total_time = init_time + sim_time

    # Compute final energy (for validation)
    ke_final, pe_final, total_final = compute_total_energy(bodies)

    # Energy conservation check
    energy_error = abs(total_final - total_initial) / abs(total_initial) * 100

    print(f"\nFinal Energy:")
    print(f"  Kinetic: {ke_final:.3e} J")
    print(f"  Potential: {pe_final:.3e} J")
    print(f"  Total: {total_final:.3e} J")
    print(f"  Energy error: {energy_error:.6f}%")

    print(f"\n{'='*60}")
    print("SIMULATION SUMMARY")
    print('='*60)
    print(f"Total time: {total_time:.3f}s")
    print(f"  Initialization: {init_time:.3f}s ({init_time/total_time*100:.1f}%)")
    print(f"  Simulation: {sim_time:.3f}s ({sim_time/total_time*100:.1f}%)")
    print(f"Steps per second: {num_steps / sim_time:.2f}")
    print(f"Force calculations: {num_bodies * (num_bodies - 1) // 2 * num_steps:,}")
    print(f"FLOPS (estimate): {num_bodies * (num_bodies - 1) * 20 * num_steps / sim_time:.3e}")

    return {
        'num_bodies': num_bodies,
        'num_steps': num_steps,
        'total_time': total_time,
        'init_time': init_time,
        'sim_time': sim_time,
        'steps_per_sec': num_steps / sim_time,
        'energy_initial': total_initial,
        'energy_final': total_final,
        'energy_error_percent': energy_error
    }

if __name__ == "__main__":
    num_bodies = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    num_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    dt = float(sys.argv[3]) if len(sys.argv) > 3 else 86400.0

    result = run_simulation(num_bodies, num_steps, dt)

    # Save benchmark results
    if len(sys.argv) > 4 and sys.argv[4] == '--save':
        with open('python_benchmark.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nBenchmark results saved to python_benchmark.json")
