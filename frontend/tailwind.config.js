/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0D664F',   // ពណ៌បៃតងគោលរបស់ CarPark
        secondary: '#056669',
        info: '#2563EB',
        success: '#16A34A',
        warning: '#F59E0B',
        danger: '#DC2626',
        light: '#F3F4F6',
        dark: '#1F2937'
      },
      fontFamily: {
        sans: ['Inter', 'Khmer OS Siemreap', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
