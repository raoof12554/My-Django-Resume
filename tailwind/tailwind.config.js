/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/templates/**/*.html", 
    "./**/*.html",            
    "./**/*.js",               
    "./**/*.py",              
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Vazir', 'sans-serif'],
      },
    },
  },
  plugins: [],
}