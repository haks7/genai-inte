const BACKEND_URL = process.env.BACKEND_URL;

module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/vehicle-optimization",
        destination: `${BACKEND_URL}/api/vehicle-optimization`,
      },
      {
        source: "/api/vehicle-security",
        destination: `${BACKEND_URL}/api/vehicle-security`,
      },
    ];
  },
};