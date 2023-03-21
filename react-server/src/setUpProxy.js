const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(Login) {
    Login.use('/users', createProxyMiddleware({ target: 'http://localhost:5000', changeOrigin: true }));
  };