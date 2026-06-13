class CourseRepository {
  constructor({ courseModel }) {
    this.model = courseModel;
  }
  async findActiveById(id) {
    return await this.model.findOne({ where: { id, active: true } });
  }
  async findAll() {
    return await this.model.findAll();
  }
}
module.exports = CourseRepository;
