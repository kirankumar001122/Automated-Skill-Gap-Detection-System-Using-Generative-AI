/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination:
          'https://automated-skill-gap-detection-system.onrender.com/api/v1/:path*',
      },
      {
        source: '/health',
        destination:
          'https://automated-skill-gap-detection-system.onrender.com/health',
      },
    ];
  },
};

module.exports = nextConfig;