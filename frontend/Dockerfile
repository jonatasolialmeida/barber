# Fase de build
FROM node:18-alpine as build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm install

# Copiar o código-fonte do frontend
COPY . .

# Gerar os arquivos para produção
RUN npm run build

# Fase final: produção
FROM node:18-alpine as production

# Definir o diretório de trabalho
WORKDIR /app

# Copiar somente os arquivos necessários para o container de produção
COPY --from=build /app ./

# Expor a porta em que o Next.js irá rodar
EXPOSE 3000

# Iniciar o Next.js
CMD ["npm", "start"]
