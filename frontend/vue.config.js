module.exports = {
  devServer: {
    port: "8080",
    host: "127.0.0.1",
    disableHostCheck: true,
    proxy: {
      "^/time/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
      "^/auth/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
      "^/public/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
      "^/feed/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
      "^/data/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
      "^/account/": {
        target: "http://localhost/",
        ws: true,
        changeOrigin: true,
      },
    },
  },
};
