export const ENV = {
    development: {
      API_BASE_URL: "http://localhost:5500",
    },
    staging: {
      API_BASE_URL: "https://staging.example.com",
    },
    production: {
      API_BASE_URL: "http://localhost:5500",
    },
  };
  
  // Detect environment
  export const CONFIG =
    process.env.NODE_ENV === "production"
      ? ENV.production
      : process.env.NODE_ENV === "staging"
      ? ENV.staging
      : ENV.development;