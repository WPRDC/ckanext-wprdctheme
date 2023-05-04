const colors = require("tailwindcss/colors");
// const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./ckanext/wprdc_theme/**/*.{html,js}"],
  darkMode: "media", // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: ["Public Sans", "Arial", "sans-serif"],
        mono: ['"JetBrains Mono"', "monospace"],
      },
      colors: {
        primary: "#FCEC52",
        secondary: colors.cyan,
        background: colors.cyan,
        focused: colors.cyan,
        error: colors.red,
        warning: colors.orange,
        text: "#181818",
        textSecondary: "#52525B",
      },
      maxHeight: {
        "1/4": "25%",
        "1/2": "50%",
        "3/4": "75%",
      },
      boxShadow: {
        sm: "2px 2px 0 rgba(0,0,0,0.5)",
        DEFAULT: "3px 3px 0 rgba(0,0,0,0.5)",
        md: "4px 4px 0 rgba(0,0,0,0.5)",
        lg: "5px 5px 0 rgba(0,0,0,0.5)",
        xl: "6px 6px 0 rgba(0,0,0,0.5)",
        "2xl": "8px 8px 0 rgba(0,0,0,0.5)",
        "sm-reverse": "-2px -2px 0 rgba(0,0,0,0.5)",
        reverse: "-3px -3px 0 rgba(0,0,0,0.5)",
        "md-reverse": "-4px -4px 0 rgba(0,0,0,0.5)",
        "lg-reverse": "-5px -5px 0 rgba(0,0,0,0.5)",
        "xl-reverse": "-6px -6px 0 rgba(0,0,0,0.5)",
        "2xl-reverse": "-8px -8px 0 rgba(0,0,0,0.5)",
        inner: "2px 2px 0 #cbd5e1 inset",
        none: "none",
      },
    },
  },
  plugins: [],
};
