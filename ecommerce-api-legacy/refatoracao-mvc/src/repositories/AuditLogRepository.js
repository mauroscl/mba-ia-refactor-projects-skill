class AuditLogRepository {
  constructor({ auditLogModel }) {
    this.model = auditLogModel;
  }
  async create(logData) {
    return await this.model.create(logData);
  }
}
module.exports = AuditLogRepository;
