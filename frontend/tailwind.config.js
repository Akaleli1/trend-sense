/** @type {import('tailwindcss').Config} */
module.exports = {
  // CONTENT kısmı zaten doğru, dokunmuyoruz.
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}', // SRC klasörünü de ekleyelim, garanti olsun
  ],
  theme: {
    extend: {
      // SADECE uzatma (extend) yapıyoruz, default renkleri ezmiyoruz.
      // Bu, hem senin primary rengini hem de Tailwind'in slate/green/red renklerini aktif tutar.
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [],
}