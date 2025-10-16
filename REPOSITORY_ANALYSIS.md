# SpecklePy Repository Analysis

## Overview

**SpecklePy** is the official Python SDK for [Speckle](https://speckle.systems), the first AEC (Architecture, Engineering, Construction) data hub that connects with your favorite AEC tools. This repository provides a comprehensive Python interface for interacting with Speckle servers, manipulating 3D geometric data, and building automation workflows.

## Repository Structure

The repository is organized into three main packages:

### 1. `specklepy` - Core Python SDK
Located in `src/specklepy/`, this is the main Python package that provides:

#### API Components (`src/specklepy/api/`)
- **SpeckleClient**: Your entry point for interacting with Speckle Server's GraphQL API
- **Operations**: Core send/receive functionality for data synchronization  
- **Credentials**: Authentication and account management
- **Resources**: Access to projects, models, versions, and other Speckle entities

#### Objects System (`src/specklepy/objects/`)
- **Base**: Foundation class for all Speckle objects with automatic serialization
- **Geometry**: Comprehensive 3D geometry objects (Points, Lines, Meshes, Surfaces, etc.)
- **Primitive**: Basic data types (Intervals, etc.)
- **Models**: Supporting data structures (Units, Collections)

#### Core Services (`src/specklepy/core/`)
- Low-level API handling and transport mechanisms
- Serialization/deserialization logic
- Helper utilities

#### Transport Layer (`src/specklepy/transports/`)
- Abstract transport interface
- Local caching mechanisms
- Network transport implementations

### 2. `speckle_automate` - Automation Framework  
Located in `src/speckle_automate/`, this package provides:
- **AutomationContext**: Framework for building Speckle automation functions
- **Runner**: Execution environment for automation workflows
- **Schema**: Data validation and structure definitions

### 3. `speckleifc` - IFC Integration
Located in `src/speckleifc/`, this package offers:
- **IFC Import/Export**: Integration with Industry Foundation Classes format
- **Geometry Processing**: IFC-specific geometric operations
- **Property Extraction**: Building information modeling data extraction
- **OpenShell Integration**: Leverage the IfcOpenShell library for IFC operations

## Key Features

### 1. 3D Geometry Handling
SpecklePy provides a rich set of geometric primitives:

```python
from specklepy.objects.geometry.point import Point
from specklepy.objects.geometry.line import Line
from specklepy.objects.models.units import Units

# Create geometric objects with proper units
point1 = Point(x=1.0, y=2.0, z=3.0, units=Units.m)
point2 = Point(x=4.0, y=5.0, z=6.0, units=Units.m)
line = Line(start=point1, end=point2, units=Units.m)

print(f"Line length: {line.length}")  # Calculated automatically
```

Available geometry types:
- **Point, Vector**: Basic 3D positioning and direction
- **Line, Polyline, Polycurve**: Linear geometry
- **Arc, Circle, Ellipse**: Curved geometry  
- **Plane, Surface**: 2D surfaces
- **Mesh, PointCloud**: Complex 3D geometry
- **Box**: 3D bounding volumes

### 2. Data Synchronization
Send and receive data to/from Speckle servers:

```python
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper

# Connect to a Speckle stream
stream_url = "https://app.speckle.systems/streams/[stream-id]"
wrapper = StreamWrapper(stream_url)
transport = wrapper.get_transport()

# Receive data from server
received_object = operations.receive("[object-id]", transport)

# Send data to server  
sent_object_id = operations.send(my_object, [transport])
```

### 3. Custom Object Creation
Extend Speckle's object system with your own types:

```python
from specklepy.objects import Base

class CustomBuildingElement(Base, speckle_type="Custom.Building.Element"):
    name: str = ""
    material: str = "concrete"
    strength: float = 0.0
    
    # Custom methods
    def calculate_load_capacity(self):
        return self.strength * 1.5
```

### 4. Server API Integration
Full access to Speckle server functionality:

```python
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account

# Connect to server
client = SpeckleClient(host="app.speckle.systems")
account = get_default_account()
client.authenticate_with_account(account)

# Work with projects and models
projects = client.project.get_all()
new_project = client.project.create(name="My Project")
```

### 5. Automation Framework
Build automated workflows with Speckle Automate:

```python
from speckle_automate import AutomationContext

def my_automation_function(context: AutomationContext):
    # Access input data
    speckle_objects = context.receive_version()
    
    # Process data
    for obj in speckle_objects:
        # Perform analysis, validation, or transformation
        pass
    
    # Report results
    context.mark_run_success("Processing completed successfully")
```

### 6. IFC Integration
Work with Industry Foundation Classes (IFC) files:

```python
# Note: Requires optional 'speckleifc' dependencies
from speckleifc import IfcImporter

# Import IFC file to Speckle objects
importer = IfcImporter("building.ifc")
speckle_objects = importer.to_speckle()

# Process building elements
for element in speckle_objects:
    if hasattr(element, 'properties'):
        # Access BIM properties
        pass
```

## What You Can Do With This Repository

### For AEC Professionals:
1. **Data Interoperability**: Exchange 3D models between different AEC software tools
2. **Version Control**: Track changes in building models over time
3. **Collaboration**: Share and synchronize design data across teams
4. **Analysis**: Extract geometric and semantic information from BIM models
5. **Reporting**: Generate automated reports from building data

### For Developers:
1. **Custom Integrations**: Build plugins for your favorite AEC software
2. **Automation**: Create scripts to automate repetitive modeling tasks  
3. **Data Processing**: Build pipelines for large-scale geometric data processing
4. **Web Applications**: Develop web-based viewers and editors for 3D models
5. **Analysis Tools**: Create specialized analysis and simulation tools

### For Researchers:
1. **Algorithm Development**: Test new geometric algorithms on real building data
2. **Machine Learning**: Train models on large datasets of architectural geometry
3. **Performance Analysis**: Study building performance using geometric and semantic data
4. **Visualization**: Create advanced 3D visualizations and rendering

## Installation and Setup

1. **Basic Installation**:
   ```bash
   pip install specklepy
   ```

2. **With IFC Support**:
   ```bash
   pip install specklepy[speckleifc]
   ```

3. **Development Setup**:
   ```bash
   # Using UV (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

4. **Authentication**:
   - Install [Speckle Manager](https://speckle.guide/#speckle-manager)
   - Add your Speckle account
   - Use `get_default_account()` to authenticate

## Development Environment

- **Python Version**: Requires Python 3.10+
- **Package Manager**: Uses UV for dependency management (can fallback to pip)
- **Testing**: pytest framework for unit and integration tests
- **Code Quality**: pre-commit hooks with ruff linting
- **Documentation**: Available at [speckle.guide](https://speckle.guide/dev/python.html)

## Key Dependencies

- **pydantic**: Data validation and serialization
- **httpx**: Modern HTTP client for API communication  
- **gql**: GraphQL client for Speckle API interaction
- **attrs**: Enhanced class definitions
- **ujson**: Fast JSON processing
- **ifcopenshell** (optional): IFC file processing

## Community and Support

- **Documentation**: https://speckle.guide/dev/python.html
- **Community Forum**: https://speckle.community
- **GitHub Issues**: For bug reports and feature requests
- **Examples**: Check the `example/` directory for usage patterns

This repository represents a comprehensive toolkit for working with 3D geometric data in the AEC industry, providing both low-level geometric primitives and high-level integration with the Speckle ecosystem.