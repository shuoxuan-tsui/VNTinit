-- vntdb_schema.sql
-- 该脚本创建 vntdb 数据库中的核心业务表及其约束、索引
-- 如需重新初始化数据库，可按顺序执行本脚本

-- 扩展：启用 uuid 生成函数
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/*============================================================
表：api_department   （部门）
============================================================*/
CREATE TABLE IF NOT EXISTS public.api_department (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(100)  NOT NULL,
    code            VARCHAR(20)   NOT NULL,
    description     TEXT          NOT NULL DEFAULT ''::TEXT,
    manager         VARCHAR(100)  NOT NULL DEFAULT ''::VARCHAR,
    manager_title   VARCHAR(100)  NOT NULL DEFAULT ''::VARCHAR,
    location        VARCHAR(200)  NOT NULL DEFAULT ''::VARCHAR,
    phone           VARCHAR(20)   NOT NULL DEFAULT ''::VARCHAR,
    email           VARCHAR(254)  NOT NULL DEFAULT ''::VARCHAR,
    budget          NUMERIC(12,2) NOT NULL DEFAULT 0,
    status          VARCHAR(20)   NOT NULL DEFAULT 'active',
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    CONSTRAINT api_department_name_key UNIQUE (name),
    CONSTRAINT api_department_code_key UNIQUE (code)
);

-- 索引
CREATE INDEX IF NOT EXISTS api_departm_name_cbbdb1_idx ON public.api_department (name);

CREATE INDEX IF NOT EXISTS api_departm_code_dcd7e2_idx ON public.api_department (code);

CREATE INDEX IF NOT EXISTS api_departm_status_0b40bb_idx ON public.api_department (status);

/*============================================================
表：api_employee   （员工）
============================================================*/

CREATE TABLE IF NOT EXISTS public.api_employee (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id      VARCHAR(20)  NOT NULL,
    name             VARCHAR(100) NOT NULL,
    gender           VARCHAR(1)   NOT NULL,
    department       VARCHAR(100) NOT NULL,
    department_ref_id UUID NULL,
    position         VARCHAR(100) NOT NULL,
    phone            VARCHAR(20)  NOT NULL DEFAULT ''::VARCHAR,
    hire_date        DATE         NOT NULL,
    birth_date       DATE         NULL,
    base_salary      NUMERIC(10,2) NOT NULL,
    status           VARCHAR(20)   NOT NULL DEFAULT 'active',
    location         VARCHAR(200),
    notes            TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT api_employee_employee_id_key UNIQUE (employee_id),
    CONSTRAINT api_employee_department_ref_fk FOREIGN KEY (department_ref_id)
        REFERENCES public.api_department(id) ON UPDATE RESTRICT ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED
);

-- 索引
CREATE INDEX IF NOT EXISTS api_employe_employe_0a2b07_idx ON public.api_employee (employee_id);

CREATE INDEX IF NOT EXISTS api_employe_departm_a88d93_idx ON public.api_employee (department);

CREATE INDEX IF NOT EXISTS api_employe_positio_a8b669_idx ON public.api_employee (position);

CREATE INDEX IF NOT EXISTS api_employe_name_463c63_idx ON public.api_employee (name);

CREATE INDEX IF NOT EXISTS api_employee_department_ref_id_idx ON public.api_employee (department_ref_id);

/*============================================================
表：api_salaryrecord   （薪资记录）
============================================================*/
CREATE TABLE IF NOT EXISTS public.api_salaryrecord (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    employee_id UUID NOT NULL,
    salary_period VARCHAR(7) NOT NULL,
    position_snapshot VARCHAR(100) NOT NULL,
    base_salary_snapshot NUMERIC(10, 2) NOT NULL,
    bonus NUMERIC(10, 2) NOT NULL DEFAULT 0,
    deductions NUMERIC(10, 2) NOT NULL DEFAULT 0,
    gross_salary NUMERIC(10, 2) NOT NULL,
    net_salary NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT api_salaryrecord_employee_period_uniq UNIQUE (employee_id, salary_period),
    CONSTRAINT api_salaryrecord_employee_fk FOREIGN KEY (employee_id) REFERENCES public.api_employee (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- 索引
CREATE INDEX IF NOT EXISTS api_salaryr_employe_46c67d_idx ON public.api_salaryrecord (employee_id, salary_period);

CREATE INDEX IF NOT EXISTS api_salaryr_salary_period_idx ON public.api_salaryrecord (salary_period);

CREATE INDEX IF NOT EXISTS api_salaryr_created_idx ON public.api_salaryrecord (created_at);

/*============================================================
表：api_attendancerecord   （考勤记录）
============================================================*/
CREATE TABLE IF NOT EXISTS public.api_attendancerecord (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    employee_id UUID NOT NULL,
    date DATE NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    status VARCHAR(20) NOT NULL DEFAULT 'present',
    work_hours NUMERIC(4, 2) NOT NULL DEFAULT 0,
    overtime_hours NUMERIC(4, 2) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT api_attendancerecord_employee_date_uniq UNIQUE (employee_id, date),
    CONSTRAINT api_attendancerecord_employee_fk FOREIGN KEY (employee_id) REFERENCES public.api_employee (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- 索引
CREATE INDEX IF NOT EXISTS api_attenda_employe_c3e514_idx ON public.api_attendancerecord (employee_id, date);

CREATE INDEX IF NOT EXISTS api_attenda_date_2082cd_idx ON public.api_attendancerecord (date);

CREATE INDEX IF NOT EXISTS api_attenda_status_f113d0_idx ON public.api_attendancerecord (status);

CREATE INDEX IF NOT EXISTS api_attenda_created_idx ON public.api_attendancerecord (created_at);

-- 结束