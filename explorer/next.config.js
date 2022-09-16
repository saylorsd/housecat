/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  typescript: {
    // todo: check back to see if type issues are fixed in react-map-gl
    ignoreBuildErrors: true,
  },
  output: 'standalone',
};

module.exports = nextConfig;
