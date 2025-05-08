# Use a lightweight Node.js image
FROM node:18-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the frontend files to the container
COPY . .

# Build the Next.js app
RUN npm run build

# Use a lightweight web server for serving the built app
FROM nginx:alpine

# Copy the built app from the builder stage
COPY --from=builder /app/out /usr/share/nginx/html

# Expose the port the app runs on
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]