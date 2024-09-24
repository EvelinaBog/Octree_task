import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class OctreeNode:
    def __init__(self, center, size):
        self.center = tuple(center)
        self.size = size
        self.children = [None] * 8
        self.sphere = self.create_sphere()
        self.points = [self.center]  # First point of the center

    def calculate_octant_centers(self):
        half_size = self.size / 2
        cx, cy, cz = self.center

        octant_centers = [
            (cx + half_size / 2, cy + half_size / 2, cz + half_size / 2),
            (cx + half_size / 2, cy + half_size / 2, cz - half_size / 2),
            (cx + half_size / 2, cy - half_size / 2, cz + half_size / 2),
            (cx + half_size / 2, cy - half_size / 2, cz - half_size / 2),
            (cx - half_size / 2, cy + half_size / 2, cz + half_size / 2),
            (cx - half_size / 2, cy + half_size / 2, cz - half_size / 2),
            (cx - half_size / 2, cy - half_size / 2, cz + half_size / 2),
            (cx - half_size / 2, cy - half_size / 2, cz - half_size / 2),
        ]

        return octant_centers

    def create_sphere(self):
        radius = self.size / 2
        return {'center': self.center, 'radius': radius}

    def is_point_in_sphere(self, point):
        cx, cy, cz = self.sphere['center']
        px, py, pz = point
        distance_square = math.sqrt((px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2)
        return distance_square <= (self.sphere['radius'] ** 2)

    def check_octant_centers(self):
        octant_centers = self.calculate_octant_centers()  # Calculate octant centers for current size

        for octant_center in octant_centers:
            # Check if the point is inside the sphere
            if self.is_point_in_sphere(octant_center):
                self.points.append(octant_center)
            else:
                print(f"Octant center {octant_center} is outside the sphere.")

    def subdivide_and_check(self):
        if self.size <= 1:
            print("Cube size is 1 or smaller, stopping subdivision.")
            return

        print(f"Current cube size: {self.size}, centers: {self.points}")

        # Check if the current center is inside the sphere
        if not self.is_point_in_sphere(self.center):
            print(f"Center {self.center} is outside the sphere. Stopping.")
            return

        # Octant center check
        self.check_octant_centers()

        if len(self.points) <= 1:
            print("No valid octant centers remain inside the sphere.")
            return

        # Subdivide into 8 child cubes
        octant_centers = self.calculate_octant_centers()
        for i, octant_center in enumerate(octant_centers):
            if self.is_point_in_sphere(octant_center):
                # Create a child node with half the size and centered at the octant center
                self.children[i] = OctreeNode(octant_center, self.size / 2)
                print(f"Subdividing at octant center {octant_center} with size {self.size / 2}")
                self.children[i].subdivide_and_check()

    def print_points(self):
        print("Valid points inside the sphere:", self.points)

    def extract_points(self):
        # Extract points from this node and its children
        points = self.points[:]
        for child in self.children:
            if child:
                points.extend(child.extract_points())
        return points

    def visualize(self, ax):
        cx, cy, cz = self.sphere['center']
        radius = self.sphere['radius']

        # Create a grid for the main sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = cx + radius * np.outer(np.cos(u), np.sin(v))
        y = cy + radius * np.outer(np.sin(u), np.sin(v))
        z = cz + radius * np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color='b', alpha=0.1, label='Main Sphere')

        points = np.array(self.extract_points())
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='r', s=50)

        for child in self.children:
            if child:
                child.visualize(ax)

        # Set the axis limits
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-3, 3])

        ax.set_title("Octree Visualization")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")


class Octree:
    def __init__(self, boundary):
        self.root = OctreeNode(boundary['center'], boundary['size'])

    def insert(self, point):
        pass


boundary = {'center': (0, 0, 0), 'size': 2}  # Change size for bigger cube and more spheres
octree = Octree(boundary)
octree.root.subdivide_and_check()
octree.root.print_points()

# Visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
octree.root.visualize(ax)
plt.show()
