# FROM node:22

# WORKDIR /app

# COPY client/package*.json ./
# RUN npm install

# COPY client/ .
# COPY .env .

# RUN npm run build

# EXPOSE 3000
# CMD ["npm", "run", "start"]

# Stage 1: Build
FROM node:22-alpine AS builder

WORKDIR /app

COPY client/package*.json ./
RUN npm install

COPY client/ .
RUN npm run build

# Stage 2: Production image
FROM node:22-alpine

WORKDIR /app

COPY --from=builder /app ./

EXPOSE 3000

ENV NODE_ENV=production

CMD ["npm", "run", "start"]
