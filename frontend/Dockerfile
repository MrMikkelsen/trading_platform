FROM node:16-alpine as build

#COPY package*.json ./

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
#build stage
RUN npm run build

FROM nginx:latest as production-stage
RUN mkdir /app
COPY --from=build /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf