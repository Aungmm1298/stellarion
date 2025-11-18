/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./admin-3d-manager.html",
    "./debug-products.html",
    "./test-3d-generator.html",
    "./how-to-get-image-urls.html",
    "./script.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1a1f3a',
        secondary: '#ff6b6b',
        accent: '#4ecdc4',
        luxury: '#ffd93d',
        dark: '#0f1419',
        light: '#f8f9fa'
      },
      fontFamily: {
        sans: ['Poppins', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
