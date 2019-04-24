from flask_assets import Bundle

app_css = Bundle('app.scss', filters='scss', output='styles/app.css')

app_js = Bundle('app.js', filters='jsmin', output='scripts/app.js')

vendor_css = Bundle(
    'vendor/custom.css',
    'vendor/ionicons.min.css',
    output='styles/vendor.css')

vendor_js = Bundle(
    '../../../node_modules/vue/dist/vue.js',
    '../../../node_modules/buefy/dist/buefy.js',
    '../../../node_modules/superagent/superagent.js',
    '../../../node_modules/@vladocar/nanojs/src/nanoJS.js',
    'vendor/custom.js',
    filters='jsmin',
    output='scripts/vendor.js')
