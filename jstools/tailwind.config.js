module.exports = {
    future: {
        removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    purge: {
        enabled: false, //true for production build
        content: [
            '../**/templates/*.html',
            '../**/templates/**/*.html'
        ]
    },
    theme: {
        flexGrow:{
                '0': 0,
                DEFAULT: 2,
                '1': 1,
        }
    }
    ,
    variants: {},
    plugins: [],
}