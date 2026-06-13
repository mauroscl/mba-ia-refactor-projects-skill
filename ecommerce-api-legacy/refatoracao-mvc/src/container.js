const { asClass, asValue, createContainer } = require('awilix');
const models = require('./models');

// Repositories
const CourseRepository = require('./repositories/CourseRepository');
const UserRepository = require('./repositories/UserRepository');
const EnrollmentRepository = require('./repositories/EnrollmentRepository');
const PaymentRepository = require('./repositories/PaymentRepository');
const AuditLogRepository = require('./repositories/AuditLogRepository');

// Services
const CheckoutService = require('./services/CheckoutService');
const ReportService = require('./services/ReportService');
const UserService = require('./services/UserService');

// Controllers
const CheckoutController = require('./controllers/CheckoutController');
const ReportController = require('./controllers/ReportController');
const UserController = require('./controllers/UserController');

const container = createContainer();

container.register({
  // Models
  courseModel: asValue(models.Course),
  userModel: asValue(models.User),
  enrollmentModel: asValue(models.Enrollment),
  paymentModel: asValue(models.Payment),
  auditLogModel: asValue(models.AuditLog),

  // Repositories
  courseRepository: asClass(CourseRepository).singleton(),
  userRepository: asClass(UserRepository).singleton(),
  enrollmentRepository: asClass(EnrollmentRepository).singleton(),
  paymentRepository: asClass(PaymentRepository).singleton(),
  auditLogRepository: asClass(AuditLogRepository).singleton(),

  // Services
  checkoutService: asClass(CheckoutService).singleton(),
  reportService: asClass(ReportService).singleton(),
  userService: asClass(UserService).singleton(),

  // Controllers
  checkoutController: asClass(CheckoutController).singleton(),
  reportController: asClass(ReportController).singleton(),
  userController: asClass(UserController).singleton()
});

module.exports = container;
