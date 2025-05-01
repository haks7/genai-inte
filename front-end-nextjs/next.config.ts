module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/vehicle-optimization",
        destination: "http://127.0.0.1:5000/api/vehicle-optimization",
      },
    ];
  },
};