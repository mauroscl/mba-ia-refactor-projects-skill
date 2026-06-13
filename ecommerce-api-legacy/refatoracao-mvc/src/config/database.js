const { Sequelize } = require('sequelize');
const env = require('./env');

const sequelize = new Sequelize({
  dialect: env.dbDialect,
  storage: env.dbStorage,
  logging: false, // Disable logging for cleaner console
});

module.exports = sequelize;
