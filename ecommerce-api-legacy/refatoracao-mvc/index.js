const { app, initDb } = require('./src/app');
const env = require('./src/config/env');

async function start() {
  try {
    await initDb();
    console.log('Database synced and seeded.');

    app.listen(env.port, () => {
      console.log(`API refatorada rodando na porta ${env.port}...`);
      console.log(`Documentação disponível em http://localhost:${env.port}/swagger-ui`);
    });
  } catch (error) {
    console.error('Failed to start the application:', error);
    process.exit(1);
  }
}

start();
