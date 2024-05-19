# Utiliser une image de base officielle Node.js pour construire l'application
FROM node:14 AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application
COPY . .

# Construire l'application pour la production
RUN npm run build

# Utiliser une image de base Nginx pour servir l'application
FROM nginx:alpine

# Copier les fichiers construits vers le répertoire de Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 80

# Définir la commande pour démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
