FROM node:20-alpine
WORKDIR /repo/apps/web
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
COPY apps/web/package.json apps/web/package-lock.json apps/web/.npmrc ./
COPY packages/page-builder /repo/packages/page-builder
RUN npm ci
COPY apps/web .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]
