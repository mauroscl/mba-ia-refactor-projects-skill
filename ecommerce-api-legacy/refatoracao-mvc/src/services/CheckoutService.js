const bcrypt = require('bcrypt');
const env = require('../config/env');

class CheckoutService {
  constructor({ courseRepository, userRepository, enrollmentRepository, paymentRepository, auditLogRepository }) {
    this.courseRepo = courseRepository;
    this.userRepo = userRepository;
    this.enrollmentRepo = enrollmentRepository;
    this.paymentRepo = paymentRepository;
    this.auditLogRepo = auditLogRepository;
  }

  async processCheckout({ username, email, password, courseId, creditCard }) {
    const course = await this.courseRepo.findActiveById(courseId);
    if (!course) {
      throw new Error('COURSE_NOT_FOUND');
    }

    let user = await this.userRepo.findByEmail(email);
    if (!user) {
      const hashedPassword = await bcrypt.hash(password || '123456', 10);
      user = await this.userRepo.create({ name: username, email, password: hashedPassword });
    }

    console.log(`Processando cartão ${creditCard} na chave ${env.paymentGatewayKey}`);
    const status = creditCard.startsWith('4') ? 'PAID' : 'DENIED';

    if (status === 'DENIED') {
      throw new Error('PAYMENT_DENIED');
    }

    const enrollment = await this.enrollmentRepo.create({ user_id: user.id, course_id: courseId });
    await this.paymentRepo.create({ enrollment_id: enrollment.id, amount: course.price, status });

    await this.auditLogRepo.create({ action: `Checkout curso ${courseId} por ${user.id}` });

    return { enrollment_id: enrollment.id, status: 'Success' };
  }
}

module.exports = CheckoutService;
