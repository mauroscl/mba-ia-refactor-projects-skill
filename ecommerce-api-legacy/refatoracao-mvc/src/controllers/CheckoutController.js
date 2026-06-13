class CheckoutController {
  constructor({ checkoutService }) {
    this.checkoutService = checkoutService;
    this.checkout = this.checkout.bind(this);
  }

  async checkout(req, res, next) {
    try {
      const username = req.body.usr;
      const email = req.body.eml;
      const password = req.body.pwd;
      const courseId = req.body.c_id;
      const creditCard = req.body.card;

      if (!username || !email || !courseId || !creditCard) {
        return res.status(400).send('Bad Request');
      }

      const result = await this.checkoutService.processCheckout({
        username, email, password, courseId, creditCard
      });

      return res.status(200).json({ msg: 'Sucesso', enrollment_id: result.enrollment_id });
    } catch (error) {
      if (error.message === 'COURSE_NOT_FOUND') {
        return res.status(404).send('Curso não encontrado');
      }
      if (error.message === 'PAYMENT_DENIED') {
        return res.status(400).send('Pagamento recusado');
      }
      next(error);
    }
  }
}

module.exports = CheckoutController;
