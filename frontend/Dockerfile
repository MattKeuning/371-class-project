FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PATH /app/node_modules/.bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV HOST 0.0.0.0
EXPOSE 3000
ENTRYPOINT []
CMD ["npm", "run", "dev"]