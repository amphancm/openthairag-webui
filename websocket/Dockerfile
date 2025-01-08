# Use Node.js LTS as the base image
FROM node:lts

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all application files
COPY . .

# Expose the port the server is running on
EXPOSE 3000

# Start the application
CMD ["node", "index.js"]