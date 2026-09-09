FROM node:20-alpine
WORKDIR /repo
COPY packages/page-builder ./packages/page-builder
COPY apps/web ./apps/web
WORKDIR /repo/apps/page-builder
COPY apps/page-builder ./
RUN npm ci --no-audit --no-fund
EXPOSE 3002
CMD ["npm", "run", "dev"]
