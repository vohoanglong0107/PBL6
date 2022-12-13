FROM node:16.18.1-alpine3.17 AS builder
RUN apk add --no-cache libc6-compat=1.2.3-r4 && apk update
# Set working directory
WORKDIR /app
RUN npm i -g turbo@1.6.3
COPY . .
RUN turbo prune --scope=web --docker
 
# Add lockfile and package.json's of isolated subworkspace
FROM node:16.18.1-alpine3.17 AS runner
RUN apk add --no-cache libc6-compat=1.2.3-r4 && apk update
WORKDIR /app
 
# First install the dependencies (as they change less often)
COPY .gitignore .gitignore
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/package-lock.json ./
RUN npm install
 
# Build the project
COPY --from=builder /app/out/full/ .
COPY turbo.json turbo.json
RUN npx turbo run build --filter=web...
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

USER nextjs
ENV NODE_ENV production

CMD ["npm", "run", "start", "-w", "web"]
