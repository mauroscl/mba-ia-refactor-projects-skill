class ReportController {
  constructor({ reportService }) {
    this.reportService = reportService;
    this.getFinancialReport = this.getFinancialReport.bind(this);
  }

  async getFinancialReport(req, res, next) {
    try {
      const report = await this.reportService.getFinancialReport();
      return res.status(200).json(report);
    } catch (error) {
      next(error);
    }
  }
}

module.exports = ReportController;
