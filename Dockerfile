# Use the official node image as the base
FROM node:alpine

WORKDIR /usr/app

# Copy the package files and install dependencies
COPY package*.json /usr/app

RUN npm install dotenv express cors @azure/openai

# Copy the rest of the app files
COPY server.js /usr/app
COPY .env /usr/app

# Expose the port
EXPOSE 3000

# Start the app
CMD [ "node", "/usr/app/server.js" ]
