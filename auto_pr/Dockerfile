FROM node

WORKDIR /auto_pr

COPY package.json package-lock.json ./
RUN npm install

COPY index.js .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/auto_pr/entrypoint.sh" ]