import math

class OctreeNode:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.points = []  # List to store points in this node
        self.children = [None] * 8  # Placeholder for child nodes
        self.sphere = self.create_sphere()

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

    def check_octant_centers(self):
        octant_centers = self.calculate_octant_centers()
        radius = self.sphere['radius']
        cx, cy, cz = self.center

        for octant_center in octant_centers:
            ox, oy, oz = octant_center
            distance_square = math.sqrt((ox - cx) ** 2 + (oy - cy) ** 2 + (oz - cz) ** 2)
            radius_square = radius ** 2

            if distance_square <= radius_square:
                self.points.append(octant_center)
            else:
                print(f"Octant center {octant_center} is outside the sphere.")

    def print_points(self):
        print("Points in this node:", self.points)


class Octree:
    def __init__(self, boundary):
        self.root = OctreeNode(boundary['center'], boundary['size'])

    def insert(self, point):
        pass


boundary = {'center': (0, 0, 0), 'size': 2}
octree = Octree(boundary)  # Create the Octree with the boundary
octree.root.check_octant_centers()  # Check the octant centers
octree.root.print_points()  # Print the points in the root node
