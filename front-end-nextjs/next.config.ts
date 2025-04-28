module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/query",
        destination: "http://127.0.0.1:5000/api/query",
      },
    ];
  },
};