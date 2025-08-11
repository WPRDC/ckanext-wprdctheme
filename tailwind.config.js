const colors = require("tailwindcss/colors");
// const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./ckanext/wprdctheme/**/*.{html,js}"],
    darkMode: "media", // or 'media' or 'class'
    theme: {
        // use same breakpoints as CKAN/bootstrap
        screens: {
            'sm': '576px',
            'md': '768px',
            'lg': '992px',
            'xl': '1200px',
            '2xl': '1300px',
        },
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
                wprdc: {
                    "50": "#FEFDE8",
                    "100": "#FEFDC3",
                    "200": "#FDF68B",
                    "300": "#FCEC52", // primary color
                    "400": "#F9DA16",
                    "500": "#E9C109",
                    "600": "#C99705",
                    "700": "#A06C08",
                    "800": "#84550F",
                    "900": "#704513",
                    "950": "#422406",
                },
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
