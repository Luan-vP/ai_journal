# Use an official Node.js runtime as the base image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json .

# Install app dependencies
RUN npm install

# Copy the Svelte app files to the working directory
COPY . .

# Build the Svelte app
RUN npm run build

# Expose the port that the app will run on
EXPOSE 5173

# Define the command to start the app
CMD [ "npm", "run", "dev" ]
