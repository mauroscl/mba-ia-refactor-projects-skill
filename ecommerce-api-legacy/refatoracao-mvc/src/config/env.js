require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  dbDialect: process.env.DB_DIALECT || 'sqlite',
  dbStorage: process.env.DB_STORAGE || ':memory:',
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
  smtpUser: process.env.SMTP_USER,
  jwtSecret: process.env.JWT_SECRET
};
