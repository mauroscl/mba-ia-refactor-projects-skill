class UserRepository {
  constructor({ userModel }) {
    this.model = userModel;
  }
  async findByEmail(email) {
    return await this.model.findOne({ where: { email } });
  }
  async create(userData) {
    return await this.model.create(userData);
  }
  async deleteById(id) {
    return await this.model.destroy({ where: { id } });
  }
}
module.exports = UserRepository;
