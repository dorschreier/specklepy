#!/usr/bin/env python3
"""
Comprehensive SpecklePy Demo

This example demonstrates the key features and capabilities of SpecklePy:
1. Creating geometric objects with proper units
2. Building complex 3D models from basic primitives  
3. Custom object types and serialization
4. Working with collections and hierarchical data
5. Basic operations for data processing

Run this script to see SpecklePy in action!
"""

import sys
import math
from pathlib import Path

# Add src to path for development
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from specklepy.objects.geometry.point import Point
from specklepy.objects.geometry.line import Line  
from specklepy.objects.geometry.mesh import Mesh
from specklepy.objects.geometry.box import Box
from specklepy.objects.geometry.circle import Circle
from specklepy.objects.geometry.plane import Plane
from specklepy.objects.geometry.vector import Vector
from specklepy.objects.models.units import Units
from specklepy.objects import Base
from specklepy.api import operations


class BuildingFloor(Base, speckle_type="Demo.Building.Floor"):
    """Custom Speckle object representing a building floor"""
    
    name: str = "Unnamed Floor"
    level: float = 0.0
    area: float = 0.0
    elements: list = None
    
    def __post_init__(self):
        """Initialize after dataclass creation"""
        if self.elements is None:
            self.elements = []
    
    def add_element(self, element):
        """Add a building element to this floor"""
        if self.elements is None:
            self.elements = []
        self.elements.append(element)
        
    def calculate_total_area(self):
        """Calculate total area of all elements"""
        total = self.area
        if self.elements:
            for element in self.elements:
                if hasattr(element, 'area'):
                    total += element.area
        return total


class SimpleRoom(Base, speckle_type="Demo.Building.Room"):
    """A simple room representation"""
    
    name: str = "Room"
    width: float = 5.0
    length: float = 4.0
    height: float = 3.0
    units: str = Units.m.value
    
    @property 
    def area(self):
        return self.width * self.length
    
    @property
    def volume(self):
        return self.width * self.length * self.height
        

def create_basic_geometry():
    """Demonstrate basic geometric object creation"""
    print("=== Creating Basic Geometry ===")
    
    # Create points
    origin = Point(x=0.0, y=0.0, z=0.0, units=Units.m)
    corner = Point(x=10.0, y=10.0, z=5.0, units=Units.m) 
    
    print(f"Origin: {origin}")
    print(f"Corner: {corner}")
    print(f"Distance: {origin.distance_to(corner):.2f} meters")
    
    # Create a line
    line = Line(start=origin, end=corner, units=Units.m)
    print(f"Line length: {line.length:.2f} meters")
    
    # Create some vectors
    up_vector = Vector(x=0, y=0, z=1, units=Units.m)
    right_vector = Vector(x=1, y=0, z=0, units=Units.m)
    
    print(f"Up vector: {up_vector}")
    print(f"Up vector length: {up_vector.length:.2f}")
    
    return [origin, corner, line, up_vector, right_vector]


def create_building_model():
    """Create a simple building model using custom objects"""
    print("\n=== Creating Building Model ===")
    
    # Create a building floor
    ground_floor = BuildingFloor()
    ground_floor.name = "Ground Floor"
    ground_floor.level = 0.0
    ground_floor.area = 100.0  # Base floor area
    ground_floor.units = Units.m.value
    
    # Add rooms to the floor
    rooms = []
    room_specs = [
        ("Living Room", 6.0, 5.0, 3.0),
        ("Kitchen", 4.0, 3.0, 3.0),
        ("Bedroom", 4.0, 4.0, 3.0),
        ("Bathroom", 2.0, 2.0, 3.0),
    ]
    
    for name, width, length, height in room_specs:
        room = SimpleRoom()
        room.name = name
        room.width = width
        room.length = length 
        room.height = height
        rooms.append(room)
    
    for room in rooms:
        ground_floor.add_element(room)
        print(f"Added {room.name}: {room.area:.1f}m² (Volume: {room.volume:.1f}m³)")
    
    total_area = ground_floor.calculate_total_area()
    print(f"Total floor area: {total_area:.1f} square meters")
    
    # Create simple point representations for room corners
    geometry_elements = []
    
    # Create corner points for each room
    current_x = 0.0
    for room in rooms:
        corners = [
            Point(x=current_x, y=0.0, z=0.0, units=Units.m),
            Point(x=current_x + room.width, y=0.0, z=0.0, units=Units.m),
            Point(x=current_x + room.width, y=room.length, z=0.0, units=Units.m),
            Point(x=current_x, y=room.length, z=0.0, units=Units.m),
        ]
        geometry_elements.extend(corners)
        current_x += room.width + 0.5  # Small gap between rooms
    
    return ground_floor, rooms, geometry_elements


