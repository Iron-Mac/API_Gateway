FROM node:16

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Build the Vue app
RUN npm run build

# Make port 80 available to the world outside this container
EXPOSE 8080
EXPOSE 5173

# Serve the Vue app with a simple HTTP server
CMD ["npm", "run", "dev"]

