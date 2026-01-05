# source : https://www.geeksforgeeks.org/devops/how-to-dockerize-a-reactjs-app/
# source : https://dev.to/rakib-dev/effortlessly-dockerize-your-vite-react-application-5bid
# source : https://thedkpatel.medium.com/dockerizing-react-application-built-with-vite-a-simple-guide-4c41eb09defa

# Use an official node image as the base image, updated to version 25
FROM node:25-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm install

COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Command to run the application
CMD ["npm", "run", "dev"]
