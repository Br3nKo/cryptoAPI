# Use Node.js as the base image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Build the frontend
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Serve the frontend using a simple HTTP server
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]