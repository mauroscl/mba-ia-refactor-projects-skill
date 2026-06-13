const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const path = require('path');

const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const models = require('./models');

const app = express();

app.use(express.json());

// Swagger
const swaggerDocument = YAML.load(path.join(__dirname, '../openapi.yaml'));
app.use('/swagger-ui', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Rotas
app.use('/api', routes);

// Tratamento centralizado de erros
app.use(errorHandler);

// Inicialização do Banco de Dados
async function initDb() {
  await models.sequelize.sync({ force: true });
  
  // Seed inicial para bater com o legado
  const bcrypt = require('bcrypt');
  const hash = await bcrypt.hash('123', 10);
  
  const user = await models.User.create({ name: 'Leonan', email: 'leonan@fullcycle.com.br', password: hash });
  const course1 = await models.Course.create({ title: 'Clean Architecture', price: 997.00, active: true });
  const course2 = await models.Course.create({ title: 'Docker', price: 497.00, active: true });
  
  const enrollment = await models.Enrollment.create({ user_id: user.id, course_id: course1.id });
  await models.Payment.create({ enrollment_id: enrollment.id, amount: course1.price, status: 'PAID' });
}

module.exports = { app, initDb };
