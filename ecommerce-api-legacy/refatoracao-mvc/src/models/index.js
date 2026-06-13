const sequelize = require('../config/database');
const { DataTypes } = require('sequelize');

const User = sequelize.define('User', {
  name: { type: DataTypes.STRING, allowNull: false },
  email: { type: DataTypes.STRING, allowNull: false, unique: true },
  password: { type: DataTypes.STRING, allowNull: false }
}, { tableName: 'users', timestamps: false });

const Course = sequelize.define('Course', {
  title: { type: DataTypes.STRING, allowNull: false },
  price: { type: DataTypes.FLOAT, allowNull: false },
  active: { type: DataTypes.BOOLEAN, defaultValue: true }
}, { tableName: 'courses', timestamps: false });

const Enrollment = sequelize.define('Enrollment', {
  // auto-generated ID is handled by Sequelize
}, { tableName: 'enrollments', timestamps: false });

const Payment = sequelize.define('Payment', {
  amount: { type: DataTypes.FLOAT, allowNull: false },
  status: { type: DataTypes.STRING, allowNull: false }
}, { tableName: 'payments', timestamps: false });

const AuditLog = sequelize.define('AuditLog', {
  action: { type: DataTypes.STRING, allowNull: false },
  createdAt: { type: DataTypes.DATE, defaultValue: DataTypes.NOW, field: 'created_at' }
}, { tableName: 'audit_logs', timestamps: false });

// Setup relationships
User.hasMany(Enrollment, { foreignKey: 'user_id' });
Enrollment.belongsTo(User, { foreignKey: 'user_id' });

Course.hasMany(Enrollment, { foreignKey: 'course_id' });
Enrollment.belongsTo(Course, { foreignKey: 'course_id' });

Enrollment.hasMany(Payment, { foreignKey: 'enrollment_id' });
Payment.belongsTo(Enrollment, { foreignKey: 'enrollment_id' });

module.exports = {
  sequelize,
  User,
  Course,
  Enrollment,
  Payment,
  AuditLog
};
