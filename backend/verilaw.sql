-- ============================================================
-- VeriLaw (Judiciary Flow) — Complete MySQL Schema
-- Compatible with MySQL 8.x and MySQL Workbench
-- ============================================================
drop database verilaw;
CREATE DATABASE IF NOT EXISTS verilaw
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE verilaw;

-- ─── USERS ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id       INT          NOT NULL AUTO_INCREMENT,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL,
    mobile        VARCHAR(15)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('citizen','lawyer','admin') NOT NULL DEFAULT 'citizen',
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_email  (email),
    UNIQUE KEY uq_users_mobile (mobile),
    INDEX idx_users_role (role)
) ENGINE=InnoDB;

-- ─── LAWYER PROFILES ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lawyer_profiles (
    profile_id         INT          NOT NULL AUTO_INCREMENT,
    user_id            INT          NOT NULL,
    bar_council_number VARCHAR(100) DEFAULT NULL,
    specialization     VARCHAR(200) DEFAULT NULL,
    experience_years   INT          NOT NULL DEFAULT 0,
    about              TEXT         DEFAULT NULL,
    availability       BOOLEAN      NOT NULL DEFAULT TRUE,
    rating             DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    total_cases        INT          NOT NULL DEFAULT 0,
    location           VARCHAR(200) DEFAULT NULL,
    created_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (profile_id),
    UNIQUE KEY uq_lawyer_user_id (user_id),
    CONSTRAINT fk_lawyer_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── COMPLAINT CATEGORIES ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS complaint_categories (
    category_id   INT          NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    description   TEXT         DEFAULT NULL,
    keywords      TEXT         DEFAULT NULL,
    PRIMARY KEY (category_id),
    UNIQUE KEY uq_category_name (category_name)
) ENGINE=InnoDB;

-- ─── DEPARTMENTS ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS departments (
    department_id   INT          NOT NULL AUTO_INCREMENT,
    department_name VARCHAR(150) NOT NULL,
    description     TEXT         DEFAULT NULL,
    website         VARCHAR(255) DEFAULT NULL,
    helpline        VARCHAR(20)  DEFAULT NULL,
    email           VARCHAR(150) DEFAULT NULL,
    PRIMARY KEY (department_id)
) ENGINE=InnoDB;

-- ─── COMPLAINTS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id  INT          NOT NULL AUTO_INCREMENT,
    user_id       INT          NOT NULL,
    category_id   INT          DEFAULT NULL,
    department_id INT          DEFAULT NULL,
    title         VARCHAR(200) NOT NULL,
    description   TEXT         NOT NULL,
    state         VARCHAR(100) NOT NULL,
    district      VARCHAR(100) NOT NULL,
    incident_date DATE         DEFAULT NULL,
    ai_confidence DECIMAL(5,2) DEFAULT NULL,
    status        ENUM('Draft','Processing','Completed','Closed') NOT NULL DEFAULT 'Draft',
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (complaint_id),
    INDEX idx_complaints_user_id      (user_id),
    INDEX idx_complaints_status       (status),
    INDEX idx_complaints_category_id  (category_id),
    INDEX idx_complaints_department_id(department_id),
    CONSTRAINT fk_complaints_user     FOREIGN KEY (user_id)       REFERENCES users(user_id)                    ON DELETE CASCADE,
    CONSTRAINT fk_complaints_category FOREIGN KEY (category_id)   REFERENCES complaint_categories(category_id) ON DELETE SET NULL,
    CONSTRAINT fk_complaints_dept     FOREIGN KEY (department_id) REFERENCES departments(department_id)         ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─── EVIDENCE ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id   INT          NOT NULL AUTO_INCREMENT,
    complaint_id  INT          NOT NULL,
    file_name     VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) DEFAULT NULL,
    file_type     VARCHAR(50)  DEFAULT NULL,
    file_size     BIGINT       DEFAULT NULL,
    file_path     VARCHAR(500) DEFAULT NULL,
    ocr_text      LONGTEXT     DEFAULT NULL,
    category      VARCHAR(100) DEFAULT NULL,
    upload_time   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (evidence_id),
    INDEX idx_evidence_complaint_id (complaint_id),
    INDEX idx_evidence_upload_time  (upload_time),
    CONSTRAINT fk_evidence_complaint FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── GENERATED DOCUMENTS ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS generated_documents (
    document_id   INT          NOT NULL AUTO_INCREMENT,
    complaint_id  INT          NOT NULL,
    user_id       INT          NOT NULL,
    document_type ENUM('PDF','HTML','DOCX') NOT NULL DEFAULT 'PDF',
    file_path     VARCHAR(500) DEFAULT NULL,
    generated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (document_id),
    INDEX idx_gendocs_complaint_id (complaint_id),
    INDEX idx_gendocs_user_id      (user_id),
    CONSTRAINT fk_gendocs_complaint FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE,
    CONSTRAINT fk_gendocs_user      FOREIGN KEY (user_id)      REFERENCES users(user_id)           ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── ACTIVITY LOGS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS activity_logs (
    log_id      INT          NOT NULL AUTO_INCREMENT,
    user_id     INT          NOT NULL,
    activity    VARCHAR(255) NOT NULL,
    ip_address  VARCHAR(45)  DEFAULT NULL,
    user_agent  VARCHAR(500) DEFAULT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    INDEX idx_activity_user_id    (user_id),
    INDEX idx_activity_created_at (created_at),
    CONSTRAINT fk_activity_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── APPOINTMENTS ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT          NOT NULL AUTO_INCREMENT,
    citizen_id     INT          NOT NULL,
    lawyer_id      INT          NOT NULL,
    complaint_id   INT          DEFAULT NULL,
    scheduled_at   DATETIME     NOT NULL,
    duration_mins  INT          NOT NULL DEFAULT 30,
    status         ENUM('Pending','Confirmed','Cancelled','Completed') NOT NULL DEFAULT 'Pending',
    notes          TEXT         DEFAULT NULL,
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (appointment_id),
    INDEX idx_appointments_citizen_id (citizen_id),
    INDEX idx_appointments_lawyer_id  (lawyer_id),
    INDEX idx_appointments_status     (status),
    CONSTRAINT fk_appt_citizen   FOREIGN KEY (citizen_id)   REFERENCES users(user_id)      ON DELETE CASCADE,
    CONSTRAINT fk_appt_lawyer    FOREIGN KEY (lawyer_id)    REFERENCES users(user_id)      ON DELETE CASCADE,
    CONSTRAINT fk_appt_complaint FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─── CHAT MESSAGES ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id   INT       NOT NULL AUTO_INCREMENT,
    sender_id    INT       NOT NULL,
    receiver_id  INT       NOT NULL,
    complaint_id INT       DEFAULT NULL,
    content      TEXT      NOT NULL,
    is_read      BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (message_id),
    INDEX idx_chat_sender_id   (sender_id),
    INDEX idx_chat_receiver_id (receiver_id),
    INDEX idx_chat_is_read     (is_read),
    CONSTRAINT fk_chat_sender    FOREIGN KEY (sender_id)    REFERENCES users(user_id)           ON DELETE CASCADE,
    CONSTRAINT fk_chat_receiver  FOREIGN KEY (receiver_id)  REFERENCES users(user_id)           ON DELETE CASCADE,
    CONSTRAINT fk_chat_complaint FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─── NOTIFICATIONS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT          NOT NULL AUTO_INCREMENT,
    user_id         INT          NOT NULL,
    title           VARCHAR(200) NOT NULL,
    message         TEXT         NOT NULL,
    type            ENUM('info','success','warning','error') NOT NULL DEFAULT 'info',
    is_read         BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (notification_id),
    INDEX idx_notifications_user_id (user_id),
    INDEX idx_notifications_is_read (is_read),
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── FEEDBACK ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id  INT       NOT NULL AUTO_INCREMENT,
    user_id      INT       NOT NULL,
    complaint_id INT       DEFAULT NULL,
    rating       TINYINT   NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT      DEFAULT NULL,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (feedback_id),
    INDEX idx_feedback_user_id (user_id),
    CONSTRAINT fk_feedback_user      FOREIGN KEY (user_id)      REFERENCES users(user_id)           ON DELETE CASCADE,
    CONSTRAINT fk_feedback_complaint FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─── REPORTS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reports (
    report_id    INT          NOT NULL AUTO_INCREMENT,
    generated_by INT          NOT NULL,
    report_type  VARCHAR(50)  NOT NULL,
    parameters   TEXT         DEFAULT NULL,
    file_path    VARCHAR(500) DEFAULT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_id),
    INDEX idx_reports_generated_by (generated_by),
    CONSTRAINT fk_reports_user FOREIGN KEY (generated_by) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── CASES ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cases (
    id          INT          NOT NULL AUTO_INCREMENT,
    user_id     INT          NOT NULL,
    title       VARCHAR(255) NOT NULL,
    category    VARCHAR(100) NOT NULL,
    description TEXT         DEFAULT NULL,
    status      ENUM('Draft','Active','Verification Running','Complaint Generated','Resolved','Archived') NOT NULL DEFAULT 'Draft',
    priority    ENUM('Low','Medium','High','Critical') NOT NULL DEFAULT 'Medium',
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_cases_user_id (user_id),
    INDEX idx_cases_status (status),
    INDEX idx_cases_priority (priority),
    CONSTRAINT fk_cases_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── VIEWS ─────────────────────────────────────────────────────
CREATE OR REPLACE VIEW complaint_summary AS
SELECT
    c.complaint_id,
    u.full_name        AS citizen_name,
    u.email            AS citizen_email,
    cc.category_name,
    d.department_name,
    c.title,
    c.status,
    c.state,
    c.district,
    c.created_at
FROM complaints c
JOIN users u ON c.user_id = u.user_id
LEFT JOIN complaint_categories cc ON c.category_id = cc.category_id
LEFT JOIN departments d ON c.department_id = d.department_id;

CREATE OR REPLACE VIEW dashboard_summary AS
SELECT
    user_id,
    COUNT(*)                                             AS total_complaints,
    SUM(status = 'Draft')                               AS draft_count,
    SUM(status = 'Processing')                          AS processing_count,
    SUM(status = 'Completed')                           AS completed_count
FROM complaints
GROUP BY user_id;

-- ─── TRIGGERS ──────────────────────────────────────────────────
DELIMITER $$

CREATE TRIGGER trg_complaint_log
AFTER INSERT ON complaints
FOR EACH ROW
BEGIN
    INSERT INTO activity_logs (user_id, activity)
    VALUES (NEW.user_id, CONCAT('Complaint Created: ', NEW.title));
END$$

DELIMITER ;

-- ─── SEED: Complaint Categories ────────────────────────────────
INSERT IGNORE INTO complaint_categories (category_name, description, keywords) VALUES
('Consumer Complaint',  'Consumer product or service issues',            'product,defective,refund,seller,purchase,ecommerce'),
('Labour Complaint',    'Employment and workplace related complaints',    'salary,employer,workplace,job,harassment,termination'),
('Cyber Crime',         'Online fraud and cyber incidents',              'online,fraud,hack,phishing,scam,cyber,internet'),
('Property Dispute',    'Land and property related issues',              'land,property,rent,tenant,encroachment,lease'),
('Banking Complaint',   'Bank and financial institution complaints',     'bank,loan,account,credit,debit,emi,fraud,atm'),
('Insurance Complaint', 'Insurance claim and policy disputes',           'insurance,claim,policy,premium,settlement'),
('Municipal Complaint', 'Civic amenities and municipal issues',          'water,roads,garbage,electricity,municipality,drainage'),
('RTI',                 'Right to Information requests',                 'rti,information,government,public,transparency'),
('Women Safety',        'Women safety and harassment complaints',        'harassment,dowry,domestic,violence,women,safety'),
('Tenant Dispute',      'Landlord and tenant conflicts',                 'rent,landlord,tenant,eviction,deposit,lease');

-- ─── SEED: Departments ─────────────────────────────────────────
INSERT IGNORE INTO departments (department_name, description, website, helpline, email) VALUES
('Consumer Commission',          'Handles consumer disputes',                           'https://consumerhelpline.gov.in',  '1800-11-4000', 'consumerhelpline@nic.in'),
('Labour Department',            'Handles employment and labour disputes',               'https://labour.gov.in',            '1800-11-2222', 'labour@nic.in'),
('Cyber Crime Cell',             'Handles cyber crime complaints',                       'https://cybercrime.gov.in',        '1930',         'cybercrime@nic.in'),
('Land Revenue Department',      'Handles property and land disputes',                  'https://dolr.gov.in',              NULL,           'dolr@nic.in'),
('Banking Ombudsman',            'Handles banking related complaints',                   'https://bankingombudsman.rbi.org', '14448',        'rbi@rbi.org.in'),
('IRDAI',                        'Insurance Regulatory and Development Authority',       'https://www.irdai.gov.in',         '155255',       'complaints@irdai.gov.in'),
('Municipal Corporation',        'Handles civic and municipal complaints',               NULL,                               NULL,           NULL),
('Central Information Commission','Handles RTI appeals and complaints',                 'https://cic.gov.in',               NULL,           'cic@nic.in'),
('National Commission for Women','Handles women safety and harassment cases',           'https://ncw.nic.in',               '7827170170',   'ncw@nic.in'),
('District Court',               'Handles civil disputes including tenant issues',       NULL,                               NULL,           NULL),
('Police Department',            'Handles criminal complaints and FIR registration',    NULL,                               '100',          NULL);

-- ─── SEED: Admin User ──────────────────────────────────────────
-- Default credentials: admin@judiciaryflow.in / Admin@123456
-- Hash will be generated by Flask at first run (see init_db in app.py).
-- This is a placeholder; the actual app seeds the admin via Python.
