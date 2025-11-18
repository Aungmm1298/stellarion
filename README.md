# 🪑 Stellarion - Luxury Furniture E-Commerce with 3D AI Generation

A premium furniture e-commerce website featuring **AI-powered 3D model generation** from product images.

![Stellarion](https://img.shields.io/badge/Stellarion-Luxury%20Furniture-2D3E50?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

---

## ✨ Features

### � **E-Commerce Core**
- ✅ Full shopping cart with localStorage persistence
- ✅ Wishlist system with dedicated modal
- ✅ User authentication (login, register, logout)
- ✅ Product search and category filtering
- ✅ Dual currency display (USD/THB at 1:35 rate)
- ✅ Responsive design (mobile, tablet, desktop)

### 🎨 **Premium Design**
- ✅ Navy (#2D3E50) and Gold (#E8B86D) luxury theme
- ✅ Playfair Display & Lato font pairing
- ✅ Smooth animations and transitions
- ✅ Professional product cards
- ✅ Hero section with gradient overlay

### 🎯 **3D Visualization**
- ✅ Three.js-powered 3D product viewer
- ✅ GLB/GLTF model support
- ✅ Professional lighting (ambient, directional, hemisphere)
- ✅ OrbitControls with auto-rotation
- ✅ Modal 3D viewer with auto-scaling

### 🤖 **AI Model Generation** (NEW!)
- ✅ **Meshy.ai API integration**
- ✅ Convert product images to 3D models
- ✅ Real-time progress tracking
- ✅ Admin panel with cube icon
- ✅ Model preview and download
- ✅ Direct browser integration (no backend needed)

---

## 🚀 Quick Start

### 1. Open the Website
Simply open `index.html` in your browser. No server setup required!

### 2. Test the 3D Generator
1. Click the **cube icon (🧊)** in the navigation
2. Enter a product name and image URL
3. Click "Generate 3D Model"
4. Wait 2-5 minutes for completion
5. Preview or download your 3D model!

### 3. Test API Connection
Open `test-meshy-api.html` in your browser to verify the Meshy API is working correctly.

---

## 📁 Project Structure

```
Stellarion(Hylife)/
├── index.html              # Main website
├── script.js               # All JavaScript logic
├── test-meshy-api.html     # API testing tool
├── MESHY_API_GUIDE.md      # Complete API guide
├── README.md               # This file
├── 3d model/               # 3D model files
│   └── sectional sofa 3d model.glb
├── models/                 # Additional models
│   └── README.md
├── server.js               # Node.js backend (optional)
└── package.json            # Node.js config (optional)
```

---

## 🔧 Technologies

### Frontend
- **HTML5**: Semantic structure
- **TailwindCSS v3.x**: Utility-first styling via CDN
- **JavaScript ES6+**: Modern vanilla JS
- **Three.js r128**: 3D rendering engine
- **Font Awesome 6**: Icon library

### 3D Rendering
- **GLTFLoader**: Load GLB/GLTF models
- **OrbitControls**: Camera interaction
- **PBR Materials**: Realistic rendering
- **Auto-scaling**: Adaptive model sizing

### AI Integration
- **Meshy.ai API v2**: Image-to-3D conversion
- **Direct REST API**: No backend required
- **Real-time polling**: Progress tracking
- **CDN delivery**: Fast model downloads

---

## 🎮 How to Use

### Shopping Experience
1. **Browse Products**: Scroll through luxury furniture
2. **Filter by Room**: Click room categories (Living, Bedroom, Office)
3. **View in 3D**: Click "View in 3D" on any product
4. **Add to Cart**: Click shopping bag icon
5. **Wishlist**: Click heart icon to save favorites
6. **Checkout**: View cart and proceed (demo only)

### 3D Model Generation
1. **Open Admin Panel**: Click cube icon in navbar
2. **Enter Details**:
   - Product Name: "Modern Leather Sofa"
   - Image URL: Direct link to product photo
3. **Generate**: Click button and wait
4. **Monitor**: Watch real-time progress bar
5. **Download**: Save GLB file when complete
6. **Preview**: View in built-in 3D viewer
7. **Add to Products**: Use in your catalog

---

## 🔑 API Configuration

### Meshy.ai Setup
```javascript
const API_KEY = 'kiri_oZ9V44rQlpQrD5lG8nLZs0fJLlwxBssAU6nRqtkuKUM';
const MESHY_API_URL = 'https://api.meshy.ai/v2';
```

### Model Parameters
- **AI Model**: meshy-4 (latest generation)
- **Topology**: quad (clean geometry)
- **Polycount**: 30,000 triangles
- **PBR**: Enabled (realistic materials)
- **Format**: GLB (optimized binary)

---

## 📊 Product Catalog

Currently featuring **15 luxury furniture items**:

### 🛋️ Living Room (5)
- Luxury Velvet Sectional Sofa ($2,499) ⭐ **Has 3D Model**
- Mid-Century Modern Armchair ($899)
- Scandinavian Coffee Table ($599)
- Industrial TV Stand ($799)
- Modern Floor Lamp ($299)

### 🛏️ Bedroom (5)
- Contemporary Platform Bed ($1,899)
- Tufted Upholstered Headboard ($699)
- Elegant Nightstand Set ($799)
- Vintage Dresser ($1,299)
- Luxury Wardrobe ($2,199)

### 💼 Office (5)
- Executive Leather Desk Chair ($1,299)
- Minimalist Standing Desk ($1,499)
- Modern Bookshelf Unit ($899)
- Designer Office Cabinet ($1,099)
- Ergonomic Task Chair ($699)

---

## 🐛 Troubleshooting

### 3D Model Not Loading
- ✅ Check file exists in `3d model` folder
- ✅ Verify path uses URL encoding (%20 for spaces)
- ✅ Ensure GLB file is valid
- ✅ Check browser console for errors

### Meshy API Errors
- ✅ Verify API key is correct
- ✅ Check image URL is publicly accessible
- ✅ Ensure you haven't exceeded rate limits
- ✅ Test with `test-meshy-api.html`

---

## 📚 Documentation

- **API Guide**: [MESHY_API_GUIDE.md](MESHY_API_GUIDE.md) - Complete Meshy API integration guide
- **Meshy Docs**: https://docs.meshy.ai/
- **Three.js Docs**: https://threejs.org/docs/
- **TailwindCSS**: https://tailwindcss.com/docs

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Backend server for secure API key management
- [ ] Image upload from device (vs URL only)
- [ ] Batch 3D model generation
- [ ] Payment integration
- [ ] Order management system
- [ ] Admin product management
- [ ] Customer reviews and ratings

### 3D Improvements
- [ ] Augmented Reality (AR) view
- [ ] 360° product spin
- [ ] Model annotation and measurements
- [ ] Material swatching
- [ ] Room preview

---

## 🎉 Getting Started (Step-by-Step)

1. **Open Website**
   ```
   Open index.html in your browser
   ```

2. **Browse Products**
   ```
   Scroll through the catalog
   Click on products to see details
   ```

3. **Test 3D Viewer**
   ```
   Click "View in 3D" on Luxury Velvet Sectional Sofa
   Interact with the 3D model
   ```

4. **Test Shopping Cart**
   ```
   Add items to cart
   View cart modal
   Update quantities
   ```

5. **Test 3D Generator**
   ```
   Click cube icon in navbar
   Enter: "Modern Sofa"
   URL: https://images.unsplash.com/photo-1555041469-a586c61ea9bc
   Click "Generate 3D Model"
   Wait for completion (2-5 min)
   Download or preview result
   ```

6. **Run API Test**
   ```
   Open test-meshy-api.html
   Click "List All Models" to see previous generations
   Test new generation with sample data
   ```

---

## 📞 Support

For issues or questions:
1. Check [MESHY_API_GUIDE.md](MESHY_API_GUIDE.md)
2. Run `test-meshy-api.html` for diagnostics
3. Check browser console for errors
4. Verify API key and limits at https://app.meshy.ai/

---

**Built with ❤️ and AI-powered 3D generation**