def demonstrate_serialization():
    """Show how Speckle objects can be serialized and deserialized"""
    print("\n=== Demonstrating Serialization ===")
    
    # Create a complex object
    room = SimpleRoom()
    room.name = "Demo Room"
    room.width = 8.0
    room.length = 6.0
    room.height = 3.5
    
    # Add some custom properties
    room.window_count = 3
    room.door_count = 1
    room.materials = ["concrete", "wood", "glass"]
    
    print(f"Original room: {room.name}")
    print(f"  Dimensions: {room.width}×{room.length}×{room.height}")
    print(f"  Area: {room.area:.2f}m², Volume: {room.volume:.2f}m³")
    print(f"  Windows: {room.window_count}, Doors: {room.door_count}")
    
    # Serialize to JSON
    serialized = operations.serialize(room)
    print(f"Serialized successfully (length: {len(serialized)} chars)")
    
    # Deserialize back to object
    deserialized = operations.deserialize(serialized)
    print(f"Deserialized room: {deserialized.name}")
    print(f"  Area matches: {deserialized.area == room.area}")
    print(f"  Custom properties preserved: {hasattr(deserialized, 'window_count')}")
    
    return room, deserialized


def create_mesh_example():
    """Create a simple mesh geometry"""
    print("\n=== Creating Mesh Geometry ===")
    
    # Create a simple triangular mesh (a pyramid)
    vertices = [
        0.0, 0.0, 0.0,  # Base corner 1
        5.0, 0.0, 0.0,  # Base corner 2  
        5.0, 5.0, 0.0,  # Base corner 3
        0.0, 5.0, 0.0,  # Base corner 4
        2.5, 2.5, 4.0   # Apex
    ]
    
    # Faces (triangles connecting vertices)
    faces = [
        # Base (2 triangles)
        3, 0, 1, 2,     # Base quad as triangulated
        3, 0, 2, 3,
        # Sides (4 triangles)
        3, 0, 1, 4,     # Triangle 1
        3, 1, 2, 4,     # Triangle 2
        3, 2, 3, 4,     # Triangle 3
        3, 3, 0, 4,     # Triangle 4
    ]
    
    mesh = Mesh(
        vertices=vertices,
        faces=faces,
        units=Units.m
    )
    
    print(f"Created mesh with {len(vertices)//3} vertices and {len([f for f in faces if f == 3])} triangular faces")
    print(f"Mesh area: {mesh.area:.2f} square meters")
    
    return mesh


def main():
    """Run the comprehensive demo"""
    print("SpecklePy Comprehensive Demo")
    print("=" * 50)
    
    try:
        # Demonstrate basic geometry
        basic_objects = create_basic_geometry()
        
        # Create building model
        floor, rooms, geometry = create_building_model()
        
        # Show serialization capabilities  
        original_room, restored_room = demonstrate_serialization()
        
        # Create mesh geometry
        pyramid_mesh = create_mesh_example()
        
        # Summary
        print("\n=== Demo Summary ===")
        print(f"✓ Created {len(basic_objects)} basic geometric objects")
        print(f"✓ Built a floor with {len(rooms)} rooms")
        print(f"✓ Generated {len(geometry)} geometric representations")
        print(f"✓ Demonstrated object serialization/deserialization")
        print(f"✓ Created complex mesh geometry")
        
        print("\nSpecklePy Features Demonstrated:")
        print("• 3D geometric primitives (Point, Line, Circle, Box, Mesh)")
        print("• Unit handling and geometric calculations")
        print("• Custom object types with inheritance")
        print("• Object serialization for data exchange")
        print("• Building information modeling concepts")
        print("• Complex geometry creation and manipulation")
        
        print("\nNext Steps:")
        print("• Connect to a Speckle server using SpeckleClient")
        print("• Send/receive data using operations.send() and operations.receive()")
        print("• Build automation workflows with speckle_automate")
        print("• Import/export IFC files using speckleifc")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()