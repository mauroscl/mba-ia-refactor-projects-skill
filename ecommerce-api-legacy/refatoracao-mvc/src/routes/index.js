const express = require('express');
const container = require('../container');

const router = express.Router();

const checkoutController = container.resolve('checkoutController');
const reportController = container.resolve('reportController');
const userController = container.resolve('userController');

router.post('/checkout', checkoutController.checkout);
router.get('/admin/financial-report', reportController.getFinancialReport);
router.delete('/users/:id', userController.deleteUser);

module.exports = router;
