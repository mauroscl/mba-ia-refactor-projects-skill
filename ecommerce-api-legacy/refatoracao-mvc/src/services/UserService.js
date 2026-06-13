class UserService {
  constructor({ userRepository }) {
    this.userRepo = userRepository;
  }

  async deleteUser(id) {
    const deleted = await this.userRepo.deleteById(id);
    if (!deleted) {
      throw new Error('USER_NOT_FOUND');
    }
    return deleted;
  }
}

module.exports = UserService;
