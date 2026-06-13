class EnrollmentRepository {
  constructor({ enrollmentModel, userModel, paymentModel }) {
    this.model = enrollmentModel;
    this.userModel = userModel;
    this.paymentModel = paymentModel;
  }
  async create(enrollmentData) {
    return await this.model.create(enrollmentData);
  }
  async findAllByCourseWithDetails(courseId) {
    return await this.model.findAll({
      where: { course_id: courseId },
      include: [
        { model: this.userModel, required: true },
        { model: this.paymentModel, required: false }
      ]
    });
  }
}
module.exports = EnrollmentRepository;
