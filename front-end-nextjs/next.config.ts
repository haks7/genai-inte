// filepath: c:\Users\supandi\prod_ready_littlebits\littlebits\front-end-nextjs\next.config.ts
const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:5000";

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