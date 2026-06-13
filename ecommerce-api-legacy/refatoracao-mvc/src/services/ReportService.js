class ReportService {
  constructor({ courseRepository, enrollmentRepository }) {
    this.courseRepo = courseRepository;
    this.enrollmentRepo = enrollmentRepository;
  }

  async getFinancialReport() {
    const courses = await this.courseRepo.findAll();
    const report = [];

    for (const course of courses) {
      const enrollments = await this.enrollmentRepo.findAllByCourseWithDetails(course.id);
      
      let revenue = 0;
      const students = [];

      for (const enr of enrollments) {
        // Find paid amount if any
        const paidPayments = enr.Payments ? enr.Payments.filter(p => p.status === 'PAID') : [];
        const paidAmount = paidPayments.reduce((sum, p) => sum + p.amount, 0);

        revenue += paidAmount;
        students.push({
          student: enr.User ? enr.User.name : 'Unknown',
          paid: paidAmount
        });
      }

      report.push({
        course: course.title,
        revenue,
        students
      });
    }

    return report;
  }
}

module.exports = ReportService;
