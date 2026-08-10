/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#EDEBE2',
        'paper-dark': '#E2DFD3',
        ink: '#16233D',
        'ink-soft': '#3C4A63',
        rule: '#D3CEBC',
        amber: {
          DEFAULT: '#C97A2E',
          soft: '#F3E3C8',
        },
        steel: {
          DEFAULT: '#2E6F8E',
          soft: '#DDE9EE',
        },
        moss: {
          DEFAULT: '#3F7D51',
          soft: '#DEEBDF',
        },
        rust: {
          DEFAULT: '#B24C34',
          soft: '#F3DED6',
        },
      },
      fontFamily: {
        display: ['Archivo', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      backgroundImage: {
        perf: 'radial-gradient(circle, #EDEBE2 2.5px, transparent 2.5px)',
      },
    },
  },
  plugins: [],
}
