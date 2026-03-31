import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "goldneuron.io",
      },
    ],
  },
};

export default nextConfig;
