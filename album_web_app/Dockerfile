# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install express and compression middleware
RUN npm install express compression

# Copy built assets from build stage
COPY --from=build /app/dist ./dist

# Copy server file
COPY server.js .

# Expose port 3000
EXPOSE 3000

CMD ["node", "server.js"]
