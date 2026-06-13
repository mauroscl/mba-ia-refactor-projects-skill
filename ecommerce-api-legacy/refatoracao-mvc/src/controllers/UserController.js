class UserController {
  constructor({ userService }) {
    this.userService = userService;
    this.deleteUser = this.deleteUser.bind(this);
  }

  async deleteUser(req, res, next) {
    try {
      const { id } = req.params;
      await this.userService.deleteUser(id);
      return res.status(200).send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
    } catch (error) {
      if (error.message === 'USER_NOT_FOUND') {
        return res.status(404).json({ error: 'Usuário não encontrado' });
      }
      next(error);
    }
  }
}

module.exports = UserController;
