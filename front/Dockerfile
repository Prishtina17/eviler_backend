# Use an official Node.js runtime as the base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/frontend

# Copy package.json and yarn.lock files to the working directory
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of the application code to the working directory
COPY . .

RUN yarn build
# Expose the port the app runs on
ython aEXPOSE 3000

# Define the command to run the application
CMD ["yarn", "start"]