// vue.config.js
const webpack = require('webpack');

module.exports = {
  // Other configuration options...

  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        __VUE_OPTIONS_API__: JSON.stringify(true),
        // Add other flags as needed
      })
    ]
  }
};
