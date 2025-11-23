# 3D Models Folder

## How to Add Your Own 3D Models

### Step 1: Get Your 3D Model
1. Download your GLB or GLTF file (from Meshy.ai, Sketchfab, etc.)
2. Save it to this `models` folder

### Step 2: Update the Product in script.js
Find the product in the `products` array and update the `model3D` path:

```javascript
{
    id: 1,
    name: "Luxury Velvet Sofa",
    price: 899,
    category: "living-room",
    image: "https://i.imgur.com/K8ZqY9m.jpeg",
    model3D: "models/your-model-name.glb",  // ← Update this
    description: "Premium 3-seater sofa with plush velvet upholstery"
}
```

### Step 3: Test
1. Open index.html in a browser
2. Click "View in 3D" on the product
3. Your 3D model should load!

## Supported Formats
- ✅ GLB (recommended - single file)
- ✅ GLTF (with textures)

## Where to Get 3D Models
- **Meshy.ai** - AI-generated 3D models
- **Sketchfab** - Download free models
- **Poly Pizza** - Free 3D models
- **KhronosGroup** - Sample models

## Example File Structure
```
Stellarion(Hylife)/
├── models/
│   ├── sofa.glb
│   ├── chair.glb
│   └── table.glb
├── index.html
└── script.js
```

## Current Setup
- ✅ Using demo model from CDN (Astronaut.glb)
- 📁 Add your GLB files here to replace it
- 🔄 Update script.js to point to your files
