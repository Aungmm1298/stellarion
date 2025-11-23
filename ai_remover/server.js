// ============================================
// STELLARION - MESHY API BACKEND SERVER
// Node.js Express Server for Image-to-3D Conversion
// ============================================

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const PORT = 3000;

// Meshy API Configuration
const MESHY_API_KEY = 'msy_BO62XMcAXyvcYttvXRLCQx4OSnyKJaUHCoOG';
const MESHY_API_BASE = 'https://api.meshy.ai/openapi/v1/image-to-3d';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Serve static files

// ============================================
// MESHY API ENDPOINTS
// ============================================

/**
 * Upload image and create 3D model task
 * POST /api/create-3d-model
 * Body: { imageUrl: string, productName: string }
 */
app.post('/api/create-3d-model', async (req, res) => {
    try {
        const { imageUrl, productName } = req.body;

        console.log('Creating 3D model for:', productName);
        console.log('Image URL:', imageUrl);
        console.log('API Endpoint:', MESHY_API_BASE);

        // Create image-to-3D task
        const response = await axios.post(
            MESHY_API_BASE,
            {
                image_url: imageUrl,
                enable_pbr: true,
                ai_model: 'meshy-4',
                topology: 'quad',
                target_polycount: 30000
            },
            {
                headers: {
                    'Authorization': `Bearer ${MESHY_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        console.log('Task created:', response.data);

        res.json({
            success: true,
            taskId: response.data.result,
            message: '3D model generation started'
        });

    } catch (error) {
        console.error('========================================');
        console.error('ERROR creating 3D model:');
        console.error('Error message:', error.message);
        console.error('Response status:', error.response?.status);
        console.error('Response data:', JSON.stringify(error.response?.data, null, 2));
        console.error('========================================');
        
        // Extract detailed error message
        let errorMessage = error.message;
        if (error.response?.data) {
            if (typeof error.response.data === 'string') {
                errorMessage = error.response.data;
            } else if (error.response.data.message) {
                errorMessage = error.response.data.message;
            } else {
                errorMessage = JSON.stringify(error.response.data);
            }
        }
        
        res.status(error.response?.status || 500).json({
            success: false,
            error: errorMessage,
            details: error.response?.data
        });
    }
});

/**
 * Check 3D model generation status
 * GET /api/check-status/:taskId
 */
app.get('/api/check-status/:taskId', async (req, res) => {
    try {
        const { taskId } = req.params;

        console.log('Checking status for task:', taskId);

        const response = await axios.get(
            `${MESHY_API_BASE}/${taskId}`,
            {
                headers: {
                    'Authorization': `Bearer ${MESHY_API_KEY}`
                }
            }
        );

        console.log('Task status:', response.data.status);

        res.json({
            success: true,
            status: response.data.status,
            progress: response.data.progress,
            modelUrl: response.data.model_urls?.glb,
            thumbnailUrl: response.data.thumbnail_url,
            data: response.data
        });

    } catch (error) {
        console.error('Error checking status:', error.response?.data || error.message);
        res.status(500).json({
            success: false,
            error: error.response?.data || error.message
        });
    }
});

/**
 * Get all 3D models
 * GET /api/models
 */
app.get('/api/models', async (req, res) => {
    try {
        const response = await axios.get(
            MESHY_API_BASE,
            {
                headers: {
                    'Authorization': `Bearer ${MESHY_API_KEY}`
                },
                params: {
                    pageSize: 20,
                    pageNum: 1
                }
            }
        );

        res.json({
            success: true,
            models: response.data.result
        });

    } catch (error) {
        console.error('Error fetching models:', error.response?.data || error.message);
        res.status(500).json({
            success: false,
            error: error.response?.data || error.message
        });
    }
});

/**
 * Download 3D model GLB file
 * GET /api/download/:taskId
 */
app.get('/api/download/:taskId', async (req, res) => {
    try {
        const { taskId } = req.params;

        // Get task details
        const taskResponse = await axios.get(
            `${MESHY_API_BASE}/${taskId}`,
            {
                headers: {
                    'Authorization': `Bearer ${MESHY_API_KEY}`
                }
            }
        );

        const glbUrl = taskResponse.data.model_urls?.glb;

        if (!glbUrl) {
            return res.status(404).json({
                success: false,
                error: 'Model not ready yet'
            });
        }

        // Download the GLB file
        const fileResponse = await axios.get(glbUrl, {
            responseType: 'arraybuffer'
        });

        res.setHeader('Content-Type', 'model/gltf-binary');
        res.setHeader('Content-Disposition', `attachment; filename="model-${taskId}.glb"`);
        res.send(fileResponse.data);

    } catch (error) {
        console.error('Error downloading model:', error.response?.data || error.message);
        res.status(500).json({
            success: false,
            error: error.response?.data || error.message
        });
    }
});

// ============================================
// START SERVER
// ============================================

app.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════╗
║   STELLARION - MESHY API SERVER       ║
╚════════════════════════════════════════╝

✅ Server running on: http://localhost:${PORT}
✅ API Key configured
✅ CORS enabled
✅ Ready to convert images to 3D models!

Available endpoints:
- POST /api/create-3d-model
- GET  /api/check-status/:taskId
- GET  /api/models
- GET  /api/download/:taskId

Press Ctrl+C to stop the server
    `);
});

// Error handling
process.on('unhandledRejection', (error) => {
    console.error('Unhandled rejection:', error);
});
