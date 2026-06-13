class PaymentRepository {
  constructor({ paymentModel }) {
    this.model = paymentModel;
  }
  async create(paymentData) {
    return await this.model.create(paymentData);
  }
}
module.exports = PaymentRepository;
