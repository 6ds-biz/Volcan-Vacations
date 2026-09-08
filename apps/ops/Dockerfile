FROM node:20-alpine
WORKDIR /repo/apps/ops
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
COPY apps/ops/package.json apps/ops/package-lock.json* apps/ops/.npmrc ./
COPY packages/page-builder /repo/packages/page-builder
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi
COPY apps/ops .
RUN npm run build
EXPOSE 3001
CMD ["npm", "run", "start"]
