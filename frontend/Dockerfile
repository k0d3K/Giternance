FROM node:24
WORKDIR /app
RUN mkdir -p ./frontend/src
COPY package.json eslint.config.js tailwind.config.js .
COPY tsconfig.json tsconfig.build.json ./frontend/
RUN npm install
COPY public ./public
COPY assets ./assets
COPY src ./frontend/src
RUN npm run format:check && npm run build
CMD ["npm", "start"]
