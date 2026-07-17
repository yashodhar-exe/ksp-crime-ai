# Build stage
FROM node:20-slim AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG VITE_API_BASE_URL=http://localhost:8000/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY deployment/nginx/frontend.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
